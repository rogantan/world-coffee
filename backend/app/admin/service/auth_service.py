from fastapi import Form, HTTPException, Request, status
from app.admin.dao.user_dao import user_dao
from core.db_postgres import async_session
from app.admin.dependens.auth import create_access_token
from app.admin.schema.user import AuthSchema
from app.admin.schema.token import Token
from core.config import settings
from datetime import timedelta


class AuthService:

    async def login(self, request: Request, obj: AuthSchema):
        async with async_session() as session:
            user = await user_dao.get_user(session, obj.username)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            if not user.registered:
                await user_dao.set_password_hash(session, user.id, obj.password)
            
            if not user_dao.verify_password(obj.password, user.hash_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = create_access_token(
                data={"sub": user.uid, "role": user.role.name},
                expires_delta=access_token_expires
            )
            return Token(access_token=access_token, token_type="bearer")

auth_service: AuthService = AuthService()