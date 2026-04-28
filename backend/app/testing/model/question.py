from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import Base


class Question(Base):
  __tablename__ = "question"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  text: Mapped[str]
  test_id: Mapped[int] = mapped_column(ForeignKey("test.id"))

  test = relationship("Test", back_populates="questions")
  choices = relationship(
    "Choice",
    back_populates="question",
    cascade="all, delete",
    order_by="Choice.id", 
  )
