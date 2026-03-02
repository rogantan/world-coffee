from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, func
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy_utils.types.choice import ChoiceType
from datetime import datetime


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    mode: Mapped[ChoiceType["displayed", "hidden", "editable"]] = mapped_column(String(255))