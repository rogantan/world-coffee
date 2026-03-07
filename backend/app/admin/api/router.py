from fastapi import APIRouter
from app.admin.api.v1.sync import router as router1
from app.admin.api.v1.auth import router as auth_router

router = APIRouter()

router.include_router(router1)
router.include_router(auth_router)