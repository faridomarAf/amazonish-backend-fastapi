from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_order_and_reserve_inventory():
    # Assuming a user and a SKU with inventory exist
    # Create order
    response = client.post("/orders", json={
        "customer_id": 1,
        "items": [{"sku_id": 1, "qty": 2}]
    })
    assert response.status_code == 201
    data = response.json()
    assert "order_id" in data

    # Check inventory reserved
    response = client.get("/catalog/inventory/1")
    assert response.status_code == 200
    inventory = response.json()
    assert inventory["reserved"] == 2
