from common.base_dao import BaseDao
from app.admin.model.sync import Synchronization
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

class SynchronizationDAO(BaseDao[Synchronization]):

    async def find_all(self, db: AsyncSession):
        query = select(self.model).where(self.model.start_time >= datetime.now() - timedelta(days=31)).order_by(self.model.start_time.desc())
        result = await db.execute(query)
        return result.scalars().all()
    


synchronization_dao: SynchronizationDAO = SynchronizationDAO(Synchronization)