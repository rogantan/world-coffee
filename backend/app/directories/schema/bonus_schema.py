from pydantic import BaseModel

class BonusSchema(BaseModel):
  name: str
  value: float