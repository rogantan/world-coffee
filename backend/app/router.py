from fastapi import APIRouter
from app.admin.api.router import router as router1
from core.config import settings

router = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

router.include_router(router1)