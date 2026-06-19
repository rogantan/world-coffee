from common.base_dao import BaseDao
from app.inventories.model.custom_inventory import CustomInventory
from app.inventories.model.custom_inventory_item import CustomInventoryItem
from core.db_postgres import AsyncSession
from common.my_storage import AsyncHttpClient, get_session
from sqlalchemy import select
from app.admin.dao.store_dao import store_dao
from app.inventories.dao.custom_inventory_item_dao import custom_inventory_item_dao
from core.config import settings

class CustomInventoryDao(BaseDao[CustomInventory]):

  def get_store(self, store_id):
    return {
      "meta": {
        "href": f"https://api.moysklad.ru/api/remap/1.2/entity/store/{store_id}",
        "mediaType": "application/json",
        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/store/metadata",
        "type": "store",
      }
    }
  
  def get_organization(self):
    return {
      "meta": {
        "href": "https://api.moysklad.ru/api/remap/1.2/entity/organization/b970c01a-86ed-11f0-0a80-15b3003c1d1f",
        "mediaType": "application/json",
        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/organization/metadata",
        "type": "organization",
      }
    }
  
  def get_positions(self, items):
    positions = []

    for item in items:
      positions.append(
        {
          "assortment": {"meta": item.meta},
          "price": item.price * 100,
          "quantity": item.closing_balance,
        }
      )

    return positions
  
  async def unload_inventory_to_ms(self, db: AsyncSession, retail_store_id: str, user):
    store_id = (await store_dao.get_by_retail_store(db, retail_store_id)).id
    items = await custom_inventory_item_dao.get_items(db, retail_store_id)
    user_id = user.id
    if user.role == 'admin':
      user_id = "b962993a-86ed-11f0-0a80-15b3003c1cd4"
    owner = {
      "meta": {
        "href": f"https://api.moysklad.ru/api/remap/1.2/entity/employee/{user_id}",
        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/employee/metadata",
        "type": "employee",
        "mediaType": "application/json",
      }
    }
    data = {
      "organization": self.get_organization(),
      "store": self.get_store(store_id),
      "positions": self.get_positions(items),
      "description": user.name,
      "owner": owner
    }

    async with get_session(login=settings.MS_LOGIN, password=settings.MS_PASSWORD) as ms_client:
      response = await ms_client.post("entity/inventory", data)
      inventory_meta = response.get("meta")
      inventory_id = inventory_meta["href"].split("/")[-1]
      # делаем пересчет расчетного остатка в инвентаризации
      
      # enter_data = {
      #   "store": self.get_store(store_id),
      #   "organization": self.get_organization(),
      #   # "positions": self.get_positions(items),
      #   "inventory": {
      #     "meta": {
      #       "href": f"https://api.moysklad.ru/api/remap/1.2/entity/inventory/{inventory_id}",
      #       "mediaType": "application/json",
      #       "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/inventory/metadata",
      #       "type": "inventory",
      #     }
      #   }
      # }
      # status1 = await ms_client.post("entity/enter", enter_data)
      # print(status1)
      # status2 = await ms_client.post("entity/loss", enter_data)
      # print(status2)
      await ms_client.put(f"rpc/inventory/{inventory_id}/recalcCalculatedQuantity")
  


custom_inventory_dao: CustomInventoryDao = CustomInventoryDao(CustomInventory)