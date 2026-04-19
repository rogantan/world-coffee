import { apiService } from "../api";
import type { tBonus, tRetailStore } from "../../types/admin/lists";
import type { tPaymentPurpose } from "../../types/admin/lists";

export const getRetailStores = async (): Promise<tRetailStore[]> =>
  await apiService.get<tRetailStore[]>("/retail_stores/salary");

export const getPaymentPurpose = async(): Promise<tPaymentPurpose[]> => 
  await apiService.get<tPaymentPurpose[]>("/payment_purpose");

export const postPaymentPurpose = async(name: string) => 
  await apiService.post(`/payment_purpose`, {"name": name});

export const putPaymentPurpose = async (row_id: number, new_value: string) =>
  await apiService.put(`/payment_purpose/${row_id}`, { "name": new_value });

export const getBonuses = async(): Promise<tBonus[]> => 
  await apiService.get<tBonus[]>("/bonuses");

export const postBonuses = async(name: string, value: number) => 
  await apiService.post(`/bonuses`, { "name": name, "value": value });

export const putBonuses = async(row_id: number, name: string, value: number) => 
  await apiService.put(`/bonuses/${row_id}`, {"name": name, "value": value});

export const putSalary = async(row_id: string, new_salary: number) =>
  await apiService.put(`/salary/${row_id}`, {"salary_per_shift": new_salary})