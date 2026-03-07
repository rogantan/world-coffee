from app.admin.model.permission import Permission
from app.reports.model.report import Report
from common.base_dao import BaseDao
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app.admin.model.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDAO(BaseDao[User]):
    async def get(self, username: str, db: AsyncSession):
        query = select(User).where(User.uid == username).options(joinedload(User.salary_increase))
        user = await db.execute(query)
        return user.scalars().first()
    
    async def set_password_hash(self, db: AsyncSession, user_id, password):
        password_hash = pwd_context.hash(password)
        await self.update(db, user_id, hash_password=password_hash, registered=True)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def user_permissions(self, db: AsyncSession, user_id: str):
        query = (select(Permission.mode, Report.display_name, Report.title)
        .where(Permission.user_id == user_id).join(Report, Permission.report_id == Report.id))
        result = await db.execute(query)
        return result.mappings().all()
    
    async def get_user(self, db: AsyncSession, username: str):
        user = await self.select_one(db, uid=username)
        return user
    
user_dao: UserDAO = UserDAO(User)