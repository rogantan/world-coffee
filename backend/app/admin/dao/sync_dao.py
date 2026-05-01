from app.admin.schema.sync import SyncShema
from common.base_dao import BaseDao
from app.admin.model.sync import Synchronization
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.admin.enum.status import Status

class SynchronizationDAO(BaseDao[Synchronization]):

    async def find_all(self, db: AsyncSession):
        query = select(self.model).where(self.model.start_time >= datetime.now() - timedelta(days=31)).order_by(self.model.start_time.desc())
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create_sync(self, db: AsyncSession, start_time: datetime):
        return await self.add(db, start_time=start_time, status=Status.IN_PROGRESS)
    
    async def find_last_successful_update(self, db: AsyncSession) -> SyncShema:
        query = (
            select(self.model)
            .filter_by(status=Status.SUCCESS)
            .order_by(self.model.start_time.desc())
            .limit(1)
        )
        result = await db.execute(query)
        return result.scalars().one_or_none()

    


synchronization_dao: SynchronizationDAO = SynchronizationDAO(Synchronization)