export type tRetailStore = {
  id: string
  name: string
  archived: boolean
  salary_per_shift: number
}

export type tPaymentPurpose = {
  id: number,
  name: string
}

export type tBonus = {
  id: number,
  name: string,
  value: number
}

export type tSalaryCondition = {
  id: number,
  retail_store_id: string,
  retail_store_name: string,
  salary_per_shift: number
}

export type tEmployee = {
  id: string,
  name: string
}