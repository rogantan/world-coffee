from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from app.testing.service.test_service import test_service
from common.exceptions.error import TestNoActiveException, TestAlreadyPassedException, ForbiddenException
from typing import List
from datetime import datetime, date
from uuid import UUID
from app.testing.schema.test import STestInMonth, SCreateTest, STestWithQuestionsAndAnswers, SUpdateTest, STestResult, STestForList

router = APIRouter(
  prefix="/test/user",
  tags=["Тестирование просмотр"],
)

@router.get(
    "/results",
    response_model="",
    summary="123",
)
async def get_test_results(
  user: CurrentUserDep,
  # filter: TestFilter,
  date_from: date,
  date_to: date,
  date_order_by: datetime | None = None,
  order_by: str | None = None,
  desc: bool = False,
):
  """Получение списка результатов тестирования.
  Доступно пользователям с ролями: админ, старший продавец, продавец.
  Ожидается первое число месяца в date_from и date_order_by
  и последнее число в date_to.
  """
  # print(date_to)
  if user.role not in ["admin", "senior_salesman", "salesman", "accountant"]:
    raise ForbiddenException

  return await test_service.get_test_results(
    date_from, date_to, date_order_by, order_by, desc
  )


@router.get("/list", response_model=list[STestForList])
async def get_all_tests(user: CurrentUserDep):
  """Получение списка всех тестов.
  Результат сортируется по полю date_to в порядке убывания.
  Просмотр доступен пользователям с ролями: админ, старший продавец, продавец
  """

  if user.role in ["admin", "senior_salesman", "salesman"]:
    return await test_service.get_test_list(user.id)

  raise ForbiddenException


@router.get(
  "/{test_id}", 
  response_model=STestResult,
)
async def get_test(user: CurrentUserDep, test_id: int):
  """Получение полной информации о тесте с вопросами и ответами.
  Доступно пользователям с ролями: админ, старший продавец."""

  if user.role not in ["admin", "senior_salesman", "salesman"]:
    raise ForbiddenException

  return await test_service.get_test_result(user.id, test_id)