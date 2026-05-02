from app.admin.dao.store_dao import store_dao
from common.my_storage import AsyncHttpClient
from datetime import datetime
from core.db_postgres import async_session

class StoreService:
  
  async def storage_update(self, ms_client: AsyncHttpClient, up_time: datetime):
    params = {"filter": f"updated>={up_time}"}
    stores = await ms_client.get(f"entity/store", params=params)
    stores = stores.get("rows", [])

    async with async_session() as session:
      for store in stores:
        exist_store = await store_dao.find_by_id(session, store.get("id"))
        if exist_store:
          await store_dao.update_entity(session, store)
        else:
          await store_dao.add_new_entity(session, store)


store_service: StoreService = StoreService()