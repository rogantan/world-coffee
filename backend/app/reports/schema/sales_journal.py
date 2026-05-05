from pydantic import BaseModel
from uuid import UUID

class SSale(BaseModel):
  id: UUID
  name: str
  moment: str
  retail_store_name: str
  agent_name: str
  cash_sum: float
  no_cash_sum: float
  qr_sum: float
  sum: float
  discounts: float
  owner_name: str