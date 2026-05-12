from app.inventories.dao.custom_inventory_dao import custom_inventory_dao
from app.inventories.dao.custom_inventory_item_dao import custom_inventory_item_dao
from app.reports.dao.retail_store_dao import retail_store_dao
from common.exceptions.error import ActualBalanceLessThanSaleSumException, CustomInventoryItemNotFoundException
from core.db_postgres import async_session
from app.inventories.schema.inventory import SInventoryEdit
from app.reports.dao.retail_store_dao import retail_store_dao


class CustomInventoryService:
  async def get_items(self, retail_store_name: str):
    async with async_session() as session:
      retail_store = await retail_store_dao.find_one_or_none(session, name=retail_store_name)
      print(retail_store.id)
      if retail_store is None:
        return
      return await custom_inventory_item_dao.get_items(session, retail_store.id)
    
  async def edit_item(self, item_id: int, data: SInventoryEdit):
    async with async_session() as session:
      item = await custom_inventory_item_dao.find_by_id(session, item_id)
      
      if not item:
        raise CustomInventoryItemNotFoundException
      print(item.id)
      data = data.model_dump()
      actual_balance = (
        data["actual_balance"]
        if (data.get("actual_balance") is not None)
        else item.actual_balance
      )
      sales = data["sales"] if (data.get("sales") is not None) else item.sales

      if actual_balance < sales:
        raise ActualBalanceLessThanSaleSumException
      result = await custom_inventory_item_dao.edit_item(session, item_id, data)
      return result
    
  async def clear_items(self, report_title: str):
    async with async_session() as session:
      retail_store = await retail_store_dao.find_one_or_none(session, name=report_title)
      if not retail_store:
        return
      return await custom_inventory_item_dao.clear_items(session, retail_store.id)
    
  async def unload_inventory(self, report_title: str, user):
    async with async_session() as session:
      retail_store = await retail_store_dao.find_one_or_none(session, name=report_title)
      if not retail_store:
        return
      await custom_inventory_dao.unload_inventory_to_ms(session, retail_store.id, user)


custom_inventory_service: CustomInventoryService = CustomInventoryService()