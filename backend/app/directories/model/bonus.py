from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, Float
from datetime import datetime

class Bonus(Base):
  __tablename__ = "bonus"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(255))
  value: Mapped[float] = mapped_column(Float)
  updated_at: Mapped[datetime] = mapped_column(
    onupdate=func.timezone("UTC", func.now()),
    server_default=func.timezone("UTC", func.now())
  )
  created_at: Mapped[datetime] = mapped_column(
    server_default=func.timezone("UTC", func.now())
  )
