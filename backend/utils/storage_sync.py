# backend/utils/storage_sync.py
from datetime import UTC, datetime
from app.admin.service.sync_service import sync_service
from app.admin.service.user_service import user_service
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
      async with get_session(login=settings.MS_LOGIN, password=settings.MS_PASSWORD) as ms_client:
        logger.info("Запуск синхронизации user")
        await user_service.storage_update(ms_client, up_time)
        logger.info("Синхронизация user завершена")

        logger.info("Запуск синхронизации store")
        #
        logger.info("Синхронизация store завершена")

        logger.info("Запуск синхронизации retail_store")
        #
        logger.info("Синхронизация retial_store завершена")

        logger.info("Запуск синхронизации inventory")
      await sync_service.update_sync(sync_id, Status.SUCCESS)
    except Exception as e:
      logger.error(e)
      await sync_service.update_sync(sync_id, Status.ERROR)
      

storage_sync = StorageSync()