from pydantic import BaseModel

class PaymentPurposeSchema(BaseModel):
    id: int
    name: str

class PaymentPurposeCreateSchema(BaseModel):
    name: str
