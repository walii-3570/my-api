from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

db: dict[int, Item] = {}
next_id = 0

# CREATE ──────────────────────────────────
@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    db[next_id] = item
    created_id = next_id
    next_id += 1
    return {"id": created_id, "item": item}

# READ (all) ──────────────────────────────
@app.get("/items")
def list_items():
    return db

# READ (one) ──────────────────────────────
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

# UPDATE ──────────────────────────────────
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item
    return {"id": item_id, "item": item}

# DELETE ──────────────────────────────────
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"message": f"Item {item_id} deleted"}