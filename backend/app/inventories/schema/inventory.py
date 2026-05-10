from pydantic import BaseModel

class SInventoryEdit(BaseModel):
  actual_balance: int
  sales: int

class SInventory(SInventoryEdit):
  id: int
  product_name: str
  price: float | int
  closing_balance: int = 0