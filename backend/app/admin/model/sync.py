from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, func
from sqlalchemy import String, BigInteger
from datetime import datetime
from typing import Optional

class Synchronization(Base):
    __tablename__ = "synchronization"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start_time: Mapped[datetime]
    finish_time: Mapped[Optional[datetime]]
    status: Mapped[str] = mapped_column(String(255))