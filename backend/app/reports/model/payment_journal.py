from common.model import Base
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime
from typing import Optional

class PaymentJournal(Base):
    __tablename__ = "payment_journal"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_date: Mapped[date] 
    retail_store_id: Mapped[str] = mapped_column(ForeignKey("retail_store.id"))
    amount: Mapped[float]
    payment_purpose_id: Mapped[int] = mapped_column(ForeignKey("payment_purpose.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    accrual_date: Mapped[date]
    description: Mapped[Optional[str]]

    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.timezone("UTC", func.now()),
        server_default=func.timezone("UTC", func.now())
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.timezone("UTC", func.now())
    )