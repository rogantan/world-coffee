import itertools
from app.reports.dao.report_dao import report_dao
from app.reports.dao.retail_store_dao import retail_store_dao
from app.utils.support import get_date_from, get_date_to
from core.db_postgres import async_session
from datetime import date, timedelta

class ReportService:

    async def get_report(self, title: str):
        async with async_session() as session:
            result = await report_dao.find_one_or_more(session, title=title)
            return result
        
    async def get_revenue_month(self, date_from: date, date_to: date):
        async with async_session.begin() as db:

            date_from = date_from.replace(day=1)
            date_to = (date_to.replace(day=1) + timedelta(days=32)).replace(
                day=1
            ) - timedelta(days=1)

            result = []
            result.append(
                {
                    "retail_store_name": "ИТОГИ",
                    "employees": [
                        {
                            "employee_name": "ИТОГИ",
                            "data": [
                                {
                                    "date_from": get_date_from(date_from, row.date),
                                    "value": str(row.revenue),
                                    "dynamics": row.revenue_dynamics,
                                    "color": row.color,
                                }
                                for row in await report_dao.get_total_revenue(
                                    db, date_from, date_to
                                )
                            ],
                        }
                    ],
                }
            )

            retail_stores = await retail_store_dao.get_retail_stores(db)
            for retail_store in retail_stores:
                data = await report_dao.get_revenue(
                    db, date_from, date_to, retail_store.id
                )
                employees = []
                for key, group in itertools.groupby(
                    data, key=lambda x: x.employee_name
                ):
                    if key == "":
                        key = retail_store.name
                    employees.append(
                        {
                            "employee_name": key,
                            "data": [
                                {
                                    "date_from": get_date_from(date_from, row.date),
                                    "value": str(row.revenue),
                                    "dynamics": row.revenue_dynamics,
                                    "color": row.color,
                                }
                                for row in group
                            ],
                        }
                    )

                result.append(
                    {"retail_store_name": retail_store.name, "employees": employees}
                )

            return result
        
    async def get_shift_day(self, date_from: date, date_to: date):
        async with async_session.begin() as db:
            result = []
            retail_stores = await retail_store_dao.get_retail_stores(db)

            for retail_store in retail_stores:
                data = await report_dao.get_shift_by_day(
                    db,
                    date_from,
                    date_to,
                    retail_store.id,
                )
                employees = []
                for key, group in itertools.groupby(
                    data, key=lambda x: x.employee_name
                ):
                    employees.append(
                        {
                            "employee_name": key,
                            "shifts": [
                                {
                                    "date": row.date.strftime("%d.%m.%Y"),
                                    "shift_count": row.shift_count,
                                }
                                for row in group
                            ],
                        }
                    )
                result.append(
                    {"retail_store_name": retail_store.name, "employees": employees}
                )
            return result

    async def get_shift_month(self, date_from: date, date_to: date):
        async with async_session.begin() as db:
            result = []
            retail_stores = await retail_store_dao.get_retail_stores(db)
            for retail_store in retail_stores:
                data = await report_dao.get_shift_by_month(
                    db, date_from, date_to, retail_store.id
                )
                employees = []
                for key, group in itertools.groupby(
                    data, key=lambda x: x.employee_name
                ):
                    employees.append(
                        {
                            "employee_name": key,
                            "shifts": [
                                {
                                    "date_from": get_date_from(date_from, row.date),
                                    "date_to": get_date_to(date_to, row.date),
                                    "shift_count": row.shift_count,
                                }
                                for row in group
                            ],
                        }
                    )
                result.append(
                    {"retail_store_name": retail_store.name, "employees": employees}
                )
            return result
        

report_service: ReportService = ReportService()