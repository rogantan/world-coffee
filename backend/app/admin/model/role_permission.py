from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey, Enum
from sqlalchemy_utils.types.choice import ChoiceType
from datetime import datetime
from app.admin.enum.permission_mode import PermissionMode


class RolePermission(Base):
    __tablename__ = "role_permission"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    mode: Mapped[PermissionMode] = mapped_column(Enum(PermissionMode, name="permission_mode"))

    role: Mapped["Role"] = relationship(  # type: ignore
        "Role", back_populates="role_permissions"
    )
    report: Mapped["Report"] = relationship(  # type: ignore
        "Report", back_populates="role_permission"
    )