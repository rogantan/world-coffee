from common.base_dao import BaseDao
from app.admin.model.store import Store
from core.db_postgres import AsyncSession

class StoreDao(BaseDao[Store]):
  pass

store_dao: StoreDao = StoreDao(Store)