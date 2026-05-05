from pprint import pprint

from core.db_postgres import async_session
from app.inventories.dao.inventory_dao import inventory_dao
from datetime import date, datetime, timedelta
from common.my_storage import AsyncHttpClient
class InventoryService:

  async def get_all(self, date_from: date, date_to: date, order_by: str, order_desc: bool):
    async with async_session() as session:
      return await inventory_dao.get_all(session, date_from, date_to, order_by, order_desc)
    
  async def storage_update(self, ms_client: AsyncHttpClient, up_time: datetime):
    offset = 0
    size = 1
    while offset < size:
      params = {
        "filter": f"updated>={(datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')}",
        "expand": "enters, losses",
        "limit": 100,
        "offset": offset,
      }
      inventories = await ms_client.get(f"entity/inventory", params=params)
      size = inventories.get("meta").get("size")
      inventories = inventories.get("rows")
      pprint(inventories)
      async with async_session() as db:
        for inventory in inventories:
          exsist_inventory = await inventory_dao.find_all_with_filter(
            db,
            ms_id=inventory.get("id"),
          )

          if len(exsist_inventory) == 0:
            pprint(1)
            await inventory_dao.add_new_entity(db, inventory)
          else:
            pprint(2)
            await inventory_dao.update_entity(db, inventory)
                    
        offset += 100
    

inventory_service: InventoryService = InventoryService()