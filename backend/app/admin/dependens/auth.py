from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from core.config import settings
from app.admin.schema.user import UserCreateSchema, UserSchema
from app.admin.schema.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/backend/auth/token")

from app.admin.service.user_service import user_service

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await user_service.get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(user: Annotated[UserCreateSchema, Depends(get_current_user)], request: Request):
    authorization: str = request.headers.get("Authorization", "No headers")
    if user.archived:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

CurrentUserDep = Annotated[UserSchema, Depends(get_current_active_user)]