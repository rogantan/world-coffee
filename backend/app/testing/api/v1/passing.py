from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from app.testing.service.test_service import test_service
from common.exceptions.error import TestNoActiveException, TestAlreadyPassedException, ForbiddenException
from typing import List

router = APIRouter(
  prefix="/test/passing",
  tags=["Тестирование прохождение"],
)

@router.get("/{test_id}/preview")
async def get_test_preview(user: CurrentUserDep, test_id: int):
  if user.role not in ["admin", "salesman"]:
    raise ForbiddenException
  if await test_service.is_test_active(test_id) == False:
    raise TestNoActiveException
  if await test_service.is_test_passed(user, test_id):
    raise TestAlreadyPassedException
  return await test_service.get_test(test_id)

@router.get("/{test_id}/starting")
async def start_test(user: CurrentUserDep, test_id: int):
  if user.role not in ["admin", "salesman"]:
    raise ForbiddenException
  return await test_service.start_test(user, test_id)

@router.put("/{test_id}/finishing")
async def finish_test(user: CurrentUserDep, test_id: int, answer_options_ids: List[int]):
  if user.role not in ["admin", "salesman", "senior_salesman"]:
    raise ForbiddenException
  return await test_service.finish_test(user, test_id, answer_options_ids)

@router.get("/{test_id}/result")
async def get_test_result(user: CurrentUserDep, test_id: int):
  if user.role not in ["admin", "salesman"]:
    raise ForbiddenException
  return await test_service.get_test_result(user, test_id)
