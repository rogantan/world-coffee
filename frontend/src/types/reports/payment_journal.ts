export type PaymentJournal = {
  employee_name: string
  employee_id: string
  payment_purpose_name: string
  payment_purpose_id: string
  retail_store_name: string
  retail_store_id: string
  accrual_date: string | Date
  amount: number
  description: string
  id: number
  payment_date: string | Date
}