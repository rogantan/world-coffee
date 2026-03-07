from core.db_postgres import async_session
from app.admin.dao.user_dao import user_dao

class UserService:

    async def get_user(username: str):
        async with async_session() as session:
            user = await user_dao.get(username, session)
            permission = await user_dao.user_permissions(session, user.id)
            info = user.__dict__
            info["salary_increase"] = user.salary_increase[-1]
            info["permissions"] = permission
            return user
    
    


user_service: UserService = UserService()