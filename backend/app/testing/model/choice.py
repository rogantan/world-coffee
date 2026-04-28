from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import Base


class Choice(Base):
  __tablename__ = "choices"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
  text: Mapped[str]
  is_correct: Mapped[bool]

  question = relationship("Question", back_populates="choices")
  user_answers = relationship(
    "UserAnswer",
    back_populates="choice",
    cascade="all, delete",
  )
