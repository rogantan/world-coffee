import { apiService } from "../api";
import type { tReports } from "../../types/reports/sales_journal";
import type { ReportFilter } from "../../types/reports/filter";
export const getAuditor = async (
  {
    report_name,
    date_from,
    date_to,
    order_by = 'date',
    desc = false
  }: ReportFilter
): Promise<tReports[]> =>
  await apiService.get<tReports[]>(`/reports/${report_name}?date_from=${date_from}&date_to=${date_to}&order_by=${order_by}&desc=${desc}`);
