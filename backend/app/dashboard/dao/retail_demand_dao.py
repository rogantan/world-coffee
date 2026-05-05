from datetime import timedelta, date
from sqlalchemy import desc, func, select, update
from app.admin.model.user import User
from app.reports.model.retail_store import RetailStore
from utils.date_formatter import ms_date_to_datetime
from common.base_dao import BaseDao
from app.dashboard.model.retail_demand import RetailDemand
from app.admin.dao.user_dao import user_dao
from core.db_postgres import AsyncSession

class RetailDemandDao(BaseDao[RetailDemand]):

  async def get_all(
    self,
    db: AsyncSession,
    order_by: str,
    has_desc: bool,
    date_from: date,
    date_to: date,
    ):
    """Получение всех записей"""
    demand_in_period = (
      select(self.model)
      .filter(
        (self.model.moment >= date_from)
        & (self.model.moment < date_to + timedelta(days=1))
        & (self.model.applicable == True)
      )
      .subquery()
    )

    query = (
      select(
        demand_in_period.c.id,
        demand_in_period.c.name,
        func.to_char(demand_in_period.c.moment, "dd-mm-yyyy").label("moment"),
        RetailStore.name.label("retail_store_name"),
        demand_in_period.c.agent_name,
        demand_in_period.c.cash_sum,
        demand_in_period.c.no_cash_sum,
        demand_in_period.c.qr_sum,
        demand_in_period.c.sum,
        demand_in_period.c.discounts,
        User.name.label("owner_name"),
      )
      .outerjoin(
        RetailStore,
        demand_in_period.c.retail_store_id == RetailStore.id,
      )
      .outerjoin(
        User,
        demand_in_period.c.owner_id == User.id,
      )
    )

    if order_by:
      query = query.order_by(desc(order_by) if has_desc else order_by)
    else:
      query = query.order_by(demand_in_period.c.moment.desc())
    results = await db.execute(query)
    return results.mappings().all()

  def get_name_from_object(self, entity: dict, odject_name: str) -> str | None:
    obj = entity.get(odject_name)
    if not obj:
      return

    return obj.get("name")
  
  def get_id_from_object(self, entity: dict, odject_name: str) -> str | None:
    obj = entity.get(odject_name)
    if not obj:
      return
    href = obj.get("meta", {}).get("href")
    return href.split("/")[-1]
  
  async def add_new_entity(self, db: AsyncSession, entity):
    senior_salesman = await user_dao.get_senior_salesman(db)
    senior_salesman_id = senior_salesman.id if senior_salesman else None
    
    new_demand = RetailDemand(
      id=entity.get("id"),
      agent_name=self.get_name_from_object(entity, "agent"),
      retail_store_id=self.get_id_from_object(entity, "retailStore"),
      owner_id=self.get_id_from_object(entity, "owner"),
      senior_salesman_id=senior_salesman_id,
      applicable=entity.get("applicable"),
      name=entity.get("name"),
      cash_sum=entity.get("cashSum") / 100,
      no_cash_sum=entity.get("noCashSum") / 100,
      payed_sum=entity.get("payedSum") / 100,
      qr_sum=entity.get("qrSum") / 100,
      sum=entity.get("sum") / 100,
      discounts=self.get_discounts(entity.get("positions", {})),
      moment=ms_date_to_datetime(entity.get("moment")),
      ms_created=ms_date_to_datetime(entity.get("created")),
      ms_updated=ms_date_to_datetime(entity.get("updated"))
    )
    db.add(new_demand)
    await db.commit()

  async def update_entity(self, db: AsyncSession, entity):
    senior_salesman = await user_dao.get_senior_salesman(db)
    senior_salesman_id = senior_salesman.id if senior_salesman else None

    stmt = update(RetailDemand).where(RetailDemand.id == entity.get("id")).values(
      agent_name=self.get_name_from_object(entity, "agent"),
      retail_store_id=self.get_id_from_object(entity, "retailStore"),
      owner_id=self.get_id_from_object(entity, "owner"),
      senior_salesman_id=senior_salesman_id,
      applicable=entity.get("applicable"),
      name=entity.get("name"),
      cash_sum=entity.get("cashSum") / 100,
      no_cash_sum=entity.get("noCashSum") / 100,
      payed_sum=entity.get("payedSum") / 100,
      qr_sum=entity.get("qrSum") / 100,
      sum=entity.get("sum") / 100,
      discounts=self.get_discounts(entity.get("positions", {})),
      moment=ms_date_to_datetime(entity.get("moment")),
      ms_created=ms_date_to_datetime(entity.get("created")),
      ms_updated=ms_date_to_datetime(entity.get("updated"))
    )
    await db.execute(stmt)
    await db.commit()
  
  def get_discounts(self, positions: dict):
    """Получить сумму скидок"""
    try:
      discounts = 0
      for position in positions.get("rows", []):
        discounts += (
          position["price"]
          * position["discount"]
          * position["quantity"]
          / 10000
        )
      return round(discounts, 2)
    except:
      return 0

retail_demand_dao: RetailDemandDao = RetailDemandDao(RetailDemand)