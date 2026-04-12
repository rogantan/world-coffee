from fastapi import APIRouter
from app.directories.api.v1.payment_purpose import router as payment_purpose_router
from app.directories.api.v1.bonus import router as bonus_router
from app.directories.api.v1.salary import router as salary_router

router = APIRouter()

router.include_router(payment_purpose_router)
router.include_router(bonus_router)
router.include_router(salary_router)