from common.base_dao import BaseDao
from app.reports.model.retail_store import RetailStore
from core.db_postgres import AsyncSession
from sqlalchemy import select
from app.directories.model.salary import SalaryCondition

class RetailStoreDao(BaseDao[RetailStore]):
    
    async def get_retail_stores(self, db: AsyncSession):
        query = select(RetailStore.id, RetailStore.name, RetailStore.archived, SalaryCondition.salary_per_shift).join(SalaryCondition, RetailStore.id == SalaryCondition.retail_store_id)
        result = await db.execute(query)
        return result.mappings().all()

retail_store_dao: RetailStoreDao = RetailStoreDao(RetailStore)