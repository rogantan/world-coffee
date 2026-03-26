from common.base_dao import BaseDao
from app.reports.model.retail_store import RetailStore


class RetailStoreDao(BaseDao[RetailStore]):
    pass

retail_store_dao: RetailStoreDao = RetailStoreDao(RetailStore)