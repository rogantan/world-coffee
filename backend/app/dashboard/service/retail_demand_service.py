from datetime import datetime
from common.exceptions.error import UnprocessableEntity
from common.my_storage import AsyncHttpClient
from core.db_postgres import async_session
from app.dashboard.dao.retail_demand_dao import retail_demand_dao

class RetailDemandService:
  async def storage_update(self, ms_client: AsyncHttpClient, up_time: datetime):
    async with async_session() as session:
      offset = 0
      size = 1
      while offset < size:
        params = {
          "expand": "agent,organization,positions",
          "filter": f"updated>={up_time}",
          "limit": 100,
          "offset": offset,
        }
        retail_demands = await ms_client.get(
          "entity/retaildemand", params=params
        )
        size = retail_demands.get("meta").get("size")
        retail_demands = retail_demands.get("rows", [])
        for retail_demand in retail_demands:
          exist_retail_demand = await retail_demand_dao.find_by_id(
            session, retail_demand.get("id")
          )
          if exist_retail_demand:
            await retail_demand_dao.update_entity(
              session, retail_demand
            )
          else:
            await retail_demand_dao.add_new_entity(session, retail_demand)
        offset += 100

  async def get_all(self, order_by, desc, date_from, date_to):
    async with async_session() as session:
      return await retail_demand_dao.get_all(session, order_by, desc, date_from, date_to)
      # try:
      #   return await retail_demand_dao.get_all(session, order_by, desc, date_from, date_to)
      # except:
      #   raise UnprocessableEntity

retail_demand_service: RetailDemandService = RetailDemandService()