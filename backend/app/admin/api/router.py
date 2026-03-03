from fastapi import APIRouter
from app.admin.api.v1.sync import router as router1

router = APIRouter()

router.include_router(router1)