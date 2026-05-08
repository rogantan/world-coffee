from pydantic import BaseModel

class SInventory(BaseModel):
  id: int
  product_name: str
  price: float | int
  actual_balance: int
  sales: int = 0
  closing_balance: int = 0