from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("gen_random_uuid()")
    )
    name = Column(
        String, 
        index=True, 
        unique=True
    )