from common.model import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, func
from typing import Optional

class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    hash_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    uid: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    archived: Mapped[bool] 
    registered: Mapped[bool]
    has_eighteen_months: Mapped[bool]
    ms_created: Mapped[datetime]
    ms_updated: Mapped[datetime]
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.timezone("UTC", func.now()),
        server_default=func.timezone("UTC", func.now())
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.timezone("UTC", func.now())
    )