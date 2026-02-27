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
import httpx
import zeep
import grpc
import sys
import os

# Add logistics to path to import generated protobufs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logistics/mock-server')))
import warehouse_pb2
import warehouse_pb2_grpc

# ---------------------------------------------------------------------------
# Backend Service URLs
# ---------------------------------------------------------------------------
REST_URL = "http://localhost:8002/inventory"
SOAP_WSDL = "http://localhost:8001/?wsdl"
GRPC_TARGET = "localhost:50051"


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

# ---------------------------------------------------------------------------
# Backend Fetchers
# ---------------------------------------------------------------------------

def fetch_rest_inventory(store_id: str = None) -> list[InventoryItem]:
    try:
        with httpx.Client() as client:
            resp = client.get(REST_URL)
            if resp.status_code == 200:
                data = resp.json()
                items = [
                    InventoryItem(
                        sku=item["sku"],
                        name=item["name"],
                        category=item["category"],
                        quantity=item["quantity"],
                        price_cents=item["price_cents"]
                    ) for item in data if (not store_id or item.get("store_id") == store_id)
                ]
                return items
    except Exception as e:
        print(f"REST fetch error: {e}")
    return []


def fetch_soap_orders(store_id: str) -> list[Order]:
    try:
        client = zeep.Client(wsdl=SOAP_WSDL)
        resp = client.service.GetRecentOrders(request={'storeId': store_id})
        if resp:
            orders_data = getattr(resp, "PurchaseOrder", getattr(resp, "orders", []))
            if orders_data:
                if not getattr(orders_data, "__iter__", False) or isinstance(orders_data, dict):
                    orders_data = [orders_data]
                
                orders = []
                for o in orders_data:
                    # Robust parsing for Spyne's nested items
                    item_count = 0
                    items_obj = getattr(o, "items", None)
                    if items_obj:
                        order_items = getattr(items_obj, "OrderItem", items_obj)
                        if order_items:
                            if getattr(order_items, "__iter__", False) and not isinstance(order_items, str):
                                item_count = len(list(order_items))
                            else:
                                item_count = 1

                    orders.append(Order(
                        id=getattr(o, "order_id", "UNKNOWN"),
                        supplier_id=getattr(o, "supplier_org_id", "UNKNOWN"),
                        status=OrderStatus.PENDING,
                        total_price_cents=item_count * 1000, 
                        item_count=item_count,
                        order_date=str(getattr(o, "order_date", "UNKNOWN")),
                        estimated_delivery=None
                    ))
                return orders
    except Exception as e:
        print(f"SOAP fetch error: {e}")
    return []


def fetch_grpc_robots(store_id: str) -> list[RobotTelemetry]:
    try:
        # In a real scenario, you might filter robots by store_id
        # For the demo, we just fetch a single status for a robot ID derived from the store_id
        robot_id = f"ROBOT-{store_id[-2:]}"
        with grpc.insecure_channel(GRPC_TARGET) as channel:
            stub = warehouse_pb2_grpc.WarehouseAutomationStub(channel)
            req = warehouse_pb2.RobotRequest(robot_id=robot_id)
            resp = stub.GetRobotStatus(req)
            
            # Map enum to our GraphQL enum
            status_map = {
                warehouse_pb2.ROBOT_STATUS_IDLE: RobotStatus.IDLE,
                warehouse_pb2.ROBOT_STATUS_MOVING: RobotStatus.MOVING,
                warehouse_pb2.ROBOT_STATUS_PICKING: RobotStatus.PICKING,
                warehouse_pb2.ROBOT_STATUS_CHARGING: RobotStatus.CHARGING,
                warehouse_pb2.ROBOT_STATUS_ERROR: RobotStatus.ERROR,
            }
            
            return [
                RobotTelemetry(
                    robot_id=resp.robot_id,
                    x=resp.position.x,
                    y=resp.position.y,
                    z=resp.position.z,
                    battery_level=resp.battery_level,
                    status=status_map.get(resp.status, RobotStatus.IDLE)
                )
            ]
    except Exception as e:
        print(f"gRPC fetch error: {e}")
    return []


STORE_DIRECTORY = [
    {"id": "STORE-PARIS-01", "name": "RetailSync Paris - Le Marais", "city": "Paris", "country": "France"},
    {"id": "STORE-BERLIN-02", "name": "RetailSync Berlin - Mitte", "city": "Berlin", "country": "Germany"},
]

def build_store(store_data: dict) -> Store:
    store_id = store_data["id"]
    return Store(
        id=strawberry.ID(store_id),
        name=store_data["name"],
        city=store_data["city"],
        country=store_data["country"],
        inventory=fetch_rest_inventory(store_id),
        orders=fetch_soap_orders(store_id),
        robots=fetch_grpc_robots(store_id)
    )


# ---------------------------------------------------------------------------
# Root query
# ---------------------------------------------------------------------------

@strawberry.type
class Query:

    @strawberry.field
    def stores(self) -> list[Store]:
        """List all stores with nested inventory, orders, and robots by calling backend APIs."""
        return [build_store(s) for s in STORE_DIRECTORY]

    @strawberry.field
    def store(self, id: strawberry.ID) -> Optional[Store]:
        """Fetch a single store by dynamically assembling data from REST, SOAP, and gRPC."""
        for s in STORE_DIRECTORY:
            if s["id"] == str(id):
                return build_store(s)
        return None

    @strawberry.field
    def dashboard_summary(self) -> DashboardSummary:
        """Aggregated KPIs across all stores."""
        all_stores = [build_store(s) for s in STORE_DIRECTORY]
        all_inventory = [item for store in all_stores for item in store.inventory]
        all_orders = [order for store in all_stores for order in store.orders]
        all_robots = [robot for store in all_stores for robot in store.robots]

        low_stock = [item for item in all_inventory if item.quantity < 10]

        return DashboardSummary(
            total_stores=len(all_stores),
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
    title="RetailSync - Manager Dashboard (GraphQL)",
    description="GraphQL aggregator gateway for store managers.",
    version="1.0.0",
)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    print("=" * 60)
    print("  RetailSync - GraphQL Dashboard")
    print("=" * 60)
    print("  GraphQL endpoint : http://localhost:8003/graphql")
    print("  GraphiQL IDE     : http://localhost:8003/graphql")
    print("  Protocol         : GraphQL over HTTP")
    print("=" * 60)
    print()

    uvicorn.run(app, host="0.0.0.0", port=8003)
