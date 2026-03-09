from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, BigInteger, ForeignKey, func, UUID
from datetime import datetime
import uuid

class Store(Base):
    __tablename__ = "store"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String(255))
    archived: Mapped[bool]
    ms_updated: Mapped[datetime]
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.timezone("UTC", func.now()),
        server_default=func.timezone("UTC", func.now()),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.timezone("UTC", func.now())
    )

    retail_stores = relationship("RetailStore", back_populates="store")