from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, func
from sqlalchemy import String, BigInteger, ForeignKey, Enum
from sqlalchemy_utils.types.choice import ChoiceType
from datetime import datetime
from app.admin.enum.permission_mode import PermissionMode


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    mode: Mapped[PermissionMode] = mapped_column(Enum(PermissionMode, name="permission_mode"))