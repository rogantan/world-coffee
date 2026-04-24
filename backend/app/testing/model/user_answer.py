from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import Base


class UserAnswer(Base):

  __tablename__ = "user_answer"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
  choice_id: Mapped[str] = mapped_column(ForeignKey("choices.id"))
  created_at: Mapped[datetime] = mapped_column(
    server_default=func.timezone("UTC", func.now())
  )

  __table_args__ = (
    UniqueConstraint(
      "user_id", "choice_id", name="_user_id_choice_id_uc"
    ),
  )

  answer_option = relationship("Choice", back_populates="user_answers")
