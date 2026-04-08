import { apiService } from "../api";
import type { tRetailStore } from "../../types/admin/lists";
import type { tPaymentPurpose } from "../../types/admin/lists";

export const getRetailStores = async (): Promise<tRetailStore[]> =>
  await apiService.get<tRetailStore[]>("/retail_stores");

export const getPaymentPurpose = async(): Promise<tPaymentPurpose[]> => 
  await apiService.get<tPaymentPurpose[]>("/payment_purpose");