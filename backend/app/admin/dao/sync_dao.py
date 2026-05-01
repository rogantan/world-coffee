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

    


synchronization_dao: SynchronizationDAO = SynchronizationDAO(Synchronization)