from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.model import Base
from app.admin.enum.permission_mode import PermissionMode

class Report(Base):
    __tablename__ = "report"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    display_name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    mode: Mapped[PermissionMode] = mapped_column(Enum(PermissionMode, name="permission_mode"))

    permission: Mapped["Permission"] = relationship(  # type: ignore
        "Permission", back_populates="report"
    )