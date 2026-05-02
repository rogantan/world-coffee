from pprint import pprint
from typing import List
from app.admin.schema.user import UserPermission, UserRoleSchema
from app.admin.dao.role_dao import role_dao
from common.exceptions.error import RoleNotFoundException, UserNotFoundException
from core.db_postgres import async_session
from app.admin.dao.user_dao import user_dao
from app.admin.dao.role_permission_dao import role_permission_dao
from app.admin.dao.user_permission_dao import user_permission_dao
from common.my_storage import AsyncHttpClient

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
    
    async def change_permission(self, username: str, report_title: str, permission: UserPermission):
        async with async_session() as session:
            result = await user_permission_dao.change_permissions(session, username, report_title, permission.permission)
            return result
        
    async def storage_update(self, ms_client: AsyncHttpClient, up_time):
        params = {"filter": f"updated>=2025-06-24 00:00:00"}
        employees = await ms_client.get("entity/employee", params=params, cache_key=False)
        employees = employees.get("rows", [])
        
        async with async_session() as session:
            await self.set_default_role(db=session, client=ms_client, employees=employees)
            await self.delete_user(db=session, ms_client=ms_client, up_time=up_time)
        
    
    async def set_default_role(self, db, client: AsyncHttpClient, employees: List):
        for employee in employees:
            user = await user_dao.get_user_by_id(db, employee["id"], False)
            if not user:
                request = await client.get(f"entity/employee/{employee['id']}/security")
                await user_dao.add_new_entity(db, employee, 2)
            else:
                data = {"archived": False}
                await user_dao.update_one_uncommit(db, employee.get("id"), **data)

    async def delete_user(self, db, ms_client: AsyncHttpClient, up_time):
        deleted_users = await ms_client.get(
            "/audit",
            params={
                "filter": (
                    f"moment>={up_time};" f"eventType=delete;entityType=employee"
                ),
            },
        )
        deleted_users = deleted_users.get("rows")
        for user in deleted_users:
            # print(user)
            event_id = user.get("id")
            events = await ms_client.get(f"/audit/{event_id}/events")
            events = events.get("rows")

            for event in events:
                if event["eventType"] == "delete" and event["entityType"] == "employee":
                    user_id = event["entity"]["meta"]["href"].split("/")[-1]

                    exsist_user = await user_dao.get_user_by_id(db, user_id, False)
                    if exsist_user:
                        await user_dao.update(db, user_id, archived=True)

        params = {"filter": f"updated>={up_time};archived=true"}

        archived_employees = await ms_client.get(f"entity/employee", params=params)
        archived_employees = archived_employees.get("rows")

        for employee in archived_employees:
            user = await user_dao.get_user_by_id(db, employee["id"], False)
            if user and not user.archived:
                await user_dao.update(db, user.id, archived=True)

    async def list_employees(self):
        async with async_session() as session:
            return await user_dao.get_employees(session)

user_service: UserService = UserService()