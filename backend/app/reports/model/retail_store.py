from sqlalchemy import String, UUID, func, ForeignKey
from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class RetailStore(Base):
    __tablename__ = "retail_store"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    short_name: Mapped[str] = mapped_column(String(255), nullable=True)
    store_id: Mapped[str] = mapped_column(ForeignKey("store.id"))
    archived: Mapped[bool]
    ms_updated: Mapped[datetime]

    store: Mapped["Store"] = relationship( # type: ignore
        "Store", back_populates="retail_stores") 
    
    custom_inventory: Mapped["CustomInventory"] = relationship( # type: ignore
        "CustomInventory", back_populates="retail_store")