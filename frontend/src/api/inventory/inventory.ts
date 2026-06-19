import { apiService } from "../api";
import type { Inventory } from "../../types/inventory/inventory";

export const getInventoryByShop = async (report_title: string): Promise<Inventory[]> => 
  await apiService.get<Inventory[]>(`/inventory/${report_title}`);

export const putInventoryByShop = async (report_title: string, item_id: string, data: any):Promise<Inventory> => 
  await apiService.put<Inventory>(`/inventory/${report_title}/item/${item_id}`, data);

export const clearItems = async (report_title: string) =>
  await apiService.post(`/inventory/${report_title}/clear`);

export const unloadInventoryByShop = async (report_title: string) => 
  await apiService.post(`/inventory/${report_title}/inload`);