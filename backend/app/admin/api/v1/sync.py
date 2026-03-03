from fastapi import APIRouter
from app.admin.schema.sync import SyncShema
from datetime import datetime


router = APIRouter(prefix="/synch", tags=["Синхронизация с МойСклад"])

@router.get("/statuses", response_model=SyncShema)
async def get_statuses():
    return SyncShema(
        start_time=datetime.now(),
        finish_time=datetime.now(),
        status="success"
    )