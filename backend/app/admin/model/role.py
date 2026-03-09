from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    users: Mapped[list["User"]] = relationship( # type: ignore
        "User", back_populates="role"
    )
    role_permissions: Mapped[list["RolePermission"]] = relationship( # type: ignore
        "RolePermission", back_populates="role"
    )