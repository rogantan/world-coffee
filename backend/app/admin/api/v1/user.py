from fastapi import APIRouter, HTTPException, status
from app.admin.schema.user import UserSchema, UserRoleSchema
from app.admin.dependens.auth import CurrentUserDep
from app.admin.service.user_service import user_service
from typing import List

router = APIRouter(prefix="/user", tags=["Настройки пользователей"])

@router.get("/me", response_model=UserSchema, response_model_exclude="hash_password", summary="Получение информации о текущем пользователе")
async def get_current_user(user: CurrentUserDep):
    return user

@router.get("/list_users", response_model=List[UserSchema], summary="Получение информации о всех пользователях")
async def get_user_list(user: CurrentUserDep):
    return await user_service.get_user_list()

@router.get("/{username}", response_model=UserSchema, response_model_exclude="hash_password", summary="Получение информации о пользователе по username")
async def get_user_by_username(username: str, user: CurrentUserDep):
    return await user_service.get_user(username)

@router.post("/{username}/reset_password", summary="Сбросить пароль у пользователя")
async def reset_password(username: str, user: CurrentUserDep):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin cam reset password"
        )
    return await user_service.reset_user_password(username)

@router.put("/{username}/role")
async def update_role(username: str, role: UserRoleSchema, user: CurrentUserDep):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update user role"
        )
    return await user_service.change_role(username, role)

@router.post("/create_users")
async def create():
    pass