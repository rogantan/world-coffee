from fastapi import APIRouter
from app.dashboard.api.v1.dashboard import router as dashboard_router

router = APIRouter()

router.include_router(dashboard_router)