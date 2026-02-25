from pydantic import BaseModel, Field
from uuid import UUID

# Input schema for creating an item, only accepts name as id automatically generated
class ItemCreate(BaseModel):
    name: str = Field(..., example="User ID", max_length=255)

class Item(ItemCreate):
    id: UUID

    class Config:
        from_attributes = True #SQLAlchemy ItemModel → Pydantic response