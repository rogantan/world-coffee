type tDashboardItem = {
  last_month: string
  current_month: string
  lfl: string
}

type DashboardUnionTypes =
  'revenue' |
  'avg_revenue' |
  'number_of_checks' |
  'avg_number_of_checks' |
  'avg_check'

export type tDashboardData = {
  [key in DashboardUnionTypes]: tDashboardItem;
};

export type tDashboardUser = {
  employee_name: string
  shift_count: number
  revenue: number
  salesman_percent: number
  number_of_checks: number
  average_revenue: number
  average_check: number
  number_of_bonus_plus_checks: number
  bonus_plus_conversion: string
  bonuses_written_off: number
  salary_plan: number
  salary_fact: number
  bonus: number
  best_emp_bonus: number
  retention_by_inv: number
  retention: number
  debt: number
}

export type tDashboardUserSSalesman = {
  employee_name: string
  shift_count: number
  revenue: number
  number_of_checks: number
  average_revenue: number
  average_check: number
  number_of_bonus_plus_checks: number
  bonus_plus_conversion: string
  bonuses_written_off: number
  salary_plan: number
  salary_fact: number
  bonus: number
  salesman_percent: number
  best_emp_bonus: number
  retention_by_inv: number
  retention: number
  debt: number
}

export type DashboardFilter = {
  report_name: string,
  month_start: string,
  order_by?: string,
  filter?: boolean,
}