from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, Enum
from datetime import datetime
from typing import Optional
from app.admin.enum.status import Status

class Synchronization(Base):
    __tablename__ = "synchronization"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start_time: Mapped[datetime]
    finish_time: Mapped[Optional[datetime]]
    status: Mapped[Status] = mapped_column(Enum(Status, name="status_enum"), nullable=False)