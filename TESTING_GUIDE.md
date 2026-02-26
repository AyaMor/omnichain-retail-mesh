# Testing Guide -- OmniChain Retail Mesh

This guide walks you through starting every mock server, verifying each one from the terminal, and then importing and running the full Postman test suite.



## Prerequisites

- Python 3.10 or later installed
- pip installed
- Postman desktop application installed (download from https://www.postman.com/downloads)



## Step 1: Install Dependencies

Open a terminal at the project root (`projet-API/`) and run:

```bash
pip install -r procurement/requirements.txt
pip install -r marketplace/requirements.txt
pip install -r dashboard/requirements.txt
pip install -r logistics/requirements.txt
```

Then generate the gRPC Python stubs (one-time step):

```bash
python -m grpc_tools.protoc \
    -Ilogistics/contracts \
    --python_out=logistics/mock-server \
    --grpc_python_out=logistics/mock-server \
    logistics/contracts/warehouse.proto
```

---

## Step 2: Start All Servers

Open **four separate terminal windows**, each at the project root. Start one server per terminal:

**Terminal 1 -- SOAP Procurement (port 8001):**
```bash
python procurement/mock-server/server.py
```
Expected output:
```
============================================================
  OmniChain Retail Mesh - SOAP Procurement Service
============================================================
  SOAP endpoint : http://localhost:8001/
  WSDL          : http://localhost:8001/?wsdl
```

**Terminal 2 -- REST Marketplace (port 8002):**
```bash
python marketplace/mock-server/server.py
```
Expected output:
```
============================================================
  OmniChain Retail Mesh - REST Marketplace API
============================================================
  API endpoint  : http://localhost:8002
  Swagger UI    : http://localhost:8002/docs
```

**Terminal 3 -- GraphQL Dashboard (port 8003):**
```bash
python dashboard/mock-server/server.py
```
Expected output:
```
============================================================
  OmniChain Retail Mesh - GraphQL Dashboard
============================================================
  GraphQL endpoint : http://localhost:8003/graphql
```

**Terminal 4 -- gRPC Logistics (port 50051):**
```bash
python logistics/mock-server/server.py
```
Expected output:
```
============================================================
  OmniChain Retail Mesh - gRPC Warehouse Automation
============================================================
  gRPC endpoint  : localhost:50051
```

---

## Step 3: Verify from the Terminal

Open a **fifth terminal** and run these commands one by one.

### 3.1 REST -- List inventory

```bash
curl -s http://localhost:8002/inventory | python -m json.tool
```

Expected: a JSON array with 5 inventory items. Each item has `sku`, `name`, `category`, `quantity`, `price_cents`, `store_id`.

### 3.2 REST -- Get single item

```bash
curl -s http://localhost:8002/inventory/SKU001 | python -m json.tool
```

Expected: a single JSON object with `"sku": "SKU001"`.

### 3.3 REST -- Update stock (PATCH)

```bash
curl -s -X PATCH http://localhost:8002/inventory/SKU001 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 75}' | python -m json.tool
```

Expected: the same item with `"quantity": 75`.

### 3.4 GraphQL -- Aggregated store query

```bash
curl -s -X POST http://localhost:8003/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ stores { id name inventory { sku quantity } orders { id status } } }"}' \
  | python -m json.tool
```

Expected: a `data.stores` array with 2 stores, each containing nested `inventory` and `orders` arrays.

### 3.5 GraphQL -- Dashboard KPIs

```bash
curl -s -X POST http://localhost:8003/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ dashboardSummary { totalStores totalSkus totalOrdersPending lowStockAlerts { sku } } }"}' \
  | python -m json.tool
```

Expected: a `data.dashboardSummary` object with numeric KPIs and a `lowStockAlerts` array.

### 3.6 SOAP -- Submit purchase order

```bash
curl -s -X POST http://localhost:8001 \
  -H "Content-Type: text/xml" \
  -d @procurement/mock-server/test_request.xml
```

Expected: an XML SOAP envelope containing `<confirmation_id>CONF-PO-2026-0042-001</confirmation_id>` and `<status>ACCEPTED</status>`.

### 3.7 gRPC -- Run demo client

```bash
python logistics/mock-server/client.py
```

Expected: first a unary response with robot position and battery, then a stream of telemetry events as the robot executes MOVE, PICK, and CHARGE commands.


## Step 4: Import into Postman

### 4.1 Import the Environment

1. Open Postman.
2. Click the **Environments** tab in the left sidebar.
3. Click **Import**.
4. Select the file `postman/OmniChain_Environment.json` from the project directory.
5. You should see a new environment called **OmniChain Retail Mesh - Local** with four variables:
   - `baseUrl_rest` = `http://localhost:8002`
   - `baseUrl_graphql` = `http://localhost:8003`
   - `baseUrl_soap` = `http://localhost:8001`
   - `current_sku` = `SKU001`

### 4.2 Import the Collection

1. Click the **Collections** tab in the left sidebar.
2. Click **Import**.
3. Select the file `postman/OmniChain_Collection.json`.
4. You should see a collection called **OmniChain Retail Mesh - Full Lifecycle** with three folders:
   - Module 1: REST - Partner Marketplace (3 requests)
   - Module 2: GraphQL - Manager Dashboard (2 requests)
   - Module 3: SOAP - B2B Procurement (1 request)

### 4.3 Select the Environment

In the top-right corner of Postman, click the environment dropdown and select **OmniChain Retail Mesh - Local**. This activates the base URL variables used by all requests.

-

## Step 5: Run Individual Requests

Before running the full collection, test one request to confirm connectivity:

1. Expand **Module 1: REST - Partner Marketplace**.
2. Click **GET - List All Inventory**.
3. Click **Send**.
4. Verify:
   - Status: `200 OK`
   - Body: a JSON array of 5 items
   - Open the **Test Results** tab at the bottom -- all tests should show green check marks.



## Step 6: Run the Full Collection

1. Click the three dots next to the collection name and select **Run collection**.
2. In the Collection Runner window:
   - Ensure all 6 requests are checked.
   - Iterations: 1.
   - Delay: 0 ms.
3. Click **Run OmniChain Retail Mesh - Full Lifecycle**.
4. Wait for all requests to complete. You should see:
   - 6/6 requests completed
   - All test assertions passing (green check marks)
   - Total test count: approximately 30 assertions across all requests

### What each test validates

| Request | Test assertions |
|---|---|
| GET List Inventory | Status 200, response time < 200ms, non-empty array, SKU001 present, all required fields |
| GET Single Item | Status 200, response time < 200ms, correct SKU, all required fields |
| PATCH Update Stock | Status 200, response time < 200ms, correct SKU, quantity updated to 75 |
| GraphQL Stores Query | Status 200, response time < 200ms, data object present, no errors, stores array, nested inventory and orders |
| GraphQL Dashboard Summary | Status 200, response time < 200ms, KPI fields present, lowStockAlerts is array |
| SOAP SubmitOrder | Status 200, response time < 200ms, XML content type, confirmation_id present, ACCEPTED status, delivery date and total price |



## Step 7: Test gRPC in Postman

Postman handles gRPC through a dedicated interface, not standard HTTP requests.

### 7.1 Create a gRPC request

1. Click **New** in the top left.
2. Select **gRPC** (not HTTP).
3. In the server URL field, enter: `localhost:50051` (no `http://` prefix).

### 7.2 Import the proto file

1. In the **Service definition** section, click **Import .proto file**.
2. Navigate to `logistics/contracts/warehouse.proto` and select it.
3. Postman will parse the file and populate the method dropdown with:
   - `WarehouseAutomation / GetRobotStatus`
   - `WarehouseAutomation / StreamTelemetry`

### 7.3 Test GetRobotStatus (Unary RPC)

1. Select **WarehouseAutomation / GetRobotStatus** from the method dropdown.
2. In the **Message** tab, enter:
   ```json
   {
     "robot_id": "ROBOT-P01-A"
   }
   ```
3. Click **Invoke**.
4. You should receive a response with:
   - `robot_id`: "ROBOT-P01-A"
   - `position`: x=12.5, y=3.2, z=0.0
   - `battery_level`: 0.87
   - `status`: ROBOT_STATUS_PICKING

### 7.4 Test StreamTelemetry (Bi-directional Streaming)

1. Select **WarehouseAutomation / StreamTelemetry** from the method dropdown.
2. Postman will show the streaming interface.
3. Enter the first message in the composer:
   ```json
   {
     "robot_id": "ROBOT-P01-A",
     "command": "COMMAND_MOVE",
     "target": { "x": 15.0, "y": 12.0, "z": 0.0 },
     "timestamp_ms": 1740564000000
   }
   ```
4. Click **Send** to push the message into the stream.
5. The server will respond with 3 telemetry events showing the robot moving toward the target.
6. You can send additional commands:
   ```json
   {
     "robot_id": "ROBOT-P01-A",
     "command": "COMMAND_PICK",
     "target": { "x": 15.0, "y": 12.0, "z": 2.5 },
     "payload_sku": "SKU-JACKET-BLK-L",
     "timestamp_ms": 1740564001000
   }
   ```
7. Click **End streaming** when finished.



## Troubleshooting

| Problem | Solution |
|---|---|
| `Connection refused` on any port | Make sure the corresponding server is running in its terminal |
| Port already in use | Kill the process: `lsof -ti:PORT_NUMBER \| xargs kill -9` |
| gRPC stubs not found | Re-run the `grpc_tools.protoc` command from Step 1 |
| Postman shows `Could not send request` | Verify the environment is selected (top-right dropdown) |
| SOAP returns 500 | Check the XML envelope matches the expected namespace `http://omnichain.retail/procurement` |
