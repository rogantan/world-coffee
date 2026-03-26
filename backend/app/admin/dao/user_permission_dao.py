from common.base_dao import BaseDao
from app.admin.model.user_permission import UserPermission
from app.admin.enum.permission_mode import PermissionMode
from sqlalchemy import select, update
from app.reports.model.report import Report
from app.admin.model.user import User
from core.db_postgres import AsyncSession

class UserPermissionDao(BaseDao[UserPermission]):

    async def user_permissions(self, db: AsyncSession, user_id: str):
        query = (select(UserPermission.mode, Report.display_name, Report.title)
        .where(UserPermission.user_id == user_id).join(Report, UserPermission.report_id == Report.id))
        result = await db.execute(query)
        return result.mappings().all()
    

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


user_permission_dao: UserPermissionDao = UserPermissionDao(UserPermission)