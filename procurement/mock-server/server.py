"""
SOAP Mock Server - B2B Procurement Service

Implements the SubmitOrder operation defined in contracts/PurchaseOrder.wsdl
using Spyne (Python SOAP framework). Returns static confirmation data for
demonstration purposes.

Run:  python procurement/mock-server/server.py
WSDL: http://localhost:8001/?wsdl
"""

from spyne import (
    Application, Service, rpc,
    Unicode, Integer, Date, Array, ComplexModel,
)
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from datetime import date, timedelta


# ---------------------------------------------------------------------------
# Complex types (mirror the XSD types in PurchaseOrder.wsdl)
# ---------------------------------------------------------------------------

class OrderItem(ComplexModel):
    """A single line-item in a purchase order."""
    __namespace__ = "http://retailsync.retail/procurement"

    sku              = Unicode(min_occurs=1, max_occurs=1)
    product_name     = Unicode()
    quantity         = Integer(min_occurs=1)
    unit_price_cents = Integer()
    manufacturing_id = Unicode()


class PurchaseOrder(ComplexModel):
    """Full purchase order sent to the manufacturer."""
    __namespace__ = "http://retailsync.retail/procurement"

    order_id        = Unicode()
    buyer_org_id    = Unicode()
    supplier_org_id = Unicode()
    order_date      = Date()
    currency        = Unicode()
    items           = Array(OrderItem)


class OrderResponse(ComplexModel):
    """Confirmation returned by the manufacturer."""
    __namespace__ = "http://retailsync.retail/procurement"

    confirmation_id    = Unicode()
    status             = Unicode()
    estimated_delivery = Date()
    total_price_cents  = Integer()
    message            = Unicode()


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class ProcurementService(Service):
    """Implements the ProcurementPortType from the WSDL."""

    @rpc(PurchaseOrder, _returns=OrderResponse, _operation_name="SubmitOrder")
    def SubmitOrder(ctx, order):
        """Receives a PurchaseOrder and returns a mock OrderResponse."""
        total = 0
        item_count = 0
        if order.items:
            for item in order.items:
                qty = item.quantity if item.quantity else 1
                price = item.unit_price_cents if item.unit_price_cents else 0
                total += qty * price
                item_count += 1

        response = OrderResponse()
        response.confirmation_id    = f"CONF-{order.order_id or 'UNKNOWN'}-001"
        response.status             = "ACCEPTED"
        response.estimated_delivery = date.today() + timedelta(days=14)
        response.total_price_cents  = total
        response.message            = (
            f"Order {order.order_id} accepted with {item_count} item(s). "
            f"Estimated delivery in 14 days."
        )
        return response


# ---------------------------------------------------------------------------
# Application wiring
# ---------------------------------------------------------------------------

application = Application(
    services=[ProcurementService],
    tns="http://retailsync.retail/procurement",
    name="ProcurementService",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8001

    print("=" * 60)
    print("  RetailSync - SOAP Procurement Service")
    print("=" * 60)
    print(f"  SOAP endpoint : http://localhost:{PORT}/")
    print(f"  WSDL          : http://localhost:{PORT}/?wsdl")
    print(f"  Protocol      : SOAP 1.1 / XML")
    print(f"  Operation     : SubmitOrder")
    print("=" * 60)
    print()

    server = make_server(HOST, PORT, wsgi_app)
    server.serve_forever()
