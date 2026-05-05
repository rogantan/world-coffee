from datetime import date
from core.db_postgres import async_session
from app.dashboard.dao.dashboard_dao import dashboard_dao

class DashboardService:
  async def get_data(self, report_title: str, month_start: date):
    data = {}
    async with async_session() as session:
      data["revenue"] = await dashboard_dao.get_revenue_dynamics(session, report_title, month_start)
      data["avg_revenue"] = await dashboard_dao.get_average_daily_revenue_dynamics(session, report_title, month_start)
      data["number_of_checks"] = await dashboard_dao.get_number_of_checks_dynamics(session, report_title, month_start)
      data["avg_number_of_checks"] = await dashboard_dao.get_average_number_of_checks_dynamics(session, report_title, month_start)
      data["avg_check"] = await dashboard_dao.get_average_check_dynamics(session, report_title, month_start)
      return data

dashboard_service: DashboardService = DashboardService()