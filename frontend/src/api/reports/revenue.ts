import { apiService } from "../api";
import type { tReports } from "../../types/reports/sales_journal";
import type { ReportFilerSecond } from "../../types/reports/filter";

export const getRevenueMonth = async (
  {
    date_from,
    date_to
  }: ReportFilerSecond
): Promise<tReports[]> =>
  await apiService.get<tReports[]>(`/reports/revenue_monthly?date_from=${date_from}&date_to=${date_to}`);
