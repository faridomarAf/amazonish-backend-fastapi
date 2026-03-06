from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_product_and_inventory():
    # Create product
    response = client.post("/catalog/products", json={"name": "Laptop"})
    assert response.status_code == 201
    product_id = response.json()["id"]

    # Create SKU
    response = client.post("/catalog/skus", json={
        "product_id": product_id,
        "sku_code": "LAP123"
    })
    assert response.status_code == 201
    sku_id = response.json()["id"]

    # Initialize inventory
    response = client.post("/catalog/inventory", json={
        "sku_id": sku_id,
        "on_hand": 10
    })
    assert response.status_code == 201
