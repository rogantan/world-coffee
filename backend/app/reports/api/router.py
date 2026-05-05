from fastapi import APIRouter
from app.reports.api.v1.payment_journal import router as payment_journal_router
from app.reports.api.v1.retail_store import router as retail_store_router
from app.reports.api.v1.reports import router as reports_router

router = APIRouter()

router.include_router(payment_journal_router)
router.include_router(retail_store_router)
router.include_router(reports_router)