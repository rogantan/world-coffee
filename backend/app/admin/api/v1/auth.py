from fastapi import APIRouter, Depends, Request, Form
from pyrate_limiter import Limiter, Rate
from app.admin.schema.user import AuthSchema
from fastapi_limiter.depends import RateLimiter
from fastapi.security import OAuth2PasswordRequestForm
from app.admin.service.auth_service import auth_service
from app.admin.schema.token import Token

router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/token", response_model=Token, summary="Вход пользователя в систему")
async def login_access_token(request: Request, 
    username: str = Form(),
    password: str = Form()):
    obj: AuthSchema = AuthSchema(username=username, password=password)
    return await auth_service.login(request, obj)

# dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(5, 60))))],