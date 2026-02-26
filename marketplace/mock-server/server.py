"""
REST Mock Server - Partner Marketplace Inventory API

Implements the endpoints defined in contracts/openapi.yaml using FastAPI.
Uses an in-memory inventory list that resets on restart.

Run:     python marketplace/mock-server/server.py
Swagger: http://localhost:8002/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn


# ---------------------------------------------------------------------------
# Models (mirror the schemas in openapi.yaml)
# ---------------------------------------------------------------------------

class InventoryItem(BaseModel):
    """A single product in the marketplace inventory."""
    sku: str
    name: str
    category: str
    quantity: int
    price_cents: int
    store_id: str


class InventoryUpdate(BaseModel):
    """Partial update payload. Only provided fields are applied."""
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    price_cents: Optional[int] = None


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

inventory_db: list[InventoryItem] = [
    InventoryItem(
        sku="SKU001", name="Urban Wool Jacket - Black, L",
        category="jackets", quantity=150, price_cents=4500,
        store_id="STORE-PARIS-01",
    ),
    InventoryItem(
        sku="SKU002", name="RetroFlex Sneaker - White, EU 42",
        category="sneakers", quantity=320, price_cents=3200,
        store_id="STORE-PARIS-01",
    ),
    InventoryItem(
        sku="SKU003", name="Cashmere Scarf - Navy",
        category="accessories", quantity=80, price_cents=2800,
        store_id="STORE-BERLIN-02",
    ),
    InventoryItem(
        sku="SKU004", name="Organic Cotton T-Shirt - Grey, M",
        category="tops", quantity=500, price_cents=1200,
        store_id="STORE-LONDON-03",
    ),
    InventoryItem(
        sku="SKU005", name="Leather Messenger Bag - Brown",
        category="bags", quantity=45, price_cents=8900,
        store_id="STORE-BERLIN-02",
    ),
]


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="OmniChain Retail Mesh - Partner Marketplace API",
    description="REST API for third-party boutiques to synchronise inventory.",
    version="1.0.0",
)


def find_item(sku: str) -> InventoryItem | None:
    for item in inventory_db:
        if item.sku == sku:
            return item
    return None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/inventory", response_model=list[InventoryItem],
         summary="List all inventory items")
def list_inventory(category: Optional[str] = None):
    """Returns the full inventory list, optionally filtered by category."""
    if category:
        return [item for item in inventory_db if item.category == category]
    return inventory_db


@app.get("/inventory/{sku}", response_model=InventoryItem,
         summary="Get a single inventory item by SKU")
def get_inventory_item(sku: str):
    """Returns one item identified by its SKU."""
    item = find_item(sku)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item '{sku}' not found")
    return item


@app.patch("/inventory/{sku}", response_model=InventoryItem,
           summary="Partially update an inventory item")
def update_inventory_item(sku: str, update: InventoryUpdate):
    """Applies a partial update to an existing inventory item."""
    item = find_item(sku)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item '{sku}' not found")

    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    return item


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  OmniChain Retail Mesh - REST Marketplace API")
    print("=" * 60)
    print("  API endpoint  : http://localhost:8002")
    print("  Swagger UI    : http://localhost:8002/docs")
    print("  OpenAPI spec  : http://localhost:8002/openapi.json")
    print("  Protocol      : REST / JSON over HTTP")
    print("=" * 60)
    print()

    uvicorn.run(app, host="0.0.0.0", port=8002)
