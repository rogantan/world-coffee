from common.base_dao import BaseDao
from app.reports.model.payment_journal import PaymentJournal
from app.reports.model.retail_store import RetailStore
from app.directories.model.payment_purpose import PaymentPurpose
from app.admin.model.user import User
from core.db_postgres import AsyncSession
from datetime import date
from typing import List
from sqlalchemy import desc, select

class PaymentJournalDao(BaseDao[PaymentJournal]):
    
    async def get_all_journal(
        self,
        db: AsyncSession,
        payment_date_from: date,
        payment_date_to: date,
        accrual_date_from: date,
        accrual_date_to: date,
        order_by: str = "payment_date",
        order_desc: bool = False
    ) -> List[PaymentJournal]:
        query = (
            select(
                self.model.id,
                self.model.accrual_date,
                self.model.amount,
                self.model.description,
                self.model.payment_date,
                self.model.user_id.label("employee_id"),
                self.model.retail_store_id,
                self.model.payment_purpose_id,
                RetailStore.name.label("retail_store_name"),
                PaymentPurpose.name.label("payment_purpose_name"),
                User.name.label("employee_name")
            )
            .join(RetailStore)
            .join(PaymentPurpose)
            .join(User)
        )
        if accrual_date_from:
            query = query.where(self.model.accrual_date >= accrual_date_from)
        if accrual_date_to:
            query = query.where(self.model.accrual_date <= accrual_date_to)
        if payment_date_from:
            query = query.where(self.model.payment_date >= payment_date_from)
        if payment_date_to:
            query = query.where(self.model.payment_date <= payment_date_to)
        if order_by:
            if order_desc:
                query = query.order_by(desc(order_by))
            else:
                query = query.order_by(order_by)
        result = await db.execute(query)
        return result.mappings().all()


payment_journal_dao: PaymentJournalDao = PaymentJournalDao(PaymentJournal)