type tTestResultRows = {
  date: string
  points: string
  rank: number
}

export type tTestResult = {
  id: number
  name: string
  employee_email: string 
  employee_id: string 
  employee_name: string 
  date_from: string
  date_to: string
  is_active: boolean
  was_passed: boolean
  rows: tTestResultRows[]
}


type tBestEmployeeRows = {
  date: string
  test_rank: number
  avg_check_dinamic: string
  avg_check_rank: number
  total_points: number
  total_rank: number
}
export type tBestEmployee = {
  employee_name:string
  rows: tBestEmployeeRows[]
}
