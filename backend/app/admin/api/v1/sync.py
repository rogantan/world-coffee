from fastapi import APIRouter
from app.admin.schema.sync import SyncShema
from datetime import datetime
from typing import List
from app.admin.service.sync_service import sync_service
from app.admin.dependens.auth import CurrentUserDep
from common.exceptions.error import ForbiddenException


router = APIRouter(prefix="/synch", tags=["Синхронизация с МойСклад"])

@router.get("/statuses", response_model=List[SyncShema])
async def get_statuses(user: CurrentUserDep):
    if user.role != "admin":
        raise ForbiddenException
    return await sync_service.get_sync_data()