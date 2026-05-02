from datetime import datetime

from sqlalchemy import (
  JSON,
  Computed,
  ForeignKey,
  func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import MappedBase

class CustomInventoryItem(MappedBase):
  __tablename__ = "custom_inventory_item"

  id: Mapped[int] = mapped_column(primary_key=True)
  custom_inventory_id: Mapped[int] = mapped_column(ForeignKey("custom_inventory.id"))
  product_name: Mapped[str]
  price: Mapped[float]
  actual_balance: Mapped[int] = mapped_column(default=0, server_default="0")
  sales: Mapped[int] = mapped_column(default=0, server_default="0")
  closing_balance: Mapped[int] = mapped_column(
    Computed("actual_balance - sale1 - sale2 - sale3 - sale4")
  )
  meta: Mapped[dict] = mapped_column(JSON)
  updated_at: Mapped[datetime] = mapped_column(
    onupdate=func.timezone("UTC", func.now()),
    server_default=func.timezone("UTC", func.now()),
  )
  created_at: Mapped[datetime] = mapped_column(
    server_default=func.timezone("UTC", func.now())
  )

  custom_inventory: Mapped["CustomInventory"] = relationship(  # type: ignore
    "CustomInventory", back_populates="custom_inventory_items"
  )
