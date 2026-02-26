import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID  # Optional for prod
from sqlalchemy import text
from .database import Base
"""
Jack Notes, Used UUID to generate unique ID's, Name originally set to unique to prevent duplicates,
but could be removed for a more flexible API. Would also add created_at and updated_at timestamps in a production environment.

I have updated the test setup to drop and recreate tables for each test to ensure a clean state, 
and added debug logging to verify that the 'items' table is correctly registered in the metadata. 
This should help resolve the "no such table: items" error during testing.
"""

# SQLAlchemy model for the items table

class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        server_default=text('gen_random_uuid()'), # For PostgreSQL, use gen_random_uuid() for automatic UUID generation;
        # default=lambda: str(uuid.uuid4()) # For SQLite testing purposes, we generate UUIDs in Python;
    )
    name = Column(
        String(255), 
        index=True, 
        unique=True
    )