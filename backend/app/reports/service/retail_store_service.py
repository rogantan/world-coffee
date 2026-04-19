from app.reports.dao.retail_store_dao import retail_store_dao
from core.db_postgres import async_session

class RetailStoreService:

    async def get_retail_stores_with_salary(self):
        async with async_session() as session:
            result = await retail_store_dao.get_retail_stores(session)
            return result


retail_store_service: RetailStoreService = RetailStoreService()