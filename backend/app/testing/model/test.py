from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import Base


class Test(Base):
  __tablename__ = "test"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(100), unique=True)
  date_from: Mapped[datetime]
  date_to: Mapped[datetime]
  result_resets: Mapped[bool] = mapped_column(default=False)
  updated_at: Mapped[datetime] = mapped_column(
    onupdate=func.timezone("UTC", func.now()),
    server_default=func.timezone("UTC", func.now()),
  )
  created_at: Mapped[datetime] = mapped_column(
    server_default=func.timezone("UTC", func.now())
  )

  questions = relationship(
    "Question",
    back_populates="test",
    cascade="all, delete",
    order_by="Question.id",
  )

  results = relationship("TestResult", back_populates="test", cascade="all, delete")
