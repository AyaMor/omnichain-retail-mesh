# OmniChain Retail Mesh -- Phase 1: Contracts and Mocks

A Proof-of-Concept demonstrating how a global retail brand orchestrates four distinct communication paradigms across its supply chain. Each paradigm was chosen to match the operational constraints and integration requirements of its respective domain.



## Architecture Overview

```
+---------------+--------------+---------------+----------------------+
|  SOAP / XML   |  REST / JSON |  GraphQL      |  gRPC / Protobuf     |
|  Port 8001    |  Port 8002   |  Port 8003    |  Port 50051          |
+---------------+--------------+---------------+----------------------+
|  procurement/ |  marketplace/|  dashboard/   |  logistics/          |
|               |              |               |                      |
|  B2B Purchase |  Partner     |  Manager      |  Warehouse Robot     |
|  Orders with  |  Inventory   |  Aggregated   |  Telemetry           |
|  Factories    |  Sync API    |  Dashboard    |  Bi-directional      |
|  (CN / EU)    |  (Boutiques) |  (Stores)     |  Streaming           |
+---------------+--------------+---------------+----------------------+
```



## Folder Structure

```
projet-API/
|-- README.md
|
|-- procurement/                       SOAP module
|   |-- contracts/
|   |   +-- PurchaseOrder.wsdl         WSDL contract (schema-first)
|   |-- mock-server/
|   |   |-- server.py                  Spyne SOAP server (mock)
|   |   +-- test_request.xml           Sample SOAP envelope for testing
|   +-- requirements.txt
|
|-- marketplace/                       REST module
|   |-- contracts/
|   |   +-- openapi.yaml               OpenAPI 3.0 specification (schema-first)
|   |-- mock-server/
|   |   +-- server.py                  FastAPI server (mock)
|   +-- requirements.txt
|
|-- dashboard/                         GraphQL module
|   |-- contracts/
|   |   +-- schema.graphql             GraphQL SDL (schema-first)
|   |-- mock-server/
|   |   +-- server.py                  Strawberry + FastAPI server (mock)
|   +-- requirements.txt
|
+-- logistics/                         gRPC module
    |-- contracts/
    |   +-- warehouse.proto            Protobuf IDL (schema-first)
    |-- mock-server/
    |   |-- server.py                  gRPC server (mock)
    |   +-- client.py                  Demo client for presentation
    +-- requirements.txt
```


## Technology Justification

### SOAP for B2B Procurement

Purchase orders exchanged with legacy manufacturers in China and Europe demand a protocol that enforces strict data contracts at the wire level. SOAP was selected for this module for the following reasons:

- **Strict XML Schema enforcement.** The WSDL embeds XSD definitions that guarantee every order contains the exact fields manufacturers expect. Unlike JSON, XML schemas enforce element ordering, occurrence constraints, and complex nested types through formal validation.
- **Formal contract-based integration.** The WSDL file serves as the single source of truth. Both our platform and the manufacturer generate client and server stubs from this artifact, eliminating ambiguity and reducing integration errors.
- **Enterprise system compatibility.** Many large manufacturers operate SAP, Oracle, or legacy ERP systems that communicate natively via SOAP and WS-* standards. Requiring them to adopt REST or GraphQL would create unnecessary friction in the B2B relationship.
- **WS-Security for message-level protection.** SOAP's envelope structure supports end-to-end encryption and digital signatures through WS-Security, which is critical when transmitting financial purchase orders across international borders.

### REST for Partner Marketplace

Third-party boutiques need a straightforward, well-understood API to synchronise inventory with our marketplace. REST was selected for this module for the following reasons:

- **Simplicity of integration.** HTTP verbs (GET, PATCH) map directly to inventory operations. Boutique development teams can integrate using curl, Postman, or any HTTP library without specialised toolkits or code generation.
- **Cacheability.** GET responses can be cached at CDN and reverse-proxy levels using standard HTTP headers. This is critical when thousands of boutiques poll for catalogue updates simultaneously.
- **Statelessness.** Each request is self-contained and carries all context needed for processing. There are no server-side sessions to manage, which makes the API horizontally scalable behind a load balancer.
- **Universal adoption.** REST is the most widely adopted API paradigm on the web. Small boutique teams with limited engineering resources can integrate within hours, not days.

### GraphQL for Manager Dashboard

Store managers need an aggregated view that pulls inventory, orders, and warehouse robot status into a single interface. GraphQL was selected for this module for the following reasons:

- **Solves the under-fetching problem.** With REST, assembling a complete dashboard view requires multiple sequential calls (store details, then inventory, then orders, then robot status). GraphQL collapses these into a single query with nested fields, reducing both latency and client-side complexity.
- **Client-driven field selection.** The manager's frontend requests only the fields it needs for each widget. A summary panel that only displays store names does not incur the cost of loading full inventory data, reducing bandwidth consumption.
- **Aggregator gateway pattern.** In production, each field resolver would fan out to a different backend service: inventory resolves via the REST module, orders via the SOAP module, and robot telemetry via the gRPC module. GraphQL unifies these heterogeneous sources behind a single, consistent schema.

### gRPC for Warehouse Logistics

Fulfillment robots streaming real-time telemetry require a protocol optimised for low latency and high throughput. gRPC was selected for this module for the following reasons:

- **Binary serialisation performance.** Protobuf messages are 3 to 10 times smaller than equivalent JSON payloads and significantly faster to serialise and deserialise. A RobotTelemetry message is approximately 40 bytes in Protobuf versus 250 bytes in JSON. At 100 robots transmitting 10 messages per second, this translates to 4 KB/s versus 25 KB/s of bandwidth.
- **Bi-directional streaming.** gRPC natively supports stream-to-stream RPCs over a single HTTP/2 connection. The warehouse controller streams commands to robots while simultaneously receiving telemetry from them, without the overhead of repeated HTTP request-response cycles.
- **Strong compile-time typing.** Protobuf enforces message structure at code-generation time. Both the robot firmware and the warehouse controller generate stubs from the same `.proto` file, eliminating an entire class of serialisation and compatibility bugs.
- **HTTP/2 multiplexing.** Multiple concurrent streams share a single TCP connection, reducing connection overhead in a warehouse with hundreds of active robots.



## Contract-First Design

Every module follows the same principle: the contract is defined before any implementation code is written.

1. **SOAP** -- `PurchaseOrder.wsdl` defines the XML schema and operations; the Spyne server implements them.
2. **REST** -- `openapi.yaml` defines the endpoints and data models; the FastAPI server implements them.
3. **GraphQL** -- `schema.graphql` defines the types and queries; the Strawberry server resolves them.
4. **gRPC** -- `warehouse.proto` defines the messages and services; the grpcio server implements them.

This guarantees that all parties (manufacturers, boutiques, store managers, warehouse controllers) agree on the data format before any integration work begins.



## Quick Start

### Prerequisites

- Python 3.10 or later
- pip

### Install and Run

Each module is self-contained. Open a separate terminal for each:

```bash
# 1. SOAP Procurement (port 8001)
pip install -r procurement/requirements.txt
python procurement/mock-server/server.py

# 2. REST Marketplace (port 8002)
pip install -r marketplace/requirements.txt
python marketplace/mock-server/server.py

# 3. GraphQL Dashboard (port 8003)
pip install -r dashboard/requirements.txt
python dashboard/mock-server/server.py

# 4. gRPC Logistics (port 50051)
pip install -r logistics/requirements.txt
# Generate Python stubs from the .proto file (one-time step)
python -m grpc_tools.protoc \
    -Ilogistics/contracts \
    --python_out=logistics/mock-server \
    --grpc_python_out=logistics/mock-server \
    logistics/contracts/warehouse.proto
python logistics/mock-server/server.py
# In another terminal:
python logistics/mock-server/client.py
```

### Smoke Tests

```bash
# SOAP -- send a sample purchase order
curl -X POST http://localhost:8001 \
  -H "Content-Type: text/xml" \
  -d @procurement/mock-server/test_request.xml

# REST -- list all inventory
curl http://localhost:8002/inventory

# REST -- partial update of a single item
curl -X PATCH http://localhost:8002/inventory/SKU001 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 50}'

# GraphQL -- aggregated store query
curl -X POST http://localhost:8003/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ stores { id name inventory { sku name quantity } orders { id status } } }"}'

# gRPC -- run the demo client (bi-directional streaming)
python logistics/mock-server/client.py
```

