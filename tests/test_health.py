from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    """Test main health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_db_health():
    """Test database health endpoint."""
    response = client.get("/health/db")
    assert response.status_code == 200
    data = response.json()
    assert "db" in data
    assert data["db"] == "ok"
