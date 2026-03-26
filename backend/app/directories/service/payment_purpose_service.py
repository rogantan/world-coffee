from core.db_postgres import async_session
from app.directories.dao.payment_purpose_dao import payment_purpose_dao
from app.directories.schema.payment_purpose_schema import PaymentPurposeCreateSchema, PaymentPurposeUpdateSchema

class PaymentPurposeService:

    async def get_payment_purpose(self):
        async with async_session() as session:
            result = await payment_purpose_dao.get_all(session)
            return result
        
    async def create_payment_purpose(self, payment_purpose: PaymentPurposeCreateSchema):
        async with async_session() as session:
            result = await payment_purpose_dao.add(session, **payment_purpose.model_dump())
            return result

    async def edit_payment_purpose(self, row_id: int, payment_purpose: PaymentPurposeUpdateSchema):
        async with async_session() as session:
            result = await payment_purpose_dao.update(session, row_id, **payment_purpose.model_dump())
            return result


payment_purpose_service: PaymentPurposeService = PaymentPurposeService()