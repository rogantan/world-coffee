from pydantic import BaseModel

class PaymentPurposeSchema(BaseModel):
    name: str

class PaymentPurposeCreateSchema(PaymentPurposeSchema):
    id: int
    name: str

class PaymentPurposeUpdateSchema(PaymentPurposeSchema):
    archived: bool