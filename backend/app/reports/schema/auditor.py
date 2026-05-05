from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class SAuditReport(BaseModel):
  """Модель отчета Аудит"""

  uuid: UUID
  name: str
  month: datetime
  date: datetime
  salesman_name: str
  retail_store_name: str
  loss_sum: float
  enter_sum: float
  link: str
  manual_changes: float
  retention_sum: float