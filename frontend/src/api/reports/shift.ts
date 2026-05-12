import { apiService } from "../api";
import type { tReports } from "../../types/reports/sales_journal";

export const getShifts = async (date_from: any, date_to: any, by: 'day' | 'month'): Promise<tReports[]> =>
  await apiService.get<tReports[]>(`/reports/shift_${by}?date_from=${date_from}&date_to=${date_to}`)