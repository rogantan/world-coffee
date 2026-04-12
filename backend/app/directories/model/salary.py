from common.model import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, ForeignKey

class SalaryCondition(Base):
  __tablename__ = "salary_condition"

  id: Mapped[int] = mapped_column(primary_key=True)
  retail_store_id: Mapped[str] = mapped_column(ForeignKey("retail_store.id"))
  salary_per_shift: Mapped[float] = mapped_column(Float)