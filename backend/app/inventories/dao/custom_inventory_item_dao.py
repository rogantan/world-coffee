from common.base_dao import BaseDao
from app.inventories.model.custom_inventory_item import CustomInventoryItem
from app.inventories.model.custom_inventory import CustomInventory
from core.db_postgres import AsyncSession
from sqlalchemy import select

class CustomInventoryItemDao(BaseDao[CustomInventoryItem]):
  async def get_items(self, db: AsyncSession, retail_store_id: str):
    query = (select(self.model)
    .join(CustomInventory, CustomInventory.id == self.model.custom_inventory_id)
    .where(CustomInventory.retail_store_id == retail_store_id).order_by(self.model.product_name))
    result = await db.execute(query)
    return result.scalars().all()

custom_inventory_item_dao: CustomInventoryItemDao = CustomInventoryItemDao(CustomInventoryItem)