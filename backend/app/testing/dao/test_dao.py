from typing import List
from app.testing.dao.test_result_dao import test_result_dao
from app.testing.dao.choice_dao import choice_dao
from app.testing.schema.test import SCreateTest, SUpdateTest
from app.testing.dao.question_dao import question_dao
from common.base_dao import BaseDao
from app.testing.model.test import Test
from core.db_postgres import AsyncSession
from app.testing.model.choice import Choice
from app.testing.model.question import Question
from app.testing.model.user_answer import UserAnswer
from app.testing.model.test_result import TestResult
from app.testing.dao.user_answer_dao import user_answer_dao
from sqlalchemy import Boolean, case, cast, select, text, update, delete, func
from sqlalchemy.orm import selectinload
from common.exceptions.error import InvalidOrderByValueException, NoAnswerToQuestionException, AnswerOptionNotFoundException, QuestionNotFoundException, TestNameAlreadyExistsException, TestNotFoundException
from datetime import UTC, datetime, timedelta, date
from uuid import UUID

class TestDao(BaseDao[Test]):
  async def is_active(self, db: AsyncSession, test_id: int) -> bool:
    """Проверка доступности теста для прохождения"""
    # async with async_session_maker() as session:
    msk_now = func.timezone("Europe/Moscow", func.now())
    query = select(Test.id).where(
      Test.id == test_id,
      Test.date_from <= msk_now,
      Test.date_to >= msk_now,
    )
    result = await db.execute(query)
    return bool(result.scalars().all())
  
  async def was_passed(self, db: AsyncSession, user_id: str, test_id: int):
    query = (
      select(Question.test_id)
      .join(
        Choice,
        Choice.question_id == Question.id,
      )
      .join(
        UserAnswer,
        UserAnswer.choice_id == Choice.id,
      )
      .where(
        UserAnswer.user_id == user_id,
        Question.test_id == test_id,
      )  
    )
    result = await db.execute(query)
    return bool(result.scalars().all())
  
  async def add_result(self, db: AsyncSession, user_id: str, test_id: int, user_answer_ids: List[int]):
    await self.check_answer_options_in_test(db, test_id, user_answer_ids)
    await self.check_all_questions_have_answer(db, test_id, user_answer_ids)

    for question_id in user_answer_ids:
        await user_answer_dao.insert_uncommit(
          db, user_id=user_id, choice_id=question_id
        )

    test = await self.get_test(db, test_id)
    correct_question_count = 0
    for question in test.questions:
        correct_question = True
        for option in question.choices:
          if (
            option.is_correct
            and option.id not in user_answer_ids
            or not option.is_correct
            and option.id in user_answer_ids
          ):
            correct_question = False
            break

        if correct_question:
          correct_question_count += 1

    await test_result_dao.insert_uncommit(
      db,
      test_id=test_id,
      user_id=user_id,
      question_count=len(test.questions),
      correct_question_count=correct_question_count,
    )
    await db.commit()

  async def check_answer_options_in_test(self, db, test_id: int, answer_option_ids: list) -> None:
    """Проверка наличия вариантов ответов в тесте"""
    choicess = await self.get_answer_option_ids_by_test_id(db, test_id)
    for answer_option_id in answer_option_ids:
      if answer_option_id not in choicess:
        raise AnswerOptionNotFoundException
      
  async def get_answer_option_ids_by_test_id(self, db: AsyncSession, test_id: int) -> List:
    """Получение списка id враиантов ответов по id теста"""
    query = (
      select(Choice.id)
      .join(
          Question,
          Choice.question_id == Question.id,
      )
      .where(Question.test_id == test_id)
    )
    result = await db.execute(query)
    return result.scalars().all()
  
  async def check_all_questions_have_answer(self, db, test_id: int, answer_option_ids: list) -> None:
    """Проверка наличия хотя бы одного ответа на каждый вопрос теста"""
    test = await self.get_test(db, test_id)
    for question in test.questions:
      for option in question.choices:
        if option.id in answer_option_ids:
          break
      else:
        raise NoAnswerToQuestionException
      
  async def get_test(self, db: AsyncSession, test_id: int):
    """Получение полной информации о тесте с вопросами и ответами"""
    query = (
      select(Test)
      .options(
        selectinload(Test.questions).selectinload(Question.choices),
      )
      .where(Test.id == test_id)
    )
    result = await db.execute(query)
    return result.scalars().one()
  
  async def get_tests_finished_at_month(self, db: AsyncSession, user_id: UUID, date: date):
    end_date = (date + timedelta(days=32)).replace(day=1)
    query = (
      select(
        Test.id.label("test_id"),
        Test.name,
        TestResult.user_id,
        TestResult.created_at.label("finish_date"),
        func.concat(
          TestResult.correct_question_count,
          "/",
          TestResult.question_count,
        ).label("result"),
      )
      .join(TestResult)
      .where(TestResult.user_id == user_id)
      .where(TestResult.created_at >= date)
      .where(TestResult.created_at < end_date)
    )

    result = await db.execute(query)
    return result.mappings().all()
  
  async def delete_test(self, db: AsyncSession, test_id: int):
    """Удаление теста"""
    exist_test = await self.select_one(db, id=test_id)
    await db.delete(exist_test)
    await db.commit()
  
  async def create_test(
    self,
    db: AsyncSession,
    test: SCreateTest,
    ):
    """Создание нового теста"""
    # async with async_session_maker() as session:
    test_exsist = await self.find_one_or_none(db, name=test.name)

    if test_exsist:
      raise TestNameAlreadyExistsException

    new_test = await self.insert_uncommit(
      db,
      name=test.name,
      date_from=test.date_from,
      date_to=test.date_to,
    )

    for question in test.questions:
      new_question = await question_dao.insert_uncommit(
        db, test_id=new_test.id, text=question.text
      )

      for answer in question.choices:
        await choice_dao.insert_uncommit(
          db,
          question_id=new_question.id,
          text=answer.text,
          is_correct=answer.is_correct,
        )

    await db.commit()
    return new_test.id
  
  async def get_test_result(self, db: AsyncSession, user_id: UUID, test_id: int):
    """Получение результата теста"""
    # async with async_session_maker() as session:
    query = (
      select(Test)
      .options(
        selectinload(Test.questions)
        .selectinload(Question.choices)
        .selectinload(Choice.user_answers)
      )
      .where(Test.id == test_id)
    )

    result = (await db.execute(query)).scalars().one()

    for i, question in enumerate(result.questions):
      correct_option_len = 0
      correct_answer_len = 0
      answer_len = 0
      for j, option in enumerate(question.choices):
          if option.is_correct:
            correct_option_len += 1
          for user_answer in option.user_answers:
            if user_answer.user_id == user_id:
              result.questions[i].choices[j].selected = True
              answer_len += 1
              break
          else:
            result.questions[i].choices[j].selected = False

          if option.selected == option.is_correct:
            result.questions[i].choices[j].correct_answer = True

            if option.is_correct:
              correct_answer_len += 1
          else:
            result.questions[i].choices[j].correct_answer = False

      result.questions[i].correct_answers = (
        correct_answer_len == correct_option_len
        and correct_option_len == answer_len
      )
      result.questions[i].color = (
        "green" if result.questions[i].correct_answers else "red"
      )

      if correct_option_len > 1:
        result.questions[i].multiple_answer = True

    return result
  
  async def get_test_list(
        self,
        db: AsyncSession,
        user_id: str,
        offset: int = 0,
        limit: int = None,
    ) -> list:
        """Получение списка всех тестов с дополнительной информацией о том,
        был ли пройден тест пользователем с переданным user_id.
        Результаты сортируютя по дате окончания теста по убыванию.
        Возвращается часть результата согласно offset и limit"""

        # async with async_session_maker() as session:
        passed_test = (
            select(Question.test_id.distinct().label("id"))
            .join(
                Choice,
                Choice.question_id == Question.id,
            )
            .join(
                UserAnswer,
                UserAnswer.choice_id == Choice.id,
            )
            .where(UserAnswer.user_id == user_id)
            .subquery()
        )

        msk_now = func.timezone("Europe/Moscow", func.now())
        is_active_expr = case(
            (
                (Test.date_to >= msk_now) & (Test.date_from <= msk_now),
                True,
            ),
            else_=False,
        )

        query = (
            select(
                Test.__table__.columns,
                func.coalesce(cast(passed_test.c.id, Boolean), False).label(
                    "was_passed"
                ),
                is_active_expr.label("is_active"),
            )
            .select_from(
                Test.__table__.outerjoin(passed_test, Test.id == passed_test.c.id)
            )
            .order_by(Test.date_to.desc())
            .offset(offset)
        )

        if limit:
            query = query.limit(limit)

        result = await db.execute(query)

        return result.mappings().all()
  
  async def get_test_results(
        self, db: AsyncSession, date_from, date_to, order_by="employee_name", desc=False
    ) -> List:
        # async with async_session_maker() as session:
        if order_by not in [
            "employee_name",
            "employee_email",
            "points",
            "rank",
        ]:
            raise InvalidOrderByValueException
        if order_by == "points":
            order_by = "sum(correct_question_count)"

        query = text(
            f"""with tests_in_month as (
                select t.id as test_id, DATE_TRUNC('month', date_from) as date_from_month, count(*) as question_count
                from test t
                join question q 
                on t.id = q.test_id
                where DATE_TRUNC('day', date_from) >= '{date_from}' and DATE_TRUNC('day', date_from) <= '{date_to}'
                group by t.id, TO_CHAR(date_from, 'MM.YYYY')
            ), tests_with_options as (
                select t.test_id, q.id as question_id, tao.id as choice_id, is_correct
                from tests_in_month t
                join question q 
                on t.test_id = q.test_id
                join choices tao
                on q.id = tao.question_id
            ), users_in_period as (
                select distinct ua.user_id
                from tests_with_options t
                join user_answer ua 
                on t.choice_id = ua.choice_id
            ), correct_answer as (
                select t.test_id, t.question_id, sum(is_correct::int) correct_answer_count
                from tests_with_options t
                group by t.test_id, t.question_id
            ), correct_user_answer as (
                select ua.user_id, t.test_id, t.question_id, count(*) correct_user_answer_count
                from tests_with_options t
                join user_answer ua 
                on t.choice_id = ua.choice_id 
                where is_correct is true 
                group by ua.user_id, t.test_id, t.question_id
            ), test_result as (
    select 
        t.test_id,
        user_answer.user_id,
        count(distinct case 
            when user_correct = total_correct and user_incorrect = 0 
            then question_id 
        end) as correct_question_count
    from tests_in_month t
    join (
        select 
            ua.user_id,
            tq.test_id,
            tq.id as question_id,
            -- Количество правильных ответов пользователя
            count(case when tao.is_correct then 1 end) as user_correct,
            -- Количество неправильных ответов пользователя
            count(case when not tao.is_correct then 1 end) as user_incorrect,
            ca.total_correct
        from user_answer ua
        join choices tao on ua.choice_id = tao.id
        join question tq on tao.question_id = tq.id
        join (
            select 
                question_id,
                count(*) as total_correct
            from choices
            where is_correct = true
            group by question_id
        ) ca on tq.id = ca.question_id
        group by ua.user_id, tq.id, tq.test_id, ca.total_correct
    ) user_answer on t.test_id = user_answer.test_id
    group by t.test_id, user_answer.user_id
), full_test_result as (
                select t.*, u.user_id, coalesce(tr.correct_question_count, 0) correct_question_count
                from tests_in_month t
                cross join users_in_period u
                left join test_result tr
                on t.test_id = tr.test_id
                and u.user_id = tr.user_id
            ) select tr.date_from_month , u.id user_id, u.name employee_name, u.uid employee_email, sum(correct_question_count) || '/' || sum(question_count) points, 
            RANK() over(partition by tr.date_from_month order by sum(correct_question_count) desc) rank
            from full_test_result tr
            join "user" u 
            on tr.user_id = u.id
            group by tr.date_from_month, u.id, u.name, u.uid
            order by tr.date_from_month, {order_by} {'desc' if desc else ''} """
        )
        result = await db.execute(query)
        return result.mappings().all()
  
  async def get_answer_ids_by_test_id(
        self,
        db: AsyncSession,
        test_id: int,
    ) -> list:
        """Получение списка id ответов по id теста"""
        query = (
            select(UserAnswer.id)
            .join(
                Choice,
                UserAnswer.choice_id == Choice.id,
            )
            .join(
                Question,
                Choice.question_id == Question.id,
            )
            .where(Question.test_id == test_id)
        )
        result = await db.execute(query)
        return result.scalars().all()
  
  async def update_test(
        self,
        db: AsyncSession,
        test_id: int,
        updated_test: SUpdateTest,
        has_changes_in_questions: bool,
    ):
        """Изменение теста, вопросов и ответов"""
        # async with async_session_maker() as session:
        existing_test = await self.select_one(db, id=test_id)
        if not existing_test:
            raise TestNotFoundException
        updated_test = SUpdateTest(**updated_test)

        existing_test.name = updated_test.name
        existing_test.date_from = updated_test.date_from
        existing_test.date_to = updated_test.date_to

        if has_changes_in_questions:
            if result_ids := await self.get_answer_ids_by_test_id(db, test_id):
                existing_test.result_resets = True
                for result_id in result_ids:
                    await user_answer_dao.delete_uncommit(db, result_id)

                test_result_ids = await test_result_dao.get_ids(db, test_id=test_id)
                for test_result_id in test_result_ids:
                    await test_result_dao.delete_uncommit(db, test_result_id)

            updated_question_ids = set()
            existing_question_ids = set(
                await question_dao.get_ids(db, test_id=test_id)
            )

            for question in updated_test.questions:
                if question.id is None:
                    # если нет id, то создаем новый вопрос и варианты ответа
                    existing_question = await question_dao.insert_uncommit(
                        db, test_id=test_id, text=question.text
                    )
                    for option in question.choices:
                        await choice_dao.insert_uncommit(
                            db,
                            question_id=existing_question.id,
                            text=option.text,
                            is_correct=option.is_correct,
                        )

                else:
                    # если есть id, то обновляем вопрос
                    existing_question = await question_dao.select_one(
                        db, id=question.id, test_id=test_id
                    )
                    if not existing_question:
                        raise QuestionNotFoundException

                    existing_question.text = question.text

                    updated_option_ids = set()
                    existing_option_ids = set(
                        await choice_dao.get_ids(
                            db, question_id=question.id
                        )
                    )

                    for option in question.choices:
                        if option.id is None:
                            # если нет id, то создаем новый вариант ответа
                            await choice_dao.insert_uncommit(
                                db,
                                question_id=question.id,
                                text=option.text,
                                is_correct=option.is_correct,
                            )
                        else:
                            # если есть id, то обновляем вариант ответа
                            existing_option = await choice_dao.select_one(
                                db,
                                id=option.id,
                                question_id=question.id,
                            )
                            if not existing_option:
                                raise AnswerOptionNotFoundException

                            existing_option.text = option.text
                            existing_option.is_correct = option.is_correct

                            updated_option_ids.add(option.id)

                    # удаление вариантов ответов,
                    # которых нет в обновленном списке
                    for option_id in existing_option_ids - updated_option_ids:
                        await choice_dao.delete_uncommit(db, option_id)

                    updated_question_ids.add(question.id)

            for question_id in existing_question_ids - updated_question_ids:
                await question_dao.delete_uncommit(db, question_id)

        existing_test.updated_at = datetime.now(UTC).replace(tzinfo=None)

        await db.commit()

test_dao: TestDao = TestDao(Test)