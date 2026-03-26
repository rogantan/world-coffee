from common.base_dao import BaseDao
from app.reports.model.report import Report

class ReportDao(BaseDao[Report]):
    pass

report_dao: ReportDao = ReportDao(Report)