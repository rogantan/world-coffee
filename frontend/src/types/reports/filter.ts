export type ReportFilter = {
  report_name: string
  date_from: string
  date_to?: string
  order_by?: string
  desc?: boolean
}

export type ReportFilerSecond = {
  date_from: string
  date_to?: string
}
