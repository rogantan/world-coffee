from common.base_dao import BaseDao
from app.directories.model.salary import SalaryCondition
from app.reports.model.retail_store import RetailStore
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class SalaryConditionDao(BaseDao[SalaryCondition]):
  async def get_all_salary(self, db: AsyncSession):
    query = select(SalaryCondition.id, RetailStore.name.label("retail_store_name"), SalaryCondition.salary_per_shift).join(RetailStore, RetailStore.id == SalaryCondition.retail_store_id)
    result = await db.execute(query)
    return result.mappings().all()

salary_dao: SalaryConditionDao = SalaryConditionDao(SalaryCondition)