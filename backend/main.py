from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import engine, Base, get_db

from pydantic import BaseModel


# Defining Item Model
"""
 - A persistent `Item` concept with at least:
    - `id`: unique identifier (number or string)
    - `name`: string
"""
class Item(BaseModel):
    id: int
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
def list_items():
    raise HTTPException(status_code=501, detail="Not implemented")


@app.post("/api/items")
def create_item():
    raise HTTPException(status_code=501, detail="Not implemented")


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
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
