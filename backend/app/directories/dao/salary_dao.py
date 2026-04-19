from app.directories.schema.salary_schema import SalarySchema
from common.base_dao import BaseDao
from app.directories.model.salary import SalaryCondition
from app.reports.model.retail_store import RetailStore
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

class SalaryConditionDao(BaseDao[SalaryCondition]):
  async def update_salary(self, db: AsyncSession, row_id: UUID, **new_salary: dict):
    query = update(SalaryCondition).where(SalaryCondition.retail_store_id == row_id).values(new_salary)
    result = await db.execute(query)
    await db.commit()
    return result

salary_dao: SalaryConditionDao = SalaryConditionDao(SalaryCondition)