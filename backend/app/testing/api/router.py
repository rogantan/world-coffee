from fastapi import APIRouter
from app.testing.api.v1.admin import router as admin_router
from app.testing.api.v1.passing import router as passing_router
from app.testing.api.v1.user import router as user_router

router = APIRouter()

router.include_router(admin_router)
router.include_router(passing_router)
router.include_router(user_router)