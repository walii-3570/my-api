from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_item():
    r = client.post("/items", json={"name": "Widget", "price": 9.99})
    assert r.status_code == 201
    assert r.json()["item"]["name"] == "Widget"

def test_get_item():
    create = client.post("/items", json={"name": "Keyboard", "price": 79.99})
    item_id = create.json()["id"]
    r = client.get(f"/items/{item_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "Keyboard"

def test_get_item_not_found():
    r = client.get("/items/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Item not found"

def test_update_item():
    create = client.post("/items", json={"name": "Old", "price": 1.0})
    item_id = create.json()["id"]

    r = client.put(f"/items/{item_id}",
                   json={"name": "New", "price": 2.0})
    assert r.status_code == 200
    assert r.json()["item"]["name"] == "New"
    
def test_delete_item():
    create = client.post("/items", json={"name": "ToDelete", "price": 5.0})
    item_id = create.json()["id"]

    r = client.delete(f"/items/{item_id}")
    assert r.status_code == 200

    r2 = client.get(f"/items/{item_id}")
    assert r2.status_code == 404

def test_create_item_invalid():
    r = client.post("/items", json={"name": "Bad", "price": "free"})
    assert r.status_code == 422  # Pydantic rejects "free" as a price