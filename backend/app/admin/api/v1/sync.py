from fastapi import APIRouter
from app.admin.schema.sync import SyncShema
from datetime import datetime
from typing import List
from app.admin.service.sync_service import SyncService


router = APIRouter(prefix="/synch", tags=["Синхронизация с МойСклад"])

@router.get("/statuses", response_model=List[SyncShema])
async def get_statuses():
    return await SyncService.get_sync_data()