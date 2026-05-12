from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from app.inventories.service.custom_inventory_service import custom_inventory_service
from typing import List
from app.inventories.schema.inventory import SInventory, SInventoryEdit
from app.utils.permission import has_permission
from app.admin.enum.permission_mode import PermissionMode
from common.exceptions.error import ForbiddenException

router = APIRouter(prefix="/inventory", tags=["Инвентаризация"])

@router.get("/{report_title}", response_model=List[SInventory])
async def get_custom_inventory(user: CurrentUserDep, report_title: str):
  if user.role == "admin" or user.role == "auditor" or user.role == 'salesman': 
    return await custom_inventory_service.get_items(report_title)
  raise ForbiddenException

@router.put("/{report_title}/item/{item_id}")
async def edit_inventory_item(user: CurrentUserDep, report_title: str, item_id: int, data: SInventoryEdit):
  if user.role == "admin" or user.role == "auditor" or user.role == 'salesman': 
    return await custom_inventory_service.edit_item(item_id, data)
  raise ForbiddenException

@router.post("/{report_title}/inload")
async def unload_ms(user: CurrentUserDep, report_title: str):
  if user.role == "admin" or user.role == "auditor" or user.role == 'salesman':
    await custom_inventory_service.unload_inventory(report_title, user)
    return await custom_inventory_service.clear_items(report_title)
  raise ForbiddenException

@router.post("/{report_title}/clear")
async def clear_items(user: CurrentUserDep, report_title: str):
  if user.role == "admin" or user.role == "auditor" or user.role == 'salesman': 
    return await custom_inventory_service.clear_items(report_title)
  raise ForbiddenException