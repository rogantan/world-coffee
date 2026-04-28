from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from app.testing.service.test_service import test_service
from common.exceptions.error import TestNoActiveException, TestAlreadyPassedException, ForbiddenException
from typing import List
from datetime import datetime, date
from uuid import UUID
from app.testing.schema.test import STestInMonth, SCreateTest, STestWithQuestionsAndAnswers, SUpdateTest, STestResult

router = APIRouter(
  prefix="/test/admin",
  tags=["Тестирование управление"],
)

@router.get("/tests_in_month", response_model=List[STestInMonth])
async def get_tests_in_month(date: date, user_id: UUID, user: CurrentUserDep):
  """Получение списка тестов за определенный месяц."""

  if user.role not in ["admin", "senior_salesman"]:
    raise ForbiddenException

  return await test_service.get_tests_finished_at_month(user_id, date)

@router.post("/create")
async def create_test(test: SCreateTest, user: CurrentUserDep):
  """Создание нового теста.
  Доступно пользователям с ролями: админ, старший продавец.
  Должны быть хотя бы один вопрос,
  хотя бы один вариант ответа и хотя бы один верный.
  Название теста должно быть уникальным
  """

  if user.role not in ["admin", "senior_salesman"]:
    raise ForbiddenException

  return await test_service.create_test(test)

@router.get("/{test_id}", response_model=STestWithQuestionsAndAnswers)
async def get_test(user: CurrentUserDep, test_id: int):
  """Получение полной информации о тесте с вопросами и ответами.
  Доступно пользователям с ролями: админ, старший продавец."""

  if user.role not in ["admin", "senior_salesman"]:
    raise ForbiddenException

  return await test_service.get_test(test_id)


@router.put("/{test_id}/edit", summary="")
async def edit_test(user: CurrentUserDep, test_id: int, test: SUpdateTest):
  """Редактирование теста.
  Доступно пользователям с ролями: админ, старший продавец.
  Должен быть хотя бы один вопрос,
  хотя бы один вариант ответа и хотя бы один верный.
  Название теста должно быть уникальным"""

  if user.role not in ["admin", "senior_salesman"]:
    raise ForbiddenException

  return await test_service.update_test(test_id, test)


@router.delete("/{test_id}")
async def delete_test(user: CurrentUserDep, test_id: int):
  """Удаление теста.
  Доступно пользователям с ролями: админ, старший продавец."""

  if user.role not in ["admin", "senior_salesman"]:
    raise ForbiddenException

  return await test_service.delete_test(test_id)

@router.get("/{test_id}/result/{user_id}", response_model=STestResult)
async def get_test_result_for_admin(user: CurrentUserDep, test_id: int, user_id: UUID):
  """Получение результатов прохождения теста.
  Доступно пользователям с ролями: Админ и старший продавец
  """

  if user.role not in ["admin", "senior_salesman"]:
    raise ForbiddenException

  return await test_service.get_test_result(user_id, test_id)

