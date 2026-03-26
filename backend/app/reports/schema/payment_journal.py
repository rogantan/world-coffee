from pydantic import BaseModel
from datetime import date
from uuid import UUID

class PaymentJournalSchema(BaseModel):
    id: int
    payment_date: date
    retail_store_name: str
    amount: float
    payment_purpose_name: str
    employee_name: str
    accrual_date: date
    description: str | None

class PaymentJournalCreateSchema(BaseModel):
    payment_date: date
    retail_store_id: UUID
    amount: float
    payment_purpose_id: int
    user_id: UUID
    accrual_date: date
    description: str | None