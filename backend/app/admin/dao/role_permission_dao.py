from common.base_dao import BaseDao
from app.admin.model.role_permission import RolePermission
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

class RolePermissionDAO(BaseDao[RolePermission]):
    
    async def get_permissions(self, db: AsyncSession, role_id: int):
        query = select(RolePermission).where
    


role_permission_dao: RolePermissionDAO = RolePermissionDAO(RolePermission)