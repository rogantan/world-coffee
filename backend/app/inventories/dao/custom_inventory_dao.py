from common.base_dao import BaseDao
from app.inventories.model.custom_inventory import CustomInventory
from app.inventories.model.custom_inventory_item import CustomInventoryItem
from core.db_postgres import AsyncSession
from sqlalchemy import select

class CustomInventoryDao(BaseDao[CustomInventory]):
  
  pass
  


custom_inventory_dao: CustomInventoryDao = CustomInventoryDao(CustomInventory)