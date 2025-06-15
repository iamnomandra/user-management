import pytest
from fastapi.testclient import TestClient
from src.main import app
from motor.motor_asyncio import AsyncIOMotorClient
from src.database import db

user_collection = db.getdb.User

@pytest.fixture(scope="module")
async def test_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    test_db = client.test_cart_db
    yield test_db
    await client.drop_database("test_cart_db")

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.mark.asyncio
async def test_read_user(client):
    response = client.post("/users/", json={})
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Tablet"