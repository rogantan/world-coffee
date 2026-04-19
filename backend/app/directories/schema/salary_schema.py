from pydantic import BaseModel
from uuid import UUID

class SalarySchema(BaseModel):
  salary_per_shift: float