from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func
from datetime import datetime

class PaymentPurpose(Base):
    __tablename__ = "payment_purpose"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    archived: Mapped[bool] = mapped_column(default=False)
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.timezone("UTC", func.now()),
        server_default=func.timezone("UTC", func.now())
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.timezone("UTC", func.now())
    )
