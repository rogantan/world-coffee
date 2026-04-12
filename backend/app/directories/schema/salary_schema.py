from pydantic import BaseModel
from uuid import UUID

class SalarySchema(BaseModel):
  id: int
  retail_store_name: str
  salary_per_shift: float

class SalaryCreateSchema(BaseModel):
  retail_store_id: UUID
  salary_per_shift: float