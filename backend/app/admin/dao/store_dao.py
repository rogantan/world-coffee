from sqlalchemy import select
from app.reports.model.retail_store import RetailStore
from common.base_dao import BaseDao
from app.admin.model.store import Store
from core.db_postgres import AsyncSession
from utils.date_formatter import ms_date_to_datetime

class StoreDao(BaseDao[Store]):
  async def get_by_retail_store(self, db: AsyncSession, retail_store_id):
    query = (
      select(Store)
      .join(RetailStore, Store.id == RetailStore.store_id)
      .where(RetailStore.id == retail_store_id)
    )
    result = await db.execute(query)
    return result.scalars().first()

  async def add_new_entity(self, db: AsyncSession, entity):
    await self.add(
      db,
      id=entity.get("id", ""),
      name=entity.get("name", ""),
      archived=entity.get("archived", False),
      ms_updated=ms_date_to_datetime(entity.get("updated"))
    )
  
  async def update_entity(self, db: AsyncSession, entity):
    await self.update(
      db,
      entity.get("id", ""),
      name=entity.get("name", ""),
      archived=entity.get("archived"),
      ms_updated=ms_date_to_datetime(entity.get("updated"))
    )

  async def delete_entity(self, db: AsyncSession, entity_id):
    await self.update(db, entity_id, archived=True)

store_dao: StoreDao = StoreDao(Store)