from datetime import datetime

from sqlalchemy import (
  ForeignKey,
  func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.inventories.model.custom_inventory_item import CustomInventoryItem
from common.model import MappedBase

class CustomInventory(MappedBase):
  __tablename__ = "custom_inventory"

  id: Mapped[int] = mapped_column(primary_key=True)
  retail_store_id: Mapped[str] = mapped_column(ForeignKey("retail_store.id"))
  updated_at: Mapped[datetime] = mapped_column(
    onupdate=func.timezone("UTC", func.now()),
    server_default=func.timezone("UTC", func.now()),
  )
  unloaded: Mapped[bool] = mapped_column(default=False, server_default="false")
  created_at: Mapped[datetime] = mapped_column(
    server_default=func.timezone("UTC", func.now())
  )

  retail_store: Mapped["RetailStore"] = relationship("RetailStore", back_populates="custom_inventory")  # type: ignore

  custom_inventory_items: Mapped[list[CustomInventoryItem]] = relationship(  # type: ignore
    "CustomInventoryItem",
    back_populates="custom_inventory",
    cascade="all, delete",
  )
