from fastapi import APIRouter
from app.directories.service.salary_service import salary_service
from app.admin.dependens.auth import CurrentUserDep
from app.directories.schema.salary_schema import SalarySchema
from typing import List

router = APIRouter(prefix="/salary", tags=["Справочник. Оплата за смену"])

@router.get("", response_model=List[SalarySchema])
async def get_salary(user: CurrentUserDep):
  return await salary_service.get_salary()

@router.put("/{row_id}")
async def edit_salary(user: CurrentUserDep, row_id: int, salary):
  return await salary_service.edit_salary(row_id, salary)