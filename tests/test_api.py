import os
import pytest

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database import get_db, Base

"""
Jack Notes: I orginally went for sqlite testing, but ran into issues with UUID generation and table creation.
So wired up PostgreSQL test database, which would be more alike to production and also
resolves the issues I was facing with SQLite, which would have changed the models/database
"""

load_dotenv()

TESTDB_URL = os.getenv("TESTDB_URL")
test_engine = create_engine(TESTDB_URL)

TestSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine
)

Base.metadata.drop_all(bind=test_engine)
Base.metadata.create_all(bind=test_engine)

# Override get_db to use test sessions
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Ensure clean state for each test

@pytest.fixture(autouse=True)
def cleanup_items():
    with TestSessionLocal() as db:
        db.execute(text(f"DELETE FROM items"))
        db.commit()
    yield
    with TestSessionLocal() as db:
        db.execute(text(f"DELETE FROM items"))
        db.commit()

client = TestClient(app)

# Health Tests
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_items_empty():
    response = client.get("/api/items")
    assert response.status_code == 200
    assert response.json() == []

def test_404_not_found():
    response = client.get("/bad-endpoint")
    assert response.status_code == 404

# Crud tests

def test_create_item():
    response = client.post("/api/items", json={"name": "Drum Kit"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Drum Kit"
    assert len(data["id"]) == 36

def test_list_items():
    client.post("/api/items", json={"name": "Item 1"})
    response = client.get("/api/items")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_delete_item():
    post_resp = client.post("/api/items", json={"name": "To Delete"})
    item_id = post_resp.json()["id"]
    del_resp = client.delete(f"/api/items/{item_id}")
    assert del_resp.status_code == 200
    assert "To Delete" in del_resp.json()["message"]
    get_resp = client.get("/api/items")
    assert len(get_resp.json()) == 0

def test_delete_not_found():
    response = client.delete("/api/items/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404