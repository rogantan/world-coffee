import calendar

from app.testing.dao.test_dao import test_dao
from app.testing.schema.test import SCreateTest, SUpdateTest
from app.utils.support import compare_dicts, get_month_range
from common.exceptions.error import TestAlreadyPassedException, TestNameAlreadyExistsException, TestNoActiveException
from core.db_postgres import async_session
from app.testing.dao.choice_dao import choice_dao
from typing import List
from datetime import date

class TestService:
  async def get_test(self, test_id: int):
    async with async_session() as session:
      return await test_dao.get_test(session, test_id)
    
  async def is_test_active(self, test_id: int):
    async with async_session() as session:
      return await test_dao.is_active(session, test_id)
  
  async def is_test_passed(self, user, test_id: int):
    async with async_session() as session:
      return test_dao.was_passed(session, user.id, test_id)
  
  async def start_test(self, user, test_id: int):
    async with async_session.begin() as db:
      if not await test_dao.is_active(db, test_id):
          raise TestNoActiveException

      if await test_dao.was_passed(db, user.id, test_id):
          raise TestAlreadyPassedException
      test = await test_dao.get_test(db, test_id)
      for question in test.questions:
          correct_answer_count = 0
          choices = await choice_dao.find_all_with_filter(
            db, test_question_id=question.id
          )
          for option in choices:
            if option.is_correct:
                correct_answer_count += 1
                if correct_answer_count > 1:
                    question.multiple_answer = True
                    break
      return test

  async def finish_test(self, user, test_id: int, user_answer_ids: List[int]):
    async with async_session.begin() as db:
      if not await test_dao.is_active(db, test_id):
        raise TestNoActiveException

      if await test_dao.was_passed(db, user.id, test_id):
        raise TestAlreadyPassedException

      return await test_dao.add_result(db, user.id, test_id, user_answer_ids)
  
  async def get_tests_finished_at_month(self, user_id, date):
    async with async_session.begin() as db:
      return await test_dao.get_tests_finished_at_month(db, user_id, date)
    
  async def delete_test(self, test_id: int):
    async with async_session() as session:
      return await test_dao.delete_test(session, test_id)
    
  async def create_test(self, test: SCreateTest):
    async with async_session.begin() as db:
      return await test_dao.create_test(db, test)
    
  async def update_test(
    test_id: int,
    test: SUpdateTest,
  ):
    async with async_session.begin() as db:

      # проверяем, нет ли уже теста с таким же названием
      exist_test_with_name = await test_dao.find_one_or_none(db, name=test.name)
      if exist_test_with_name:
        if exist_test_with_name.id != test_id:
          raise TestNameAlreadyExistsException
          
      # проверка, если результаты теста уже есть, то выдаем exception
      # results = await test_dao.get_test_result(db, )

      updated_test = test.model_dump()
      existing_test = SUpdateTest.model_validate(
        await test_dao.get_test(db, test_id)
      ).model_dump()

      # # проверяем, есть ли изменения в тесте, если нет, то ничего не делаем
      if compare_dicts(existing_test, updated_test):
        return

      # # проверяем, есть ли изменения в вопросах и ответах теста
      has_changes_in_questions = not compare_dicts(
        {"questions": existing_test["questions"]},
        {"questions": updated_test["questions"]},
      )
      return await test_dao.update_test(
        db, test_id, updated_test, has_changes_in_questions
      )
  async def get_test_result(self, user_id, test_id):
    async with async_session.begin() as db:
      return await test_dao.get_test_result(db, user_id, test_id)
    
  async def get_test_list(
    self,
    user_id: str,
    offset: int = 0,
    limit: int = 10000,
  ):
    async with async_session.begin() as db:
      return await test_dao.get_test_list(db, user_id, offset, limit)
  
  async def get_test_results(
        self,
        date_from: date,
        date_to: date,
        date_order_by: str,
        order_by: bool,
        desc: date,
    ):
        async with async_session.begin() as db:

            def date_in_month(date, month):
                return date.year == month.year and date.month == month.month

            if date_order_by is None:
                date_order_by = date_from
            date_from_order_by = (
                date_from
                if date_in_month(date_from, date_order_by)
                else date_order_by.replace(day=1)
            )
            date_to_order_by = (
                date_to
                if date_in_month(date_to, date_order_by)
                else date_order_by.replace(
                    day=calendar.monthrange(date_order_by.year, date_order_by.month)[1]
                )
            )

            sort = []
            if not (order_by is None or order_by == "employee_name"):
                # sort = await TestDAO.get_test_results(
                #     date_from_order_by, date_to_order_by, order_by, desc
                # )
                sort = test_dao.get_test_results(
                    date_from_order_by, date_to_order_by, order_by, desc
                )

            names = []
            for s in sort:
                if s.employee_name not in names:
                    names.append((s.employee_name, s.employee_email, s.user_id))

            months = list(get_month_range(date_from, date_to))
            result = [
                {
                    "employee_name": name[0],
                    "employee_email": name[1],
                    "employee_id": name[2],
                    "rows": [
                        {"date": date, "points": None, "rank": None} for date in months
                    ],
                }
                for name in names
            ]
            for month in months:
                start = date_from if date_in_month(date_from, month) else month
                end = (
                    date_to
                    if date_in_month(date_to, month)
                    else month.replace(
                        day=calendar.monthrange(month.year, month.month)[1]
                    )
                )
                # test_res = await TestDAO.get_test_results(start, end)
                test_res = await test_dao.get_test_results(db, start, end)
                for res in test_res:
                    index = -1
                    for r in result:
                        if r["employee_name"] == res.employee_name:
                            index = result.index(r)
                            break
                    if index == -1:
                        data = {
                            "employee_name": res.employee_name,
                            "employee_email": res.employee_email,
                            "employee_id": res.user_id,
                            "rows": [
                                {"date": date, "points": None, "rank": None}
                                for date in months
                            ],
                        }
                        for r in data["rows"]:
                            if r["date"] == month:
                                r["points"] = res.points
                                r["rank"] = res.rank
                        result.append(data)

                    else:
                        for r in result[index]["rows"]:
                            if r["date"] == month:
                                r["points"] = res.points
                                r["rank"] = res.rank

            if order_by is None or order_by == "employee_name":
                result.sort(key=lambda x: x["employee_name"])

            return result

test_service: TestService = TestService()