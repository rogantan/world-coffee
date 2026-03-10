from common.base_dao import BaseDao
from app.admin.model.role import Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

class RoleDAO(BaseDao[Role]):
    pass

    


role_dao: RoleDAO = RoleDAO(Role)