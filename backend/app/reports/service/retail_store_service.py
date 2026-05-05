from app.reports.dao.retail_store_dao import retail_store_dao
from app.directories.dao.salary_dao import salary_dao
from core.db_postgres import async_session
from common.my_storage import AsyncHttpClient
from datetime import datetime

class RetailStoreService:

    async def get_retail_stores_with_salary(self):
        async with async_session() as session:
            result = await retail_store_dao.get_retail_stores(session)
            return result
        
    async def storage_update(self, ms_client: AsyncHttpClient, up_time: datetime):
        params = {"filter": f"updated>={up_time}"}
        retail_stores = await ms_client.get(f"entity/retailstore", params=params)
        retail_stores = retail_stores.get("rows", [])

        async with async_session() as session:
            for retail_store in retail_stores:
                exist_retail_store = await retail_store_dao.find_by_id(session, retail_store.get("id"))
                if exist_retail_store:
                    await retail_store_dao.update_entity(session, retail_store)
                else:
                    await retail_store_dao.add_new_entity(session, retail_store)
                    await salary_dao.add(session, retail_store_id=retail_store.get("id"), salary_per_shift=1000)


retail_store_service: RetailStoreService = RetailStoreService()