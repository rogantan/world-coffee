from fastapi import APIRouter
from app.admin.api.v1.sync import router as sync_router1
from app.admin.api.v1.auth import router as auth_router
from app.admin.api.v1.user import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(sync_router1)
router.include_router(user_router)