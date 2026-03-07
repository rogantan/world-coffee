# from app.admin.model.user import User
from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, BigInteger, ForeignKey, func
from datetime import datetime

class SalaryIncrease(Base):
    __tablename__ = "salary_increase"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    value: Mapped[float] = mapped_column(Float, default=1, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.timezone("UTC", func.now())
    )
    user: Mapped["User"] = relationship( # type: ignore
        "User", back_populates="salary_increase"
    )