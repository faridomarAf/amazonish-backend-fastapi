from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_and_login():
    # Register new user
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 201

    # Login user
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
