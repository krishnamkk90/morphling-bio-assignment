# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine
from app.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///:test.db:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    client = TestClient(app)
    yield client


def test_create_user(client):
    # Test user creation API
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "role": "developer",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "developer"


def test_token_generation(client):
    client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "role": "developer",
            "password": "password123"
        }
    )
    response = client.post(
        "/token",
        data={"username": "testuser@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_protected_route(client):
    client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "role": "developer",
            "password": "password123"
        }
    )
    response = client.post(
        "/token",
        data={"username": "testuser@example.com", "password": "password123"}
    )
    token = response.json()["access_token"]

    response = client.get(
        "/secure-data",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "This is a protected resource"}


def test_invalid_token(client):
    response = client.get(
        "/secure-data",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}
