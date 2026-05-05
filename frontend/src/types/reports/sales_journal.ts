export type tReports = {
  employee_name: string
  date: string
  enter_sum: number
  link: string
  loss_sum: number
  manual_changes: number
  month: string
  name: string
  retail_store_name: string
  retention_sum: number
  salesman_name: string
  shifts?: any[]
  salesman_percent?: string
  uuid: string
}


export type SaleJournal = {
  agent_name: string
  cash_sum: number
  discounts: number
  id: string
  moment: string
  name: string
  no_cash_sum: number
  organization_name: string
  owner_name: string
  qr_sum: number
  retail_store_name: string
  sum: number
}