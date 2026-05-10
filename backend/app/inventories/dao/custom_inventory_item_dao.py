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
  
  async def edit_item(self, db: AsyncSession, item_id: int, data: dict):
    result = await self.update(db, item_id, **data)
    return result
  
  async def clear_items(self, db: AsyncSession, retail_store_id: str):
    data = {"actual_balance": 0, "sales": 0}
    query = select(self.model.id).join(CustomInventory, self.model.custom_inventory_id == CustomInventory.id).where(CustomInventory.retail_store_id == retail_store_id)
    result = await db.execute(query)
    item_ids = [row[0] for row in result.fetchall()]
    updated_items = []
    for item_id in item_ids:
      item = await self.update(db, item_id, **data)
      updated_items.append(item)
    return updated_items
    


custom_inventory_item_dao: CustomInventoryItemDao = CustomInventoryItemDao(CustomInventoryItem)