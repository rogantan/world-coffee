# backend/utils/storage_sync.py
from datetime import UTC, datetime
from app.admin.service.sync_service import sync_service
from common.my_storage import get_session
from core.config import settings
from app.admin.enum.status import Status

class StorageSync:
  async def start_synchronization(self):
    sync_id = await sync_service.create_sync(datetime.now(UTC).replace(tzinfo=None))

    async with get_session(login=settings.MS_LOGIN, password=settings.MS_PASSWORD) as ms_client:
      a = 1
      if a == 1:
        await sync_service.update_sync(sync_id, Status.SUCCESS)
      else:
        await sync_service.update_sync(sync_id, Status.ERROR)

storage_sync = StorageSync()