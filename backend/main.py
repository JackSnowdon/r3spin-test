from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel

from backend import models, schemas
from backend.database import engine, Base, get_db




# Defining Item Model
"""
 - A persistent `Item` concept with at least:
    - `id`: unique identifier (number or string)
    - `name`: string
"""
class Item(BaseModel):
    id: str
    name: str


app = FastAPI(title="Tech Test API", version="0.1.0")

# Create database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/items")
def list_items(db: Session = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented")


@app.post("/api/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = models.ItemModel(name=item.name)

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented")


# testing database connection
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Simple query to test connection
        result = db.execute(text("SELECT 1 as alive")).fetchone()
        return {"status": "DB connected!", "result": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
