from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from datetime import date
from app.dashboard.service.dashboard_sevrice import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Дашборд по точке продаж"])

@router.get("/{report_title}")
async def get_dashboard(user: CurrentUserDep, report_title: str, month_start: date):
  return await dashboard_service.get_data(report_title, month_start)