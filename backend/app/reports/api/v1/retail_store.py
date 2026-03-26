from fastapi import APIRouter
from typing import List
from app.reports.schema.retail_store import RetailStoreSchema
from app.admin.dependens.auth import CurrentUserDep
from app.reports.service.retail_store_service import retail_store_service


router = APIRouter(prefix="/retail_stores", tags=["Справочник. Точки продаж"])

@router.get("", response_model=List[RetailStoreSchema])
async def get_retail_stores(user: CurrentUserDep):
    return await retail_store_service.get_retail_stores()