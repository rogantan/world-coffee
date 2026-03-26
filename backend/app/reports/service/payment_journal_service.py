from app.reports.dao.payment_journal_dao import payment_journal_dao
from common.exceptions.error import RetailStoreIdNotFoundException, PaymentPurposeIdNotFoundException, UserNotFoundException
from core.db_postgres import async_session
from datetime import date
from app.reports.schema.payment_journal import PaymentJournalCreateSchema
from app.reports.dao.retail_store_dao import retail_store_dao
from app.directories.dao.payment_purpose_dao import payment_purpose_dao
from app.admin.dao.user_dao import user_dao

class PaymentJouranlService:
    
    async def get(
        self,
        payment_date_from: date,
        payment_date_to: date,
        accrual_date_from: date,
        accrual_date_to: date,
        order_by: str,
        desc: bool
    ):
        async with async_session() as session:
            result = await payment_journal_dao.get_all_journal(
                session,
                payment_date_from,
                payment_date_to,
                accrual_date_from,
                accrual_date_to,
                order_by,
                desc
            )
            return result
        
    async def create_payment(self, payment_journal: PaymentJournalCreateSchema):
        async with async_session() as session:
            if not await retail_store_dao.find_by_id(session, payment_journal.retail_store_id):
                raise RetailStoreIdNotFoundException
            if not await payment_purpose_dao.find_by_id(session, payment_journal.payment_purpose_id):
                raise PaymentPurposeIdNotFoundException
            if not await user_dao.find_by_id(session, payment_journal.user_id):
                raise UserNotFoundException
            
            await payment_journal_dao.add(session, **payment_journal.model_dump())
    
    async def edit_payment(self, row_id: int, payment_journal: PaymentJournalCreateSchema):
        async with async_session() as session:
            if not await retail_store_dao.find_by_id(session, payment_journal.retail_store_id):
                raise RetailStoreIdNotFoundException
            if not await payment_purpose_dao.find_by_id(session, payment_journal.payment_purpose_id):
                raise PaymentPurposeIdNotFoundException
            if not await user_dao.find_by_id(session, payment_journal.user_id):
                raise UserNotFoundException
            
            await payment_journal_dao.update(session, row_id, **payment_journal.model_dump())
    
    async def delete_payment(self, row_id: int):
        async with async_session() as session:
            return await payment_journal_dao.delete(session, row_id)

        
payment_journal_service: PaymentJouranlService = PaymentJouranlService()