from app.admin.model.user import User
from common.base_dao import BaseDao
from app.admin.model.role import Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta

class RoleDAO(BaseDao[Role]):
    async def update_role(self, db: AsyncSession, username: str, role: str):
        new_role = await self.find_one_or_more(db, name=role)
        print(new_role)
        print(f"'{role}'")
        new_role_id = new_role.id
        query = update(User).where(User.uid == username).values(role_id=new_role_id)
        result = await db.execute(query)
        await db.commit()
        return result

    


role_dao: RoleDAO = RoleDAO(Role)