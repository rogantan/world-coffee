import { apiService } from "../api";
import type { tSync } from "../../types/admin/sync";

export const getSync = async (): Promise<tSync[]> => 
  await apiService.get<tSync[]>('/synch/statuses');