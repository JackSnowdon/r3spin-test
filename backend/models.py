from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

"""
Jack Notes, Used UUID to generate unique ID's, Name originally set to unique to prevent duplicates,
but could be removed for a more flexible API. Would also add created_at and updated_at timestamps in a production environment.
"""

# SQLAlchemy model for the items table

class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("gen_random_uuid()")
    )
    name = Column(
        String(255), 
        index=True, 
        unique=True
    )