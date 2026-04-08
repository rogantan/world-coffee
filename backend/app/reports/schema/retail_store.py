from pydantic import BaseModel
from uuid import UUID

class RetailStoreSchema(BaseModel):
    id: UUID
    name: str
    archived: bool