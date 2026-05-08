import { apiService } from "../api";
import type { Inventory } from "../../types/inventory/inventory";

export const getInventoryByShop = async (report_title: string): Promise<Inventory[]> => 
  await apiService.get<Inventory[]>(`/inventory/${report_title}`);