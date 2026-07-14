import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from databasemodels import Base, Product

# Use a file-based SQLite database for testing to ensure connection persistence
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    # Seed some initial data
    db = TestingSessionLocal()
    p1 = Product(id=1, name="Test Laptop", price=999, quantity=10, description="High performance")
    p2 = Product(id=2, name="Test Phone", price=499, quantity=20, description="Sleek phone")
    db.add(p1)
    db.add(p2)
    db.commit()
    db.close()
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

def test_greet():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "welcome to the world of programming!"

def test_get_all_products():
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test Laptop"
    assert data[1]["name"] == "Test Phone"

def test_get_product_by_id():
    # Test valid product
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Laptop"

    # Test invalid product
    response = client.get("/products/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Product not found"}

def test_add_product():
    new_product = {
        "id": 3,
        "name": "Tablet",
        "price": 299,
        "quantity": 15,
        "description": "Portable tablet"
    }
    response = client.post("/products", json=new_product)
    assert response.status_code == 200
    assert response.json()["name"] == "Tablet"

    # Verify it was added to the DB
    response = client.get("/products/3")
    assert response.status_code == 200
    assert response.json()["name"] == "Tablet"

def test_update_product():
    updated_info = {
        "id": 1,
        "name": "Updated Laptop",
        "price": 1099,
        "quantity": 5,
        "description": "Updated description"
    }
    response = client.put("/products/1", json=updated_info)
    assert response.status_code == 200
    assert response.json() == "Product Updated"

    # Verify details are updated
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Laptop"
    assert response.json()["price"] == 1099
    assert response.json()["quantity"] == 5

def test_update_product_not_found():
    updated_info = {
        "id": 999,
        "name": "Nonexistent",
        "price": 100,
        "quantity": 1,
        "description": "No desc"
    }
    response = client.put("/products/999", json=updated_info)
    assert response.status_code == 200
    assert response.json() == "No Product found"

def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 200
    assert response.json() == "Product deleted successfully"

    # Verify it's no longer in the DB
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json() == {"error": "Product not found"}

def test_delete_product_not_found():
    response = client.delete("/products/999")
    assert response.status_code == 200
    assert response.json() == "Product not found"
