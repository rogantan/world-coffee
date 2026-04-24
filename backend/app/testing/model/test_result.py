from datetime import datetime

from sqlalchemy import (
  ForeignKey,
  func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import Base


class TestResult(Base):
  __tablename__ = "test_result"

  id: Mapped[int] = mapped_column(primary_key=True)
  test_id: Mapped[int] = mapped_column(ForeignKey("test.id"))
  user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
  question_count: Mapped[int]
  correct_question_count: Mapped[int]
  created_at: Mapped[datetime] = mapped_column(
    server_default=func.timezone("UTC", func.now())
  )

  test = relationship("Test", back_populates="results")
