from datetime import datetime
from app.admin.model.user_permission import UserPermission
from app.reports.model.report import Report
from app.admin.model.role import Role
from app.admin.dao.salary_increase_dao import salary_increase_dao
from utils.date_formatter import ms_date_to_datetime
from common.base_dao import BaseDao
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, update
from app.admin.model.user import User
from app.admin.enum.permission_mode import PermissionMode
from app.admin.schema.user import UserRoleSchema
from passlib.context import CryptContext
from app.admin.enum.permission_mode import PermissionMode
from app.admin.dao.user_permission_dao import user_permission_dao

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
        query = select(UserPermission.id).where(User.uid == username).join(User, UserPermission.user_id == User.id)
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
    
    async def change_permissions(self, db: AsyncSession, username: str, report: int, report_mode: PermissionMode):
        query_permissions = (select(UserPermission.id)
            .where(User.uid == username, Report.id == report)
            .join(User, User.id == UserPermission.user_id)
            .join(Report, Report.id == UserPermission.report_id))
        result = await db.execute(query_permissions)
        permissions = result.mappings().one_or_none()

        if permissions:
            try:
                query_update = update(UserPermission).where(UserPermission.id == permissions["id"]).values(mode=report_mode)
                await db.execute(query_update)
            except Exception as e:
                await db.rollback()
            await db.commit()
        else:
            print("No permission found")
    
    async def get_user_by_id(
        self,
        db: AsyncSession,
        id: str,
        archived: bool,
    ):
        return await self.find_one_or_none(db, id=id, archived=archived)
    
    async def add_new_entity(self, db: AsyncSession, entity, role_id: int):
        await self.insert_uncommit(
            db,
            id=entity.get("id"),
            name=entity.get("fullName"),
            role_id=role_id,
            uid=entity.get("uid"),
            last_name=entity.get("lastName"),
            first_name=entity.get("firstName"),
            middle_name=entity.get("middleName"),
            hash_password=entity.get("externalCode"),
            registered=False,
            has_eighteen_months=False,
            email=entity.get("email"),
            archived=entity.get("archived"),
            ms_created=ms_date_to_datetime(entity.get("created")),
            ms_updated=ms_date_to_datetime(entity.get("updated")),
        )

        await user_permission_dao.set_permissions(db, entity.get("uid"), role_id)
        await salary_increase_dao.insert_uncommit(
            db,
            user_id=entity.get("id"),
            created_at=datetime(year=2000, month=1, day=1),
        )

        await db.commit()

    async def get_employees(self, db: AsyncSession):
        query = select(User.id, User.name)
        result = await db.execute(query)
        return result.mappings().all()
    
user_dao: UserDAO = UserDAO(User)