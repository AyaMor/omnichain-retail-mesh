"""
Generates all presentation diagrams for the OmniChain Retail Mesh project.

Produces 5 high-resolution PNG files in the diagrams/ directory:
  01_master_architecture.png
  02_soap_sequence.png
  03_rest_sequence.png
  04_graphql_sequence.png
  05_grpc_sequence.png

Run:  python diagrams/generate_diagrams.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Shared constants ────────────────────────────────────────────────────────

COLORS = {
    "soap":    {"bg": "#1565C0", "light": "#E3F2FD", "mid": "#90CAF9", "text": "#FFFFFF"},
    "rest":    {"bg": "#2E7D32", "light": "#E8F5E9", "mid": "#A5D6A7", "text": "#FFFFFF"},
    "graphql": {"bg": "#7B1FA2", "light": "#F3E5F5", "mid": "#CE93D8", "text": "#FFFFFF"},
    "grpc":    {"bg": "#E65100", "light": "#FFF3E0", "mid": "#FFCC80", "text": "#FFFFFF"},
    "neutral": {"bg": "#455A64", "light": "#ECEFF1", "mid": "#B0BEC5", "text": "#FFFFFF"},
}
FONT = {"family": "sans-serif", "size": 10}
TITLE_FONT = {"family": "sans-serif", "size": 16, "weight": "bold"}
SUBTITLE_FONT = {"family": "sans-serif", "size": 11, "weight": "bold"}


def save(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════════
# HELPER: draw a rounded box with centered text
# ═══════════════════════════════════════════════════════════════════════════

def draw_box(ax, x, y, w, h, text, bg_color, text_color="white",
             fontsize=9, style="round,pad=0.02", linewidth=1.2, edgecolor=None):
    if edgecolor is None:
        edgecolor = bg_color
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle=style, facecolor=bg_color,
                         edgecolor=edgecolor, linewidth=linewidth)
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            color=text_color, fontfamily="sans-serif", linespacing=1.4)
    return box


def draw_arrow(ax, x1, y1, x2, y2, label="", color="#333333", style="-|>",
               fontsize=8, label_offset=0.15, dashed=False, lw=1.2):
    ls = "--" if dashed else "-"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + label_offset
        ax.text(mx, my, label, ha="center", va="center", fontsize=fontsize,
                color=color, fontfamily="sans-serif",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))


def draw_note(ax, x, y, text, color="#FFF9C4", border="#F9A825", fontsize=8, w=2.2):
    box = FancyBboxPatch((x - w/2, y - 0.2), w, 0.4,
                         boxstyle="round,pad=0.05", facecolor=color,
                         edgecolor=border, linewidth=1.0)
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            color="#333", fontfamily="sans-serif")


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 1: Master Architecture
# ═══════════════════════════════════════════════════════════════════════════

def generate_master_architecture():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(-1, 13)
    ax.set_ylim(-0.5, 9)
    ax.axis("off")
    ax.set_aspect("equal")

    # Title
    ax.text(6, 8.5, "OmniChain Retail Mesh — System Architecture",
            **TITLE_FONT, ha="center", va="center", color="#212121")
    ax.plot([1, 11], [8.15, 8.15], color="#BDBDBD", lw=0.8)

    # ── External actors (left column) ──
    actors = [
        (1.5, 6.5, "Manufacturers\n(China / Europe)", COLORS["soap"]["bg"]),
        (1.5, 4.5, "Partner Boutiques\n(Third-party)",  COLORS["rest"]["bg"]),
        (1.5, 2.5, "Store Managers\n(Internal)",        COLORS["graphql"]["bg"]),
        (1.5, 0.5, "Warehouse Robots\n(Automated)",     COLORS["grpc"]["bg"]),
    ]
    for x, y, label, color in actors:
        draw_box(ax, x, y, 2.6, 0.9, label, color, fontsize=9)

    # ── Services (center-right) ──
    services = [
        (7, 6.5, "SOAP Procurement\nService :8001\n(Spyne / WSDL)",    COLORS["soap"]["bg"]),
        (7, 4.5, "REST Marketplace\nAPI :8002\n(FastAPI / OpenAPI)",    COLORS["rest"]["bg"]),
        (7, 2.5, "GraphQL Dashboard\n:8003\n(Strawberry / SDL)",       COLORS["graphql"]["bg"]),
        (7, 0.5, "gRPC Logistics\n:50051\n(grpcio / Protobuf)",        COLORS["grpc"]["bg"]),
    ]
    for x, y, label, color in services:
        draw_box(ax, x, y, 2.8, 1.0, label, color, fontsize=9)

    # ── Contract files (right column) ──
    contracts = [
        (10.5, 6.5, "PurchaseOrder\n.wsdl",    COLORS["soap"]["light"],    COLORS["soap"]["bg"]),
        (10.5, 4.5, "openapi\n.yaml",          COLORS["rest"]["light"],    COLORS["rest"]["bg"]),
        (10.5, 2.5, "schema\n.graphql",        COLORS["graphql"]["light"], COLORS["graphql"]["bg"]),
        (10.5, 0.5, "warehouse\n.proto",       COLORS["grpc"]["light"],    COLORS["grpc"]["bg"]),
    ]
    for x, y, label, bg, ec in contracts:
        draw_box(ax, x, y, 1.7, 0.8, label, bg, text_color="#333", fontsize=8, edgecolor=ec)

    # ── Arrows: actor → service ──
    protocols = [
        (6.5, "XML / SOAP 1.1",            COLORS["soap"]["bg"]),
        (4.5, "JSON / HTTP REST",           COLORS["rest"]["bg"]),
        (2.5, "GraphQL Query",              COLORS["graphql"]["bg"]),
        (0.5, "Protobuf / HTTP/2 Stream",   COLORS["grpc"]["bg"]),
    ]
    for y, label, color in protocols:
        draw_arrow(ax, 2.8, y, 5.6, y, label=label, color=color, fontsize=8, lw=1.5)

    # ── Arrows: service → contract ──
    for y in [6.5, 4.5, 2.5, 0.5]:
        draw_arrow(ax, 8.4, y, 9.65, y, color="#9E9E9E", style="-|>", lw=0.8)

    # ── Dashed arrows: GraphQL → other services ──
    gql_x = 7.0
    gql_y = 2.5
    draw_arrow(ax, gql_x + 0.3, gql_y + 0.55, 7.0, 4.0,
               label="resolves\ninventory", color=COLORS["graphql"]["bg"],
               dashed=True, fontsize=7, lw=1.0, label_offset=0.05)
    draw_arrow(ax, gql_x + 0.3, gql_y + 0.55, 7.3, 6.0,
               label="resolves\norders", color=COLORS["graphql"]["bg"],
               dashed=True, fontsize=7, lw=1.0, label_offset=0.05)
    draw_arrow(ax, gql_x + 0.3, gql_y - 0.55, 7.0, 1.0,
               label="resolves\ntelemetry", color=COLORS["graphql"]["bg"],
               dashed=True, fontsize=7, lw=1.0, label_offset=-0.05)

    # ── Column headers ──
    ax.text(1.5, 7.6, "External Actors", **SUBTITLE_FONT, ha="center", color="#616161")
    ax.text(7.0, 7.6, "Services", **SUBTITLE_FONT, ha="center", color="#616161")
    ax.text(10.5, 7.6, "Contracts", **SUBTITLE_FONT, ha="center", color="#616161")

    save(fig, "01_master_architecture.png")


# ═══════════════════════════════════════════════════════════════════════════
# SEQUENCE DIAGRAM FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════

class SequenceDiagram:
    """Draws a professional UML sequence diagram."""

    def __init__(self, title, participants, color_key, fig_height=11):
        n = len(participants)
        self.fig_width = max(12, 3.5 * n)
        self.fig, self.ax = plt.subplots(figsize=(self.fig_width, fig_height))
        self.ax.set_xlim(-1.0, self.fig_width + 0.5)
        self.ax.set_ylim(-0.5, fig_height - 0.5)
        self.ax.axis("off")

        self.color = COLORS[color_key]
        self.participants = participants
        self.top = fig_height - 1.2
        self.y_cursor = self.top - 1.5
        pad = 2.0
        self.spacing = (self.fig_width - 2 * pad) / max(n - 1, 1)
        self.x_positions = [pad + i * self.spacing for i in range(n)]

        # Title
        self.ax.text(self.fig_width / 2, fig_height - 0.3, title,
                     **TITLE_FONT, ha="center", va="center", color="#212121")

        # Draw participant boxes and lifelines
        for i, (name, subtitle) in enumerate(participants):
            x = self.x_positions[i]
            label = f"{name}\n{subtitle}" if subtitle else name
            draw_box(self.ax, x, self.top, 2.8, 0.8, label,
                     self.color["bg"], fontsize=8.5)
            # Lifeline
            self.ax.plot([x, x], [self.top - 0.4, 0.2],
                         color=self.color["mid"], lw=1.0, ls="--", zorder=0)

    def message(self, from_idx, to_idx, label, style="solid", note=None, note_side="right"):
        """Draw a message arrow between participants."""
        x1 = self.x_positions[from_idx]
        x2 = self.x_positions[to_idx]
        y = self.y_cursor

        ls = "--" if style == "dashed" else "-"
        color = self.color["bg"] if style != "return" else "#555555"
        head = "-|>" if style != "return" else "-|>"

        if style == "return":
            ls = "--"
            color = "#555555"

        self.ax.annotate("", xy=(x2, y), xytext=(x1, y),
                         arrowprops=dict(arrowstyle=head, color=color, lw=1.3, linestyle=ls))

        # Label
        mx = (x1 + x2) / 2
        align = "center"
        self.ax.text(mx, y + 0.18, label, ha=align, va="bottom", fontsize=8,
                     color="#212121", fontfamily="sans-serif",
                     bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))

        if note:
            nx = self.x_positions[to_idx if note_side == "right" else from_idx]
            offset = 1.3 if note_side == "right" else -1.3
            draw_note(self.ax, nx + offset, y, note, fontsize=7.5, w=2.4)

        self.y_cursor -= 0.7

    def self_call(self, idx, label):
        """Draw a self-call (processing) on a participant."""
        x = self.x_positions[idx]
        y = self.y_cursor

        rect_w, rect_h = 0.15, 0.4
        self.ax.add_patch(FancyBboxPatch(
            (x + 0.05, y - rect_h/2), rect_w, rect_h,
            boxstyle="round,pad=0.02", facecolor=self.color["light"],
            edgecolor=self.color["bg"], linewidth=1.0))
        self.ax.text(x + 1.4, y, label, ha="center", va="center", fontsize=8,
                     color="#333", fontfamily="sans-serif",
                     bbox=dict(boxstyle="round,pad=0.15", fc=self.color["light"],
                               ec=self.color["mid"], alpha=0.9))
        self.y_cursor -= 0.65

    def note_banner(self, text, color=None):
        """Draw a horizontal note banner spanning the diagram."""
        if color is None:
            color = self.color["light"]
        y = self.y_cursor
        w = self.fig_width - 2
        box = FancyBboxPatch((1, y - 0.2), w, 0.4,
                             boxstyle="round,pad=0.05", facecolor=color,
                             edgecolor=self.color["mid"], linewidth=1.0)
        self.ax.add_patch(box)
        self.ax.text(self.fig_width / 2, y, text, ha="center", va="center",
                     fontsize=8.5, color="#333", fontfamily="sans-serif", fontweight="bold")
        self.y_cursor -= 0.7

    def spacer(self, amount=0.3):
        self.y_cursor -= amount

    def save(self, filename):
        save(self.fig, filename)


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 2: SOAP Sequence
# ═══════════════════════════════════════════════════════════════════════════

def generate_soap_sequence():
    sd = SequenceDiagram(
        "SOAP — B2B Procurement Flow",
        [("Manufacturer ERP", "(SAP / Oracle)"),
         ("OmniChain Gateway", ""),
         ("ProcurementService", ":8001 (Spyne)")],
        "soap", fig_height=10
    )

    sd.note_banner("Data Format: XML / SOAP 1.1 Envelope")
    sd.spacer(0.2)

    sd.message(0, 1, "HTTP POST /procurement\nContent-Type: text/xml")
    sd.message(1, 2, "Forward SOAP Envelope")
    sd.self_call(2, "Validate XML against\nPurchaseOrder.wsdl (XSD)")
    sd.self_call(2, "Parse PurchaseOrder\n(orderId, buyerOrgId, items[])")
    sd.self_call(2, "Calculate totalPriceCents\nGenerate confirmationId")
    sd.message(2, 1, "SOAP Response:\n<OrderResponse>", style="return")
    sd.message(1, 0, "HTTP 200  —  XML Body", style="return")

    sd.spacer(0.3)
    sd.note_banner("Response: confirmationId  |  status=ACCEPTED  |  estimatedDelivery  |  totalPriceCents")

    sd.save("02_soap_sequence.png")


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 3: REST Sequence
# ═══════════════════════════════════════════════════════════════════════════

def generate_rest_sequence():
    sd = SequenceDiagram(
        "REST — Partner Marketplace Flow",
        [("Boutique Client", "(Third-party)"),
         ("Marketplace API", ":8002 (FastAPI)")],
        "rest", fig_height=11
    )

    sd.note_banner("Data Format: JSON over HTTP/1.1")
    sd.spacer(0.2)

    # GET /inventory
    sd.message(0, 1, "GET /inventory")
    sd.message(1, 0, 'HTTP 200  —  [{sku, name, category,\nquantity, price_cents, store_id}, ...]', style="return")
    sd.spacer(0.3)

    # GET /inventory/{sku}
    sd.message(0, 1, "GET /inventory/SKU001")
    sd.message(1, 0, 'HTTP 200  —  {sku: "SKU001",\nname: "Urban Wool Jacket", quantity: 150}', style="return")
    sd.spacer(0.3)

    # PATCH
    sd.message(0, 1, 'PATCH /inventory/SKU001\n{"quantity": 75}',
               note="Partial update:\nonly changed fields", note_side="right")
    sd.self_call(1, "Apply delta to\nexisting resource")
    sd.message(1, 0, 'HTTP 200  —  {sku: "SKU001",\nquantity: 75, ...}', style="return")

    sd.spacer(0.3)
    sd.note_banner("PATCH sends only the delta  —  unlike PUT which requires the full resource")

    sd.save("03_rest_sequence.png")


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 4: GraphQL Sequence
# ═══════════════════════════════════════════════════════════════════════════

def generate_graphql_sequence():
    sd = SequenceDiagram(
        "GraphQL — Manager Dashboard Aggregator Flow",
        [("Store Manager", "(Dashboard UI)"),
         ("GraphQL Gateway", ":8003 (Strawberry)"),
         ("REST :8002", ""),
         ("SOAP :8001", ""),
         ("gRPC :50051", "")],
        "graphql", fig_height=12
    )

    sd.note_banner("Data Format: JSON (GraphQL query language)")
    sd.spacer(0.15)

    sd.message(0, 1, 'POST /graphql\n{ stores { id name\n  inventory { sku qty }\n  orders { id status } } }')
    sd.spacer(0.1)

    # Parallel resolution banner
    y = sd.y_cursor
    w = sd.fig_width - 2
    box = FancyBboxPatch((1, y - 0.2), w, 0.35,
                         boxstyle="round,pad=0.03",
                         facecolor="#F3E5F5", edgecolor="#CE93D8", linewidth=1.2)
    sd.ax.add_patch(box)
    sd.ax.text(1.3, y, "par", ha="left", va="center", fontsize=8,
               fontweight="bold", color=COLORS["graphql"]["bg"])
    sd.ax.text(sd.fig_width / 2, y, "Parallel resolution across backends",
               ha="center", va="center", fontsize=8, color="#333")
    sd.y_cursor -= 0.6

    sd.message(1, 2, "GET /inventory\n?store_id=...", style="solid")
    sd.message(2, 1, "JSON array", style="return")
    sd.message(1, 3, "SOAP GetOrders", style="solid")
    sd.message(3, 1, "XML response", style="return")
    sd.message(1, 4, "gRPC\nGetRobotStatus", style="solid")
    sd.message(4, 1, "Protobuf response", style="return")

    sd.spacer(0.1)
    sd.self_call(1, "Merge into unified\nStore object")
    sd.spacer(0.1)

    sd.message(1, 0, 'HTTP 200\n{data: {stores: [{id, name,\ninventory: [...], orders: [...]}]}}', style="return")

    sd.spacer(0.2)
    sd.note_banner("Single query replaces 3 x N REST calls  —  no under-fetching")

    sd.save("04_graphql_sequence.png")


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 5: gRPC Sequence
# ═══════════════════════════════════════════════════════════════════════════

def generate_grpc_sequence():
    sd = SequenceDiagram(
        "gRPC — Warehouse Robot Bi-directional Streaming",
        [("Warehouse Controller", "(Command Center)"),
         ("WarehouseAutomation", ":50051 (grpcio)")],
        "grpc", fig_height=13
    )

    sd.note_banner("Data Format: Protobuf binary / HTTP/2  (~40 bytes vs ~250 bytes JSON)")
    sd.spacer(0.2)

    sd.message(0, 1, "Open bi-directional stream\nrpc StreamTelemetry",
               note="Both streams are\nindependent", note_side="right")
    sd.spacer(0.15)

    # Command 1: MOVE
    sd.message(0, 1, "WarehouseCommand\n{COMMAND_MOVE, target: (15, 12, 0)}")
    sd.message(1, 0, "Telemetry [1/3]  pos=(5,4)  battery=0.95  MOVING", style="return")
    sd.message(1, 0, "Telemetry [2/3]  pos=(10,8)  battery=0.93  MOVING", style="return")
    sd.message(1, 0, "Telemetry [3/3]  pos=(15,12)  battery=0.91  IDLE", style="return")
    sd.spacer(0.15)

    # Command 2: PICK
    sd.message(0, 1, "WarehouseCommand\n{COMMAND_PICK, sku: SKU-JACKET-BLK-L}")
    sd.message(1, 0, "Telemetry [1/3]  status=PICKING", style="return")
    sd.message(1, 0, "Telemetry [2/3]  status=PICKING", style="return")
    sd.message(1, 0, "Telemetry [3/3]  status=IDLE", style="return")
    sd.spacer(0.15)

    # Command 3: CHARGE
    sd.message(0, 1, "WarehouseCommand\n{COMMAND_CHARGE, target: (0, 0, 0)}")
    sd.message(1, 0, "Telemetry [1/3]  battery=0.89  MOVING", style="return")
    sd.message(1, 0, "Telemetry [2/3]  battery=0.87  MOVING", style="return")
    sd.message(1, 0, "Telemetry [3/3]  battery=0.85  CHARGING", style="return")
    sd.spacer(0.15)

    sd.message(0, 1, "End stream")

    sd.spacer(0.3)
    sd.note_banner("Also supports unary RPC: GetRobotStatus(RobotRequest) → RobotTelemetry")

    sd.save("05_grpc_sequence.png")


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 6: Protocol Selection Decision Tree
# ═══════════════════════════════════════════════════════════════════════════

def generate_decision_tree():
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(-0.5, 16)
    ax.set_ylim(-0.5, 11)
    ax.axis("off")

    ax.text(8, 10.5, "OmniChain Protocol Selection Logic",
            **TITLE_FONT, ha="center", va="center", color="#212121")
    ax.plot([2, 14], [10.15, 10.15], color="#BDBDBD", lw=0.8)

    # ── Level 0: Start ──
    draw_box(ax, 8, 9.3, 2.8, 0.7, "New Requirement",
             COLORS["neutral"]["bg"], fontsize=10)

    # ── Level 1: First decision ──
    draw_box(ax, 8, 7.8, 3.6, 0.7,
             "Requires strict schema\nenforcement & WS-Security?",
             "#FFF9C4", text_color="#333", fontsize=9,
             style="round,pad=0.03", edgecolor="#F9A825")
    draw_arrow(ax, 8, 8.95, 8, 8.15, color="#555", lw=1.3)

    # ── YES → SOAP ──
    draw_arrow(ax, 6.2, 7.8, 3.5, 7.0, label="YES", color=COLORS["soap"]["bg"],
               fontsize=9, lw=1.5, label_offset=0.25)
    draw_box(ax, 2.5, 6.3, 3.0, 1.0,
             "SOAP\nPurchaseOrder.wsdl\n:8001",
             COLORS["soap"]["bg"], fontsize=9)
    # SOAP traits
    draw_box(ax, 2.5, 5.1, 2.8, 0.6,
             "XSD validation\nWS-Security\nWSDL code-gen",
             COLORS["soap"]["light"], text_color="#333", fontsize=7.5,
             edgecolor=COLORS["soap"]["mid"])

    # ── NO → next decision ──
    draw_arrow(ax, 9.8, 7.8, 11.0, 7.0, label="NO", color="#555",
               fontsize=9, lw=1.3, label_offset=0.25)

    # ── Level 2: Speed/latency ──
    draw_box(ax, 11.5, 6.3, 3.6, 0.7,
             "Real-time streaming\n& minimal latency?",
             "#FFF9C4", text_color="#333", fontsize=9,
             style="round,pad=0.03", edgecolor="#F9A825")

    # ── YES → gRPC ──
    draw_arrow(ax, 13.3, 6.3, 14.5, 5.3, label="YES", color=COLORS["grpc"]["bg"],
               fontsize=9, lw=1.5, label_offset=0.2)
    draw_box(ax, 14.0, 4.5, 2.8, 1.0,
             "gRPC\nwarehouse.proto\n:50051",
             COLORS["grpc"]["bg"], fontsize=9)
    draw_box(ax, 14.0, 3.3, 2.8, 0.6,
             "Protobuf binary\nHTTP/2 streams\nCompile-time types",
             COLORS["grpc"]["light"], text_color="#333", fontsize=7.5,
             edgecolor=COLORS["grpc"]["mid"])

    # ── NO → next decision ──
    draw_arrow(ax, 9.7, 6.3, 8.5, 5.3, label="NO", color="#555",
               fontsize=9, lw=1.3, label_offset=0.2)

    # ── Level 3: Aggregation ──
    draw_box(ax, 8, 4.5, 3.8, 0.7,
             "Aggregates data from\nmultiple backends?",
             "#FFF9C4", text_color="#333", fontsize=9,
             style="round,pad=0.03", edgecolor="#F9A825")

    # ── YES → GraphQL ──
    draw_arrow(ax, 6.1, 4.5, 5.0, 3.5, label="YES", color=COLORS["graphql"]["bg"],
               fontsize=9, lw=1.5, label_offset=0.2)
    draw_box(ax, 4.5, 2.7, 3.0, 1.0,
             "GraphQL\nschema.graphql\n:8003",
             COLORS["graphql"]["bg"], fontsize=9)
    draw_box(ax, 4.5, 1.5, 2.8, 0.6,
             "Nested queries\nNo over-fetching\nClient-driven shape",
             COLORS["graphql"]["light"], text_color="#333", fontsize=7.5,
             edgecolor=COLORS["graphql"]["mid"])

    # ── NO → REST ──
    draw_arrow(ax, 9.9, 4.5, 11.0, 3.5, label="NO (default)", color=COLORS["rest"]["bg"],
               fontsize=9, lw=1.5, label_offset=0.2)
    draw_box(ax, 11.0, 2.7, 3.0, 1.0,
             "REST\nopenapi.yaml\n:8002",
             COLORS["rest"]["bg"], fontsize=9)
    draw_box(ax, 11.0, 1.5, 2.8, 0.6,
             "HTTP caching\nUniversal adoption\nStateless scaling",
             COLORS["rest"]["light"], text_color="#333", fontsize=7.5,
             edgecolor=COLORS["rest"]["mid"])

    save(fig, "06_decision_tree.png")


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 7: GraphQL Aggregator Pattern
# ═══════════════════════════════════════════════════════════════════════════

def generate_aggregator_pattern():
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(-0.5, 15)
    ax.set_ylim(-0.5, 10)
    ax.axis("off")

    ax.text(7.5, 9.5, "GraphQL: The Omnichannel Unified Interface",
            **TITLE_FONT, ha="center", va="center", color="#212121")
    ax.plot([1.5, 13.5], [9.15, 9.15], color="#BDBDBD", lw=0.8)

    # ── Left: Store Manager Tablet ──
    # Tablet frame
    tablet_x, tablet_y = 2.2, 5.5
    tablet = FancyBboxPatch((tablet_x - 1.5, tablet_y - 2.5), 3.0, 5.0,
                            boxstyle="round,pad=0.15", facecolor="#FAFAFA",
                            edgecolor="#333", linewidth=2.5)
    ax.add_patch(tablet)
    ax.text(tablet_x, tablet_y + 2.0, "Store Manager Tablet",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color="#333", fontfamily="sans-serif")

    # Screen content
    screen = FancyBboxPatch((tablet_x - 1.2, tablet_y - 2.0), 2.4, 3.5,
                            boxstyle="round,pad=0.05", facecolor="#E8EAF6",
                            edgecolor="#7986CB", linewidth=1.0)
    ax.add_patch(screen)
    ax.text(tablet_x, tablet_y + 1.1, "Dashboard", ha="center", fontsize=8,
            fontweight="bold", color="#283593")
    ax.text(tablet_x, tablet_y + 0.6, "───────────", ha="center", fontsize=7, color="#9FA8DA")
    ax.text(tablet_x, tablet_y + 0.1, "Inventory:  5 SKUs", ha="center", fontsize=7.5, color="#333")
    ax.text(tablet_x, tablet_y - 0.3, "Orders:  3 pending", ha="center", fontsize=7.5, color="#333")
    ax.text(tablet_x, tablet_y - 0.7, "Robots:  2 active", ha="center", fontsize=7.5, color="#333")
    ax.text(tablet_x, tablet_y - 1.2, "Low Stock:  1 alert", ha="center", fontsize=7.5, color="#C62828")
    ax.text(tablet_x, tablet_y - 1.7, "Single POST /graphql", ha="center", fontsize=7,
            fontstyle="italic", color="#666")

    # ── Center: GraphQL Gateway ──
    gw_x, gw_y = 7.5, 5.5
    draw_box(ax, gw_x, gw_y + 1.5, 3.4, 0.8,
             "GraphQL Gateway\n:8003 (Strawberry)",
             COLORS["graphql"]["bg"], fontsize=10)

    # Field mapping table
    table_top = gw_y + 0.6
    headers_bg = COLORS["graphql"]["light"]
    row_h = 0.4
    table_w = 3.6

    # Table header
    header = FancyBboxPatch((gw_x - table_w/2, table_top - row_h/2), table_w, row_h,
                            boxstyle="square,pad=0", facecolor=COLORS["graphql"]["mid"],
                            edgecolor=COLORS["graphql"]["bg"], linewidth=1.0)
    ax.add_patch(header)
    ax.text(gw_x - 0.8, table_top, "GraphQL Field", ha="center", va="center",
            fontsize=7.5, fontweight="bold", color="#333")
    ax.text(gw_x + 1.0, table_top, "Backend Source", ha="center", va="center",
            fontsize=7.5, fontweight="bold", color="#333")

    # Table rows
    field_mappings = [
        ("stores.inventory[]",   "REST GET /inventory"),
        ("stores.orders[]",      "SOAP GetOrders()"),
        ("stores.robots[]",      "gRPC GetRobotStatus()"),
        ("dashboardSummary",     "Aggregated locally"),
    ]
    for i, (field, source) in enumerate(field_mappings):
        ry = table_top - (i + 1) * row_h
        bg = "#FFFFFF" if i % 2 == 0 else headers_bg
        row = FancyBboxPatch((gw_x - table_w/2, ry - row_h/2), table_w, row_h,
                             boxstyle="square,pad=0", facecolor=bg,
                             edgecolor="#BDBDBD", linewidth=0.5)
        ax.add_patch(row)
        ax.text(gw_x - 0.8, ry, field, ha="center", va="center",
                fontsize=7, color="#333", fontfamily="monospace")
        ax.text(gw_x + 1.0, ry, source, ha="center", va="center",
                fontsize=7, color="#555")

    # ── Arrow: Tablet → Gateway ──
    draw_arrow(ax, 3.7, 6.2, 5.8, 6.8, label="POST /graphql\n(JSON)",
               color=COLORS["graphql"]["bg"], lw=1.8, fontsize=8)

    # ── Right column: Backend services ──
    svc_x = 12.5

    # REST service
    draw_box(ax, svc_x, 7.5, 3.0, 0.8,
             "Marketplace Service\n(REST :8002)",
             COLORS["rest"]["bg"], fontsize=8.5)
    draw_arrow(ax, 9.2, 7.0, 11.0, 7.3, label="JSON",
               color=COLORS["rest"]["bg"], lw=1.3, fontsize=7.5)

    # SOAP service
    draw_box(ax, svc_x, 5.5, 3.0, 0.8,
             "Legacy Procurement\n(SOAP :8001)",
             COLORS["soap"]["bg"], fontsize=8.5)
    draw_arrow(ax, 9.2, 6.0, 11.0, 5.7, label="XML",
               color=COLORS["soap"]["bg"], lw=1.3, fontsize=7.5)

    # gRPC service
    draw_box(ax, svc_x, 3.5, 3.0, 0.8,
             "Warehouse Automation\n(gRPC :50051)",
             COLORS["grpc"]["bg"], fontsize=8.5)
    draw_arrow(ax, 9.2, 5.0, 11.0, 3.8, label="Protobuf",
               color=COLORS["grpc"]["bg"], lw=1.3, fontsize=7.5)

    save(fig, "07_aggregator_pattern.png")


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 8: Payload Size Comparison
# ═══════════════════════════════════════════════════════════════════════════

def generate_payload_comparison():
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.set_xlim(-0.5, 15)
    ax.set_ylim(-0.5, 9)
    ax.axis("off")

    ax.text(7.5, 8.5, "Payload Overhead Comparison — Order Object",
            **TITLE_FONT, ha="center", va="center", color="#212121")
    ax.text(7.5, 8.0, "Same business data (SKU, quantity, price) encoded in three wire formats",
            ha="center", va="center", fontsize=10, color="#757575", fontfamily="sans-serif")
    ax.plot([1.5, 13.5], [7.7, 7.7], color="#BDBDBD", lw=0.8)

    # ── Shared layout constants ──
    BLOCK_Y_TOP = 7.0
    LABEL_SIZE = 10
    CODE_SIZE = 7.5
    bar_bottom = 1.8

    # ═══ Column 1: SOAP XML ═══
    col1_x = 2.8

    # Header
    draw_box(ax, col1_x, BLOCK_Y_TOP, 3.8, 0.6,
             "SOAP XML Envelope", COLORS["soap"]["bg"], fontsize=LABEL_SIZE)

    # Code block
    soap_code = (
        '<soapenv:Envelope>\n'
        '  <soapenv:Header/>\n'
        '  <soapenv:Body>\n'
        '    <proc:SubmitOrder>\n'
        '      <proc:order>\n'
        '        <proc:order_id>\n'
        '          PO-2026-0042\n'
        '        </proc:order_id>\n'
        '        <proc:sku>...\n'
        '        <proc:quantity>\n'
        '          500\n'
        '        </proc:quantity>\n'
        '      </proc:order>\n'
        '    </proc:SubmitOrder>\n'
        '  </soapenv:Body>\n'
        '</soapenv:Envelope>'
    )
    code_box1 = FancyBboxPatch((col1_x - 1.8, 3.0), 3.6, 3.5,
                               boxstyle="round,pad=0.08", facecolor="#E3F2FD",
                               edgecolor=COLORS["soap"]["mid"], linewidth=1.0)
    ax.add_patch(code_box1)
    ax.text(col1_x, 6.3, soap_code, ha="center", va="top",
            fontsize=CODE_SIZE, fontfamily="monospace", color="#1A237E", linespacing=1.2)

    # Size bar
    bar_1_h = 4.0  # tallest bar
    bar1 = FancyBboxPatch((col1_x - 0.5, bar_bottom), 1.0, bar_1_h,
                          boxstyle="round,pad=0.03", facecolor=COLORS["soap"]["bg"],
                          edgecolor=COLORS["soap"]["bg"], linewidth=0, alpha=0.0)
    ax.add_patch(bar1)

    # Size label
    draw_box(ax, col1_x, 2.5, 1.8, 0.6,
             "~1,000 B", COLORS["soap"]["bg"], fontsize=12)
    ax.text(col1_x, 2.0, "100%", ha="center", fontsize=9, color="#666")

    # ═══ Column 2: REST JSON ═══
    col2_x = 7.5

    draw_box(ax, col2_x, BLOCK_Y_TOP, 3.8, 0.6,
             "REST JSON", COLORS["rest"]["bg"], fontsize=LABEL_SIZE)

    json_code = (
        '{\n'
        '  "order_id":\n'
        '    "PO-2026-0042",\n'
        '  "sku":\n'
        '    "SKU-JACKET-BLK-L",\n'
        '  "quantity": 500,\n'
        '  "unit_price_cents":\n'
        '    4500,\n'
        '  "currency": "EUR"\n'
        '}'
    )
    code_box2 = FancyBboxPatch((col2_x - 1.8, 3.8), 3.6, 2.7,
                               boxstyle="round,pad=0.08", facecolor="#E8F5E9",
                               edgecolor=COLORS["rest"]["mid"], linewidth=1.0)
    ax.add_patch(code_box2)
    ax.text(col2_x, 6.3, json_code, ha="center", va="top",
            fontsize=CODE_SIZE, fontfamily="monospace", color="#1B5E20", linespacing=1.2)

    draw_box(ax, col2_x, 2.5, 1.8, 0.6,
             "~200 B", COLORS["rest"]["bg"], fontsize=12)
    ax.text(col2_x, 2.0, "20%", ha="center", fontsize=9, color="#666")

    # ═══ Column 3: gRPC Protobuf ═══
    col3_x = 12.2

    draw_box(ax, col3_x, BLOCK_Y_TOP, 3.8, 0.6,
             "gRPC Protobuf Binary", COLORS["grpc"]["bg"], fontsize=LABEL_SIZE)

    proto_code = (
        'Field 1: varint\n'
        '  0A 0C [order_id]\n\n'
        'Field 2: varint\n'
        '  12 10 [sku]\n\n'
        'Field 3: varint\n'
        '  18 F4 03 [qty=500]\n\n'
        'Field 4: varint\n'
        '  20 94 23 [price]'
    )
    code_box3 = FancyBboxPatch((col3_x - 1.8, 4.2), 3.6, 2.3,
                               boxstyle="round,pad=0.08", facecolor="#FFF3E0",
                               edgecolor=COLORS["grpc"]["mid"], linewidth=1.0)
    ax.add_patch(code_box3)
    ax.text(col3_x, 6.3, proto_code, ha="center", va="top",
            fontsize=CODE_SIZE, fontfamily="monospace", color="#BF360C", linespacing=1.2)

    draw_box(ax, col3_x, 2.5, 1.8, 0.6,
             "~50 B", COLORS["grpc"]["bg"], fontsize=12)
    ax.text(col3_x, 2.0, "5%", ha="center", fontsize=9, color="#666")

    # ── Reduction arrows ──
    ax.annotate("", xy=(col2_x - 0.9, 2.5), xytext=(col1_x + 0.9, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))
    ax.text((col1_x + col2_x) / 2, 2.85, "5x smaller", ha="center",
            fontsize=8, fontweight="bold", color="#333")

    ax.annotate("", xy=(col3_x - 0.9, 2.5), xytext=(col2_x + 0.9, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))
    ax.text((col2_x + col3_x) / 2, 2.85, "4x smaller", ha="center",
            fontsize=8, fontweight="bold", color="#333")

    # ── Tradeoff bar ──
    tradeoff_y = 1.3
    ax.text(col1_x, tradeoff_y, "Human Readable",
            ha="center", fontsize=8.5, color=COLORS["soap"]["bg"], fontweight="bold")
    ax.text(col2_x, tradeoff_y, "Balanced",
            ha="center", fontsize=8.5, color=COLORS["rest"]["bg"], fontweight="bold")
    ax.text(col3_x, tradeoff_y, "Machine Optimised",
            ha="center", fontsize=8.5, color=COLORS["grpc"]["bg"], fontweight="bold")

    # Gradient arrow
    ax.annotate("", xy=(col3_x + 0.8, 0.9), xytext=(col1_x - 0.8, 0.9),
                arrowprops=dict(arrowstyle="-|>", color="#888", lw=2.0))
    ax.text(7.5, 0.55, "Readability ←──────→ Efficiency",
            ha="center", fontsize=9, color="#666", fontfamily="sans-serif")

    save(fig, "08_payload_comparison.png")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  Generating OmniChain presentation diagrams...")
    print("=" * 60)

    generate_master_architecture()
    generate_soap_sequence()
    generate_rest_sequence()
    generate_graphql_sequence()
    generate_grpc_sequence()
    generate_decision_tree()
    generate_aggregator_pattern()
    generate_payload_comparison()

    print("=" * 60)
    print(f"  All diagrams saved to: {OUTPUT_DIR}/")
    print("=" * 60)
