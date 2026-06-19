from core.logger import logger
from core.config import settings
from common.my_storage import AsyncHttpClient, get_session
from typing import List
from core.db_postgres import async_session
from app.reports.dao.retail_store_dao import retail_store_dao
from app.inventories.model.custom_inventory import CustomInventory
from app.inventories.model.custom_inventory_item import CustomInventoryItem
from sqlalchemy import select


class InventorySync:
  async def start_update(self):
    async with get_session(login=settings.MS_LOGIN, password=settings.MS_PASSWORD) as ms_client:
      products = await ms_client.get("entity/product")
      products = products.get("rows", [])
      logger.info(len(products))
      await self.insert_all(products)

  async def insert_all(self, products: List):
    async with async_session() as session:
      inventories = (await session.execute(select(CustomInventory))).scalars().all()
      for inventory in inventories:
        await session.delete(inventory)
      await session.commit()

      retail_stores = await retail_store_dao.get_retail_stores(session)
      try:
        for retail_store in retail_stores:
          inventory = CustomInventory(retail_store_id=retail_store.id)
          session.add(inventory)
          await session.flush()
          for product in products:
            item = CustomInventoryItem(
              custom_inventory_id=inventory.id,
              product_name=product.get("name", ""),
              price=self.get_price(product),
              meta=product.get("meta")
            )
            session.add(item)
          await session.commit()
      except Exception as e:
        await session.rollback()
        logger.error(e)
        raise e
      
  def get_price(self, product):
    sale_prices = product.get("salePrices", [])
    for price in sale_prices:
      if price.get("priceType", {}).get("name") == "Цена продажи":
        return price["value"] / 100
    return 0


inventory_sync: InventorySync = InventorySync()