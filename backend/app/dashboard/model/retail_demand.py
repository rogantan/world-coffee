from common.model import Base
from sqlalchemy import String, UUID, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime


class RetailDemand(Base):
    __tablename__ = "retail_demand"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    agent_type = Mapped[str]
    retail_store_id: Mapped[str] = mapped_column(ForeignKey("retail_store.id"))
    owner_id: Mapped[Optional[str]] = mapped_column(ForeignKey("user.id"), index=True, nullable=True)
    senior_salesman_id: Mapped[Optional[str]] = mapped_column(ForeignKey("user.id"), nullable=True)
    organization_name: Mapped[Optional[str]] = mapped_column(String(255))
    applicable: Mapped[bool]
    name: Mapped[str] = mapped_column(String(255))
    cash_sum: Mapped[float]
    no_cash_sum: Mapped[float]
    payed_sum: Mapped[float]
    qr_sum: Mapped[float]
    sum: Mapped[float]
    discounts: Mapped[float] = mapped_column(default=0)
    senior_salesman_percent: Mapped[float] = mapped_column(Float, nullable=True)
    senior_salesman_personal_percent: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    salesman_percent: Mapped[float] = mapped_column(Float, nullable=True)
    moment: Mapped[datetime]
    ms_created: Mapped[datetime]
    ms_updated: Mapped[datetime]
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.timezone("UTC", func.now()),
        server_default=func.timezone("UTC", func.now()),
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.timezone("UTC", func.now())
    )