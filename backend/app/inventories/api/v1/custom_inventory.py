from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from app.inventories.service.custom_inventory_service import custom_inventory_service
from typing import List
from app.inventories.schema.inventory import SInventory

router = APIRouter(prefix="/inventory", tags=["Инвентаризация"])

@router.get("/{report_title}", response_model=List[SInventory])
async def get_custom_inventory(user: CurrentUserDep, report_title: str):
  return await custom_inventory_service.get_items(report_title)

@router.put("")
async def edit_inventory_item(user: CurrentUserDep):
  pass

@router.post("")
async def unload_ms(user: CurrentUserDep):
  pass

@router.post("")
async def clear_items(user: CurrentUserDep):
  pass