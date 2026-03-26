from app.reports.dao.retail_store_dao import retail_store_dao
from core.db_postgres import async_session

class RetailStoreService:

    async def get_retail_stores(self):
        async with async_session() as session:
            result = await retail_store_dao.get_all(session, order_by="name")
            return result


retail_store_service: RetailStoreService = RetailStoreService()