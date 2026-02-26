# OmniChain Retail Mesh -- Presentation Diagrams and Slide Content

All diagrams are available as PNG images in the `diagrams/` folder, ready for direct insertion into your slides.


## Master System Architecture Diagram

Use this as the opening "Big Picture" slide.

![OmniChain Retail Mesh - System Architecture](/Users/ayamorsli/projet-API/diagrams/01_master_architecture.png)


## 1. SOAP -- B2B Procurement

### Sequence Diagram

![SOAP - B2B Procurement Flow](/Users/ayamorsli/projet-API/diagrams/02_soap_sequence.png)

### Slide Content: Why SOAP for Procurement?

**Justification (3 points):**

1. **Schema-enforced contract integrity.** The WSDL embeds XML Schema Definition (XSD) types that enforce field ordering, occurrence constraints (minOccurs/maxOccurs), and data types at the wire level. This provides compile-time guarantees that are absent in schema-optional formats like JSON, reducing integration defects in high-value B2B transactions.

2. **Native compatibility with enterprise systems.** Manufacturing partners operate ERP platforms (SAP, Oracle E-Business Suite) that expose and consume SOAP/WS-* interfaces natively. Adopting REST or GraphQL would impose an additional protocol translation layer on the manufacturer side, increasing integration cost and latency.

3. **Message-level security via WS-Security.** Unlike TLS (transport-level), WS-Security signs and encrypts individual XML elements within the SOAP envelope. This allows purchase orders to transit through intermediary message brokers and audit systems while maintaining end-to-end data confidentiality -- a regulatory requirement for cross-border financial documents.

**Trade-offs:**

| Gained | Sacrificed |
|---|---|
| Strict type safety at the wire level | Human readability (XML is verbose) |
| Formal contract (WSDL) for code generation | Simplicity (SOAP toolkits are heavy) |
| WS-Security for message-level encryption | Performance (XML parsing is slower than JSON/Protobuf) |

**Architectural Insight:**

SOAP's rigidity is not a limitation -- it is a deliberate design choice. In B2B procurement, the cost of a malformed purchase order (incorrect quantities, missing manufacturer IDs) far exceeds the cost of XML verbosity. The WSDL acts as a machine-readable Service Level Agreement: if a message passes schema validation, both parties can trust its structure without defensive parsing. This is why SOAP persists in banking, healthcare, and manufacturing long after REST became dominant in consumer-facing APIs.


## 2. REST -- Partner Marketplace

### Sequence Diagram

![REST - Partner Marketplace Flow](/Users/ayamorsli/projet-API/diagrams/03_rest_sequence.png)

### Slide Content: Why REST for Marketplace?

**Justification (3 points):**

1. **Minimal integration barrier.** REST's reliance on standard HTTP verbs (GET, PATCH) and JSON means boutique developers can integrate using any programming language and any HTTP client (curl, Postman, fetch API). There is no code generation step, no framework dependency, and no proprietary toolkit -- reducing time-to-integration from days to hours.

2. **Infrastructure-level cacheability.** GET responses are inherently cacheable using standard HTTP headers (Cache-Control, ETag). When thousands of boutiques poll for catalogue updates simultaneously, CDNs and reverse proxies can serve cached responses without hitting the origin server, enabling horizontal scalability without application-level changes.

3. **Semantic verb-to-operation mapping.** Each HTTP verb carries built-in semantic meaning (GET = safe retrieval, PATCH = partial modification, DELETE = removal). This eliminates the need for operation names in the URL and makes the API self-documenting -- a client can infer behaviour from the verb alone.

**Trade-offs:**

| Gained | Sacrificed |
|---|---|
| Universal adoption and simplicity | No built-in schema enforcement (requires OpenAPI as optional layer) |
| HTTP caching at CDN/proxy level | Multiple round-trips for related resources (under-fetching) |
| Statelessness for horizontal scaling | No native streaming or push capability |

**Architectural Insight:**

The choice of PATCH over PUT is not cosmetic. PUT semantics require the client to send the complete resource representation, meaning a boutique updating stock after a single sale would need to re-transmit every field (name, category, price) alongside the changed quantity. PATCH sends only the delta, reducing payload size and eliminating the risk of accidental field overwrites caused by stale client-side state. This distinction becomes critical at scale: with 10,000 boutiques issuing stock updates per minute, the bandwidth difference between full-resource PUT and single-field PATCH is substantial.


## 3. GraphQL -- Manager Dashboard

### Sequence Diagram

![GraphQL - Manager Dashboard Aggregator Flow](/Users/ayamorsli/projet-API/diagrams/04_graphql_sequence.png)

### Slide Content: Why GraphQL for Dashboard?

**Justification (3 points):**

1. **Eliminates under-fetching through nested queries.** A REST-based dashboard would require sequential calls to /stores, /stores/{id}/inventory, /stores/{id}/orders, and /stores/{id}/robots for each store -- an O(N) request pattern known as the N+1 problem. GraphQL collapses this into a single POST with nested field selection, reducing network round-trips and total latency.

2. **Client-driven field selection eliminates over-fetching.** The manager's dashboard contains multiple widgets, each requiring different data subsets. A summary panel needs only store names and counts; a detail panel needs full inventory. GraphQL lets each widget specify exactly the fields it needs, unlike REST where the server dictates the response shape and the client discards unused fields.

3. **Aggregator gateway pattern decouples frontend from backend topology.** The GraphQL schema presents a unified Store type that nests InventoryItem, Order, and RobotTelemetry. The frontend has no knowledge of whether inventory comes from REST, orders from SOAP, or telemetry from gRPC. Backend services can be replaced, split, or migrated without any frontend changes.

