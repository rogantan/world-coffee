from pydantic import BaseModel

class BonusSchema(BaseModel):
  name: str
  value: float

class BonusEditSchema(BonusSchema):
  id: int