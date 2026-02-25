from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from pydantic import BaseModel
from uuid import UUID

from backend import models, schemas
from backend.database import engine, Base, get_db

app = FastAPI(title="Tech Test API", version="0.1.0")

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS configuration to allow requests from local origins 
# Would not be the case in production !!!

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "HTTP://localhost:8000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/items", response_model=List[schemas.Item])
def list_items(db: Session = Depends(get_db)):
    return db.query(models.ItemModel).all()


@app.post("/api/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = models.ItemModel(name=item.name)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/items/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.ItemModel).filter(models.ItemModel.id == UUID(item_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item ({item_id}) not found")

    db.delete(item)
    db.commit()
    return {"message": f"Item '{item.name}' has been deleted"}


# Testing database connection
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Simple query to test connection
        result = db.execute(text("SELECT 1 as alive")).fetchone()
        return {"status": "DB connected!", "result": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
