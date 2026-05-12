from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from typing import List
from app.utils.permission import has_permission
from app.admin.enum.permission_mode import PermissionMode
from datetime import date
from common.exceptions.error import ForbiddenException
from app.reports.schema.sales_journal import SSale
from app.reports.schema.auditor import SAuditReport
from app.dashboard.service.retail_demand_service import retail_demand_service
from app.inventories.service.inventory_service import inventory_service
from app.reports.service.report_service import report_service
from pprint import pprint

router = APIRouter(prefix="/reports", tags=["Отчёты"])

@router.get("/sales_journal", summary="Отчёт Журнал продаж", response_model=List[SSale])
async def get_sales_journal(user: CurrentUserDep, date_from: date, date_to: date, order_by: str = "moment", desc: bool = False,):
  if not await has_permission(user, "sales_journal", PermissionMode.DISPLAYED):
    raise ForbiddenException
  pprint("HELLO")
  return await retail_demand_service.get_all(order_by, desc, date_from, date_to)

@router.get("/auditor", summary='Отчёт Аудитор', response_model=List[SAuditReport])
async def get_auditor(user: CurrentUserDep, date_from: date, date_to: date, order_by: str = "date", desc: bool = False):
  if not await has_permission(user, "auditor", PermissionMode.DISPLAYED):
    raise ForbiddenException
  return await inventory_service.get_all(date_from, date_to, order_by, desc)

@router.get("/revenue_monthly", summary='Отчёт Выручка в месяц')
async def get_revenue_monthly(user: CurrentUserDep, date_from: date, date_to: date,):
  if not await has_permission(user, "revenue_month", PermissionMode.DISPLAYED):
    raise ForbiddenException
  return await report_service.get_revenue_month(date_from, date_to)

@router.get("/shift_day")
async def get_shift_day(user: CurrentUserDep, date_from: date, date_to: date):
  if not await has_permission(user, "shift_day", PermissionMode.DISPLAYED):
    raise ForbiddenException
  return await report_service.get_shift_day(date_from, date_to)

@router.get("/shift_month")
async def get_shift_month(user: CurrentUserDep, date_from: date, date_to: date):
  if not await has_permission(user, "shift_month", PermissionMode.DISPLAYED):
    raise ForbiddenException
  return await report_service.get_shift_month(date_from, date_to)