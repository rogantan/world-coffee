from common.base_dao import BaseDao
from app.admin.model.role_permission import RolePermission
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

class RolePermissionDAO(BaseDao[RolePermission]):
    
    async def get_permissions(self, db: AsyncSession, role_id: int):
        query = select(RolePermission).where(RolePermission.role_id == role_id)
        result = await db.execute(query)
        return result.scalars().all()
    


role_permission_dao: RolePermissionDAO = RolePermissionDAO(RolePermission)