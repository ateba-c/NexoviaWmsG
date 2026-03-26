from django.test import TestCase

from apps.items.models import Item
from apps.returns.models import ReturnLine, ReturnOrder
from apps.returns.services import ReturnsService
from apps.tenants.models import Tenant
from apps.warehouse.models import Location, Warehouse, Zone


class ReturnsServiceTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(schema_name="ret", name="Returns", code="RET")
        self.item = Item.objects.create(tenant=self.tenant, sku="SKU-RET", description_en="Return item")
        warehouse = Warehouse.objects.create(tenant=self.tenant, code="WH1", name="Main")
        zone = Zone.objects.create(tenant=self.tenant, warehouse=warehouse, code="R", name="Returns")
        self.location = Location.objects.create(
            tenant=self.tenant,
            zone=zone,
            code="R-01-01-01",
            aisle="R",
            bay="01",
            level="01",
            position="01",
        )
        self.order = ReturnOrder.objects.create(tenant=self.tenant, rma_number="RMA-1")
        self.line = ReturnLine.objects.create(
            tenant=self.tenant,
            return_order=self.order,
            item=self.item,
            line_number=1,
            quantity_expected=2,
        )

    def test_receive_and_dispose_return_line(self):
        service = ReturnsService()
        position = service.receive_return_line(return_line=self.line, quantity=2, location=self.location)
        disposition = service.dispose_return_line(return_line=self.line, action="RESTOCK", quantity=2)

        self.line.refresh_from_db()
        self.assertEqual(self.line.quantity_received, 2)
        self.assertEqual(disposition.inventory_position_id, position.id)

