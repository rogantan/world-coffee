from app.admin.schema.user import UserRoleSchema
from app.admin.dao.role_dao import role_dao
from common.exceptions.error import RoleNotFoundException, UserNotFoundException
from core.db_postgres import async_session
from app.admin.dao.user_dao import user_dao
from app.admin.dao.role_permission_dao import role_permission_dao

class UserService:

    async def get_user(self, username: str):
        async with async_session() as session:
            user = await user_dao.get(username, session)
            permission = await user_dao.user_permissions(session, user.id)
            # role = await user_dao.get_role(session, username)
            info = user.__dict__
            info["salary_increase"] = user.salary_increase[-1] if user.salary_increase else None
            info["permissions"] = permission
            info["role"] = user.role.name
            return user
        
    async def get_user_list(self):
        async with async_session() as session:
            result = []
            users = await user_dao.get_users(session)
            for user in users:
                permissions = await user_dao.user_permissions(session, user.id)
                info = user.__dict__
                info["salary_increase"] = user.salary_increase[-1] if user.salary_increase else None
                info["permissions"] = permissions
                info["role"] = user.role.name
                result.append(user)
            return result
        
    async def reset_user_password(self, username: str):
        async with async_session() as session:
            return await user_dao.reset_password(session, username)
        
    async def change_role(self, username: str, role: UserRoleSchema):
        async with async_session() as session:
            role_obj = await role_dao.find_one_or_more(session, name=role.role)
            if not role_obj:
                raise RoleNotFoundException
            if not await user_dao.find_one_or_more(session, uid=username):
                raise UserNotFoundException
            await user_dao.reset_permissions(session, username)
            role_permissions = await role_permission_dao.get_permissions(session, role_obj.id)
            for permission in role_permissions:
                await user_dao.change_permissions(session, username, permission.report_id, permission.mode)
            result = await role_dao.update_role(session, username, role.role)
            return result


user_service: UserService = UserService()