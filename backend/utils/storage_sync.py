# backend/utils/storage_sync.py
from datetime import UTC, datetime
from app.admin.service.sync_service import sync_service
from app.admin.service.user_service import user_service
from app.admin.service.store_service import store_service
from app.reports.service.retail_store_service import retail_store_service
from app.dashboard.service.retail_demand_service import retail_demand_service
from app.inventories.service.inventory_service import inventory_service
from common.my_storage import get_session
from core.config import settings
from app.admin.enum.status import Status
from core.logger import logger

class StorageSync:
  async def start_synchronization(self):

    sync_id = await sync_service.create_sync(datetime.now(UTC).replace(tzinfo=None))
    logger.info("Запуск синхоронизации")

    try:
      up_time = await sync_service.find_last_successful_update()
      #up_time = datetime(year=2025, month=9, day=1)
      async with get_session(login=settings.MS_LOGIN, password=settings.MS_PASSWORD) as ms_client:
        logger.info("Запуск синхронизации user")
        await user_service.storage_update(ms_client, up_time)
        logger.info("Синхронизация user завершена")

        logger.info("Запуск синхронизации store")
        await store_service.storage_update(ms_client, up_time)
        logger.info("Синхронизация store завершена")

        logger.info("Запуск синхронизации retail_store")
        await retail_store_service.storage_update(ms_client, up_time)
        logger.info("Синхронизация retial_store завершена")

        logger.info("Запуск синхронизации inventory")
        await inventory_service.storage_update(ms_client, up_time)
        logger.info("Синхронизации inventory завершена")

        logger.info("Запуск синхронизации retail_demand")
        await retail_demand_service.storage_update(ms_client, up_time)
        logger.info("Синхронизация retail_demand завершена")
        
      await sync_service.update_sync(sync_id, Status.SUCCESS)
    except Exception as e:
      logger.error(e)
      await sync_service.update_sync(sync_id, Status.ERROR)
      

storage_sync = StorageSync()