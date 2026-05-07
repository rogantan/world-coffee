import { apiService } from "../api";
import type { tDashboardData, DashboardFilter } from "../../types/dashboards/dashboard";

export const getDashboard = async (filter: DashboardFilter): Promise<tDashboardData> => 
  await apiService.get<tDashboardData>(`/dashboard/${filter.report_name}?month_start=${filter.month_start}`)
