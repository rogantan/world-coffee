from datetime import datetime
import uuid
from typing import Optional

from sqlalchemy import (
  UUID,
  ForeignKey,
  String,
  UniqueConstraint,
  func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import MappedBase


class Inventory(MappedBase):
  __tablename__ = "inventory"

  id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
  ms_id: Mapped[Optional[str]] = mapped_column(UUID)
  store_id: Mapped[str] = mapped_column(ForeignKey("store.id"))
  salesman_id: Mapped[Optional[str]] = mapped_column(ForeignKey("user.id"))

  positive_correction_sum: Mapped[float]
  negative_correction_sum: Mapped[float]
  manual_changes: Mapped[float] = mapped_column(default=0, server_default="0")
  retention_sum: Mapped[float] = mapped_column(server_default="0")

  name: Mapped[str] = mapped_column(String(255))
  uuid_href: Mapped[str] = mapped_column(String(255))

  moment: Mapped[datetime]
  ms_updated: Mapped[datetime]
  updated_at: Mapped[datetime] = mapped_column(
    onupdate=func.timezone("UTC", func.now()),
    server_default=func.timezone("UTC", func.now()),
  )
  created_at: Mapped[datetime] = mapped_column(
    server_default=func.timezone("UTC", func.now())
  )

  store = relationship("Store", back_populates="inventories")

  __table_args__ = (
    UniqueConstraint("ms_id", "salesman_id", name="_ms_id_salesman_id_uc"),
  )
