from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from typing import List
from app.directories.schema.payment_purpose_schema import PaymentPurposeCreateSchema, PaymentPurposeSchema
from app.directories.service.payment_purpose_service import payment_purpose_service

router = APIRouter(prefix="/payment_purpose", tags=["Справочник. Назначение платежа"])


@router.get("", response_model=List[PaymentPurposeSchema])
async def get_payment_purposes(user: CurrentUserDep):
    return await payment_purpose_service.get_payment_purpose()

@router.post("")
async def create_payment_purpose(user: CurrentUserDep, payment_purpose: PaymentPurposeCreateSchema):
    return await payment_purpose_service.create_payment_purpose(payment_purpose)

@router.put("/{row_id}")
async def edit_payment_purpose(user: CurrentUserDep, row_id: int, payment_purpose: PaymentPurposeCreateSchema):
    return await payment_purpose_service.edit_payment_purpose(row_id, payment_purpose)