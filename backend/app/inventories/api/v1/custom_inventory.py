from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from app.inventories.service.custom_inventory_service import custom_inventory_service
from typing import List
from app.inventories.schema.inventory import SInventory, SInventoryEdit

router = APIRouter(prefix="/inventory", tags=["Инвентаризация"])

@router.get("/{report_title}", response_model=List[SInventory])
async def get_custom_inventory(user: CurrentUserDep, report_title: str):
  return await custom_inventory_service.get_items(report_title)

@router.put("/{report_title}/item/{item_id}")
async def edit_inventory_item(user: CurrentUserDep, report_title: str, item_id: int, data: SInventoryEdit):
  return await custom_inventory_service.edit_item(item_id, data)

@router.post("")
async def unload_ms(user: CurrentUserDep):
  pass

@router.post("/{report_title}/clear")
async def clear_items(user: CurrentUserDep, report_title: str):
  return await custom_inventory_service.clear_items(report_title)