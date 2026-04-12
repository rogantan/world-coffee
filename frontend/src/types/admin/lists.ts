export type tRetailStore = {
  id: string
  name: string
  archived: boolean
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
  retail_store: string,
  salary_per_shift: number
}