from pydantic import BaseModel
from uuid import UUID

class RetailStoreSchema(BaseModel):
    name: str