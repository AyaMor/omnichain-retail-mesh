"""
GraphQL Mock Server - Manager Dashboard (Aggregator Pattern)

Implements the schema defined in contracts/schema.graphql using Strawberry.
All resolvers return static data. In production, each resolver would fan
out to a different backend service (REST, SOAP, gRPC).

Run:      python dashboard/mock-server/server.py
GraphiQL: http://localhost:8003/graphql
"""

import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from enum import Enum
from typing import Optional
import uvicorn


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

@strawberry.enum
class OrderStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


@strawberry.enum
class RobotStatus(Enum):
    IDLE = "IDLE"
    MOVING = "MOVING"
    PICKING = "PICKING"
    CHARGING = "CHARGING"
    ERROR = "ERROR"


# ---------------------------------------------------------------------------
# GraphQL types (mirror the types in schema.graphql)
# ---------------------------------------------------------------------------

@strawberry.type
class InventoryItem:
    """Product in the store's inventory."""
    sku: str
    name: str
    category: str
    quantity: int
    price_cents: int


@strawberry.type
class Order:
    """Procurement order placed with a manufacturer."""
    id: str
    supplier_id: str
    status: OrderStatus
    total_price_cents: int
    item_count: int
    order_date: str
    estimated_delivery: Optional[str] = None


@strawberry.type
class RobotTelemetry:
    """Real-time robot position and status."""
    robot_id: str
    x: float
    y: float
    z: float
    battery_level: float
    status: RobotStatus


@strawberry.type
class Store:
    """Aggregated store entity nesting data from three backend systems."""
    id: strawberry.ID
    name: str
    city: str
    country: str
    inventory: list[InventoryItem]
    orders: list[Order]
    robots: list[RobotTelemetry]


@strawberry.type
class DashboardSummary:
    """Cross-store KPI aggregation."""
    total_stores: int
    total_skus: int
    total_orders_pending: int
    total_robots_active: int
    low_stock_alerts: list[InventoryItem]


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_STORES = [
    Store(
        id=strawberry.ID("STORE-PARIS-01"),
        name="OmniChain Paris - Le Marais",
        city="Paris",
        country="France",
        inventory=[
            InventoryItem(sku="SKU001", name="Urban Wool Jacket - Black, L",
                          category="jackets", quantity=150, price_cents=4500),
            InventoryItem(sku="SKU002", name="RetroFlex Sneaker - White, EU 42",
                          category="sneakers", quantity=320, price_cents=3200),
            InventoryItem(sku="SKU003", name="Cashmere Scarf - Navy",
                          category="accessories", quantity=8, price_cents=2800),
        ],
        orders=[
            Order(id="PO-2026-0042", supplier_id="MFG-SHENZHEN-008",
                  status=OrderStatus.CONFIRMED, total_price_cents=6090000,
                  item_count=2, order_date="2026-02-26",
                  estimated_delivery="2026-03-12"),
            Order(id="PO-2026-0039", supplier_id="MFG-MILAN-003",
                  status=OrderStatus.SHIPPED, total_price_cents=1240000,
                  item_count=1, order_date="2026-02-20",
                  estimated_delivery="2026-03-01"),
        ],
        robots=[
            RobotTelemetry(robot_id="ROBOT-P01-A", x=12.5, y=3.2, z=0.0,
                            battery_level=0.87, status=RobotStatus.PICKING),
            RobotTelemetry(robot_id="ROBOT-P01-B", x=8.1, y=14.7, z=0.0,
                            battery_level=0.23, status=RobotStatus.CHARGING),
        ],
    ),
    Store(
        id=strawberry.ID("STORE-BERLIN-02"),
        name="OmniChain Berlin - Mitte",
        city="Berlin",
        country="Germany",
        inventory=[
            InventoryItem(sku="SKU004", name="Organic Cotton T-Shirt - Grey, M",
                          category="tops", quantity=500, price_cents=1200),
            InventoryItem(sku="SKU005", name="Leather Messenger Bag - Brown",
                          category="bags", quantity=3, price_cents=8900),
        ],
        orders=[
            Order(id="PO-2026-0041", supplier_id="MFG-SHENZHEN-008",
                  status=OrderStatus.PENDING, total_price_cents=890000,
                  item_count=1, order_date="2026-02-25"),
        ],
        robots=[
            RobotTelemetry(robot_id="ROBOT-B02-A", x=5.0, y=5.0, z=1.2,
                            battery_level=0.95, status=RobotStatus.MOVING),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Root query
# ---------------------------------------------------------------------------

@strawberry.type
class Query:

    @strawberry.field
    def stores(self) -> list[Store]:
        """List all stores with nested inventory, orders, and robots."""
        return MOCK_STORES

    @strawberry.field
    def store(self, id: strawberry.ID) -> Optional[Store]:
        """Fetch a single store by ID."""
        for s in MOCK_STORES:
            if s.id == id:
                return s
        return None

    @strawberry.field
    def dashboard_summary(self) -> DashboardSummary:
        """Aggregated KPIs across all stores."""
        all_inventory = [item for store in MOCK_STORES for item in store.inventory]
        all_orders = [order for store in MOCK_STORES for order in store.orders]
        all_robots = [robot for store in MOCK_STORES for robot in store.robots]

        low_stock = [item for item in all_inventory if item.quantity < 10]

        return DashboardSummary(
            total_stores=len(MOCK_STORES),
            total_skus=len(all_inventory),
            total_orders_pending=sum(
                1 for o in all_orders if o.status == OrderStatus.PENDING
            ),
            total_robots_active=sum(
                1 for r in all_robots if r.status != RobotStatus.IDLE
            ),
            low_stock_alerts=low_stock,
        )


# ---------------------------------------------------------------------------
# Application wiring
# ---------------------------------------------------------------------------

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI(
    title="OmniChain Retail Mesh - Manager Dashboard (GraphQL)",
    description="GraphQL aggregator gateway for store managers.",
    version="1.0.0",
)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    print("=" * 60)
    print("  OmniChain Retail Mesh - GraphQL Dashboard")
    print("=" * 60)
    print("  GraphQL endpoint : http://localhost:8003/graphql")
    print("  GraphiQL IDE     : http://localhost:8003/graphql")
    print("  Protocol         : GraphQL over HTTP")
    print("=" * 60)
    print()

    uvicorn.run(app, host="0.0.0.0", port=8003)
