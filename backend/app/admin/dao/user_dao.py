from app.admin.model.user_permission import UserPermission
from app.reports.model.report import Report
from app.admin.model.role import Role
from common.base_dao import BaseDao
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, update
from app.admin.model.user import User
from app.admin.enum.permission_mode import PermissionMode
from app.admin.schema.user import UserRoleSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDAO(BaseDao[User]):
    async def get(self, username: str, db: AsyncSession):
        query = select(User).where(User.uid == username).options(joinedload(User.salary_increase), joinedload(User.role))
        user = await db.execute(query)
        return user.scalars().first()
    
    async def get_users(self, db: AsyncSession):
        query = select(User).options(joinedload(User.salary_increase), joinedload(User.role))
        result = await db.execute(query)
        return result.unique().scalars().all()
    
    async def set_password_hash(self, db: AsyncSession, user_id, password):
        password_hash = pwd_context.hash(password)
        await self.update(db, user_id, hash_password=password_hash, registered=True)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def user_permissions(self, db: AsyncSession, user_id: str):
        query = (select(UserPermission.mode, Report.display_name, Report.title)
        .where(UserPermission.user_id == user_id).join(Report, UserPermission.report_id == Report.id))
        result = await db.execute(query)
        return result.mappings().all()
    
    async def get_user(self, db: AsyncSession, username: str):
        query = (select(User)
            .options(selectinload(User.role))
            .where(User.uid == username))
        result = await db.execute(query)
        return result.scalar()
    
    async def get_role(self, db: AsyncSession, username: str):
        query = select(Role.name).join(User.role).where(User.uid == username)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def reset_password(self, db: AsyncSession, username: str):
        query = update(User).where(User.uid == username).values(hash_password = "1", registered = False)
        result = await db.execute(query)
        await db.commit()
        return result
    
    # async def is_role_exist(self, db: AsyncSession, role: UserRoleSchema):
    #     query = select(Role).where(Role.name == role.role)
    #     result = await db.execute(query)
    #     return result.scalars().first()

    async def reset_permissions(self, db: AsyncSession, username: str):
        query = select(UserPermission.id).where(User.uid == username).join(UserPermission.user_id == User.id)
        result = await db.execute(query)
        user_permissions = result.mappings().all()
        if user_permissions:
            try:
                for permission in user_permissions:
                    query_update = update(UserPermission).where(UserPermission.id == permission["id"]).values(mode=PermissionMode.HIDDEN)
                    db.execute(query_update)
            except Exception as e:
                await db.rollback()
                return None
            await db.commit()
        else:
            return None

    async def update_role(self, db: AsyncSession, username: str, role: str):
        new_role = self.select_one(db, name=role)
        new_role_id = new_role["id"]
        query = update(User).where(User.uid == username).values(role_id=new_role_id)
        result = await db.execute(query)
        await db.commit()
        return result
    
    async def change_permissions(self, db: AsyncSession, username: str, report: int, permission):
        pass

    
    
user_dao: UserDAO = UserDAO(User)