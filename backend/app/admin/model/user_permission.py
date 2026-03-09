from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey, Enum
from sqlalchemy_utils.types.choice import ChoiceType
from datetime import datetime
from app.admin.enum.permission_mode import PermissionMode


class UserPermission(Base):
    __tablename__ = "user_permission"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    mode: Mapped[PermissionMode] = mapped_column(Enum(PermissionMode, name="permission_mode"))

    user: Mapped["User"] = relationship(  # type: ignore
        "User", back_populates="user_permissions"
    )
    report: Mapped["Report"] = relationship(  # type: ignore
        "Report", back_populates="user_permissions"
    )