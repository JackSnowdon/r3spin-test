import pytest
from fastapi.testclient import TestClient

from backend.models import ItemModel
from backend.main import app
from backend.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    print("Tables registered:", list(Base.metadata.tables.keys()))  # Debug: ['items']
    Base.metadata.drop_all(bind=test_engine)  # Clean first
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

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