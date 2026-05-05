from pydantic import BaseModel

class ItemData(BaseModel):
  last_month: str | float | int
  current_month: str | float | int
  lfl: str


class DashboardData(BaseModel):
  revenue: ItemData
  avg_revenue: ItemData
  number_of_checks: ItemData
  avg_number_of_checks: ItemData
  avg_check: ItemData