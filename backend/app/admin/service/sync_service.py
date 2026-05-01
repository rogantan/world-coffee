from datetime import UTC, datetime
from core.db_postgres import async_session
from app.admin.dao.sync_dao import synchronization_dao
from app.admin.enum.status import Status

class SyncService:

    async def get_sync_data(self):
        async with async_session.begin() as session:
            result = await synchronization_dao.find_all(session)
            return result
        
    async def create_sync(self, start_time: datetime):
        async with async_session.begin() as db:
            sync = await synchronization_dao.create_sync(
                db,
                start_time=start_time,
            )
            return sync.id
        
    async def update_sync(self, synch_id: int, status: Status):
        async with async_session.begin() as session:
            return await synchronization_dao.update(session, synch_id, status=status, finish_time=datetime.now(UTC).replace(tzinfo=None))

sync_service: SyncService = SyncService()