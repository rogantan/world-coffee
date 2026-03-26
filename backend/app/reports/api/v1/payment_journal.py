from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from typing import List
from datetime import date
from app.reports.service.payment_journal_service import payment_journal_service
from app.reports.schema.payment_journal import PaymentJournalCreateSchema, PaymentJournalSchema

router = APIRouter(prefix="/payment_journal", tags=["Отчет. Журнал платежей"])

@router.get("", response_model=List[PaymentJournalSchema])
async def get_payments_journal(user: CurrentUserDep,
    payment_date_from: date,
    payment_date_to: date,
    accrual_date_from: date,
    accrual_date_to: date,
    order_by: str,
    desc: bool):
    return await payment_journal_service.get(payment_date_from, payment_date_to, accrual_date_from, accrual_date_to, order_by, desc)

@router.post("")
async def add_payment_jouranl(user: CurrentUserDep, payment_journal: PaymentJournalCreateSchema):
    return await payment_journal_service.create_payment(payment_journal)

@router.put("/{row_id}")
async def edit_payment_journal(user: CurrentUserDep, row_id: int, payment_journal: PaymentJournalCreateSchema):
    return await payment_journal_service.edit_payment(row_id, payment_journal)

@router.delete("/{row_id}")
async def delete_payment_journal(user: CurrentUserDep, row_id: int):
    return await payment_journal_service.delete_payment(row_id)