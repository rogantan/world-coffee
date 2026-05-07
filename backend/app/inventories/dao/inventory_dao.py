from datetime import datetime, date, timedelta

from sqlalchemy import String, desc, func, literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.inventories.model.inventory import Inventory
from app.admin.model.user import User
from app.admin.model.store import Store
from app.reports.model.retail_store import RetailStore
from common.base_dao import BaseDao
from utils.date_formatter import ms_date_to_datetime
from app.admin.dao.user_dao import user_dao

class InventoryDao(BaseDao[Inventory]):
  # model = Inventory

  # @classmethod
  async def get_all(
    self,
    db: AsyncSession,
    date_from: date,
    date_to: date,
    order_by: str,
    order_desc: bool,
  ):
    query = (
      select(
        self.model.id.label("uuid"),
        self.model.name,
        self.model.moment.label("date"),
        self.model.moment.label("month"),
        self.model.uuid_href.label("link"),
        User.name.label("salesman_name"),
        RetailStore.name.label("retail_store_name"),
        (-1 * self.model.negative_correction_sum).label("loss_sum"),
        self.model.positive_correction_sum.label("enter_sum"),
        self.model.retention_sum,
      )
      .join(Store, self.model.store_id == Store.id)
      .join(RetailStore, Store.id == RetailStore.store_id)
      .join(User, self.model.salesman_id == User.id)
      .where(self.model.moment >= date_from)
      .where(self.model.moment < date_to + timedelta(days=1))
      .where(RetailStore.name != "Старший продавец")
  )
    result = await db.execute(query)

    return result.mappings().all()

  def get_id_from_object(self, entity: dict, odject_name: str) -> str | None:
    """Получение id из href ссылки"""
    obj = entity.get(odject_name)
    if not obj:
      return

    href = obj.get("meta", {}).get("href")
    return href.split("/")[-1]

  def get_name_from_object(self, entity: dict, odject_name: str) -> str | None:
    """Получение имени из json объекта МС"""
    obj = entity.get(odject_name)
    if not obj:
      return

    return obj.get("name")

  async def add_new_entity(
    self,
    db,
    entity,
  ):
    """Создание новой записи"""

    positive_correction_sum = 0
    negative_correction_sum = 0

    if enters := entity.get("enters"):
      positive_correction_sum = (
        sum(enter.get("sum", 0) for enter in enters) / 100
      )

    if losses := entity.get("losses"):
      negative_correction_sum = -(
        sum(loss.get("sum", 0) for loss in losses) / 100
      )

    salesman = await user_dao.find_one_or_none(db, name=entity.get("description", ""))
    
    if salesman is None:
      return
    print(salesman.id)
    retention_sum = (negative_correction_sum + positive_correction_sum) * -0.6
    retention_sum = max(retention_sum, 0)
    await self.add(
      db,
      ms_id=entity.get("id"),
      store_id=self.get_id_from_object(entity, "store"),
      salesman_id=salesman.id,
      positive_correction_sum=positive_correction_sum,
      negative_correction_sum=negative_correction_sum,
      retention_sum=retention_sum,
      name=entity.get("name"),
      uuid_href=entity.get("meta").get("uuidHref"),
      moment=ms_date_to_datetime(entity.get("moment")),
      ms_updated=ms_date_to_datetime(entity.get("updated")),
    )

  async def update_entity(self, db, entity):
    """Обновление записи"""
    inventories = await self.find_all_with_filter(db, ms_id=entity.get("id"))
    for inventory in inventories:
      await self.delete(db, inventory.id)
      
    await self.add_new_entity(
      db=db,
      entity=entity,
    )

  async def get_salesman_id(self, entity, attribute_name: str):
    """Получаем ID продавца из атрибута Продавец"""

    for attribute in entity.get("attributes", {}):
      if attribute.get("name") == attribute_name:
        try:
          return attribute["value"]["meta"]["href"].split("/")[-1]
        except KeyError:
          return None

    return None

  async def get_salesman_ids(self, entity: dict):

    salesman_ids = []
    for name in ["Продавец 1", "Продавец 2"]:
      salesman_id = await self.get_salesman_id(entity, name)
      if salesman_id:
        salesman_ids.append(salesman_id)

    return salesman_ids

  async def entity_in_db(self, db, entity_id: str) -> bool:
    """Проверка наличия записи в БД"""
    return await self.find_all_with_filter(db, ms_id=entity_id)

  async def delete_entity(self, db, entity_id: str) -> None:
    inventories = await self.find_all_with_filter(db, ms_id=entity_id)
    for inventory in inventories:
      await self.delete(db, inventory.id)

inventory_dao: InventoryDao = InventoryDao(Inventory)