**Trade-offs:**

| Gained | Sacrificed |
|---|---|
| Single request for deeply nested data | HTTP caching (POST requests are not cacheable by default) |
| Client-controlled response shape | Query complexity analysis needed to prevent abuse |
| Backend-agnostic aggregation | Higher server-side resolver complexity |

**Architectural Insight:**

GraphQL is not a replacement for REST -- it is a complementary layer. In our architecture, the GraphQL service does not own any data. It acts purely as an aggregation gateway that fans out to the three specialised services (REST, SOAP, gRPC) and merges their responses. This separation of concerns means the REST API can still be exposed directly to boutiques (who benefit from caching and simplicity), while managers get an aggregated view through GraphQL. Attempting to serve both audiences through a single paradigm would force compromises that degrade both experiences.


## 4. gRPC -- Warehouse Logistics

### Sequence Diagram

![gRPC - Warehouse Robot Bi-directional Streaming](/Users/ayamorsli/projet-API/diagrams/05_grpc_sequence.png)

### Slide Content: Why gRPC for Logistics?

**Justification (3 points):**

1. **Binary serialisation for bandwidth-constrained environments.** Protobuf encodes a RobotTelemetry message in approximately 40 bytes versus 250 bytes for the equivalent JSON. At 100 robots transmitting 10 updates per second, this reduces bandwidth consumption from 250 KB/s to 40 KB/s -- a 6x reduction that is significant in warehouses with limited network infrastructure.

2. **Native bi-directional streaming over a single connection.** The StreamTelemetry RPC maintains a persistent HTTP/2 connection where commands flow from the controller to the robot and telemetry flows back simultaneously. Unlike WebSockets (which lack built-in serialisation) or HTTP long-polling (which requires repeated connection setup), gRPC streaming provides structured, typed, full-duplex communication with no additional framing protocol.

3. **Compile-time type safety through code generation.** Both the warehouse controller and the robot firmware generate client and server stubs from the same warehouse.proto file. Field additions, type changes, or removed messages are caught at compile time rather than at runtime, eliminating an entire class of integration bugs in safety-critical warehouse automation.

**Trade-offs:**

| Gained | Sacrificed |
|---|---|
| Binary efficiency (6x smaller payloads) | Human readability (cannot inspect with curl) |
| Bi-directional streaming on one connection | Browser compatibility (requires gRPC-Web proxy) |
| Compile-time type safety via codegen | Ecosystem maturity (fewer tools, smaller community than REST) |

**Architectural Insight:**

The choice of bi-directional streaming over unary RPCs is not about throughput -- it is about control latency. In a unary model, the controller would need to poll each robot for telemetry and send commands as separate request-response pairs. With 100 robots, this creates 200 concurrent connections and introduces polling interval delays. Bi-directional streaming inverts this: the robot pushes telemetry as soon as it is generated, and the controller pushes commands the instant a decision is made. The result is sub-second reaction time (reroute a robot whose battery drops below 20%) versus multi-second polling delays. In warehouse automation, this difference determines whether a robot collides with an obstacle or stops in time.


## Summary Comparison Table

Use this on a single slide for a side-by-side overview.

| Criterion | SOAP | REST | GraphQL | gRPC |
|---|---|---|---|---|
| **Data format** | XML | JSON | JSON | Protobuf (binary) |
| **Transport** | HTTP/1.1 | HTTP/1.1 | HTTP/1.1 | HTTP/2 |
| **Contract** | WSDL | OpenAPI (optional) | SDL Schema | .proto |
| **Typing** | Strict (XSD) | Runtime (Pydantic) | Runtime (resolvers) | Compile-time (codegen) |
| **Streaming** | No | No | No (subscriptions possible) | Native bi-directional |
| **Caching** | No | Yes (HTTP GET) | No (POST-based) | No |
| **Browser support** | Yes (via AJAX) | Yes (native) | Yes (native) | Requires gRPC-Web proxy |
| **Best for** | Formal B2B contracts | Public/partner APIs | Aggregation gateways | Real-time machine-to-machine |
| **Port in our PoC** | 8001 | 8002 | 8003 | 50051 |


---

## 5. Protocol Selection Decision Tree

Use this to demonstrate the **logical reasoning** behind each technology choice.

![OmniChain Protocol Selection Logic](/Users/ayamorsli/projet-API/diagrams/06_decision_tree.png)

**Pro-Speaker Note:** *"REST is our default — we only deviate when a requirement explicitly demands something REST cannot provide. This decision tree shows that every non-REST choice is driven by a concrete constraint, not by novelty."*


---

## 6. GraphQL Aggregator Pattern

Use this to show how the GraphQL layer **abstracts heterogeneous backends** from the frontend.

![GraphQL: The Omnichannel Unified Interface](/Users/ayamorsli/projet-API/diagrams/07_aggregator_pattern.png)

**Pro-Speaker Note:** *"The frontend developer has no idea which backend uses SOAP, REST, or gRPC — they only see a single, typed GraphQL schema. That is the power of the aggregator pattern."*


---

## 7. Payload Overhead Comparison

Use this to quantify the **wire-format trade-off** across SOAP, REST, and gRPC.

![Payload Overhead Comparison — Order Object](/Users/ayamorsli/projet-API/diagrams/08_payload_comparison.png)

**Pro-Speaker Note:** *"At 100 robots sending 10 messages per second, the choice between 1 KB and 50 B is the difference between saturating a warehouse network and barely using it."*
