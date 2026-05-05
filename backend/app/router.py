from fastapi import APIRouter
from app.admin.api.router import router as router1
from app.reports.api.router import router as router2
from app.directories.api.router import router as router3
from app.testing.api.router import router as router4
from app.dashboard.api.router import router as router5
from core.config import settings

router = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

router.include_router(router1)
router.include_router(router2)
router.include_router(router3)
router.include_router(router4)
router.include_router(router5)