from fastapi import APIRouter
from app.directories.api.v1.payment_purpose import router as payment_purpose_router

router = APIRouter()

router.include_router(payment_purpose_router)