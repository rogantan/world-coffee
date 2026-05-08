from app.inventories.dao.custom_inventory_dao import custom_inventory_dao
from app.inventories.dao.custom_inventory_item_dao import custom_inventory_item_dao
from app.reports.dao.retail_store_dao import retail_store_dao
from core.db_postgres import async_session


class CustomInventoryService:
  async def get_items(self, retail_store_name: str):
    async with async_session() as session:
      retail_store = await retail_store_dao.find_one_or_none(session, name=retail_store_name)
      print(retail_store.id)
      if retail_store is None:
        return
      return await custom_inventory_item_dao.get_items(session, retail_store.id)

custom_inventory_service: CustomInventoryService = CustomInventoryService()