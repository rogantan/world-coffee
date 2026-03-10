from core.db_postgres import async_session
from app.admin.dao.sync_dao import synchronization_dao

class SyncService:

    async def get_sync_data(self):
        async with async_session.begin() as session:
            result = await synchronization_dao.find_all(session)
            return result

sync_service: SyncService = SyncService()