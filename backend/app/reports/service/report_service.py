from app.reports.dao.report_dao import report_dao
from core.db_postgres import async_session

class ReportService:

    async def get_report(self, title: str):
        async with async_session() as session:
            result = await report_dao.find_one_or_more(session, name=title)
            return result
        

report_service: ReportService = ReportService()