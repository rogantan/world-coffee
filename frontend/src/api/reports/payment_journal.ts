import { apiService } from '../../api/api';
import type { PaymentJournal } from "../../types/reports/payment_journal";
export type PaymentJournalBody = {
  payment_date_from: string,
  payment_date_to: string,
  accrual_date_from: string,
  accrual_date_to: string
}

export const getPaymentJournal = async ({
  payment_date_from,
  payment_date_to,
  accrual_date_from,
  accrual_date_to
}: PaymentJournalBody):Promise<PaymentJournal[]> => {
  return await apiService.get<PaymentJournal[]>(
    `/payment_journal?` +
    `payment_date_from=${payment_date_from}&` +
    `payment_date_to=${payment_date_to}&` +
    `accrual_date_from=${accrual_date_from}&` +
    `accrual_date_to=${accrual_date_to}`);
};
 
export const newSalesJournal = async (data: any) => {
  return await apiService.post('/payment_journal', data)
}

export const editSalesJournal = async (record_id: number, data: any) => {
  return await apiService.put(`/payment_journal/${record_id}`, data)
}

export const deleteSalesJournal = async (record_id: number) => {
  return await apiService.delete(`/payment_journal/${record_id}`)
}
