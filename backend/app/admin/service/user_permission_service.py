from app.admin.dao.user_permission_dao import user_permission_dao
from core.db_postgres import async_session

class UserPermissionService:

    async def get_permission(self, user_id: str, report_id: int):
        async with async_session() as session:
            result = await user_permission_dao.get_all_with_filter(session, None, user_id=user_id, report_id=report_id)
            return result
        

user_permission_service: UserPermissionService = UserPermissionService()