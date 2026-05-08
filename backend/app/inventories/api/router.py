from fastapi import APIRouter
from app.inventories.api.v1.custom_inventory import router as custom_inventory_router

router = APIRouter()

router.include_router(custom_inventory_router)