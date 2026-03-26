from datetime import date

from django.test import TestCase

from apps.inventory.services import AllocationService
from apps.items.models import Item
from apps.lpn.services import LPNService
from apps.outbound.models import OrderLine, OutboundOrder
from apps.tenants.models import Tenant
from apps.warehouse.models import Location, Warehouse, Zone
from apps.inventory.services import InventoryService


class AllocationServiceTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(schema_name="alloc", name="Alloc", code="ALC")
        self.item = Item.objects.create(
            tenant=self.tenant,
            sku="SKU-1",
            description_en="Test SKU",
        )
        warehouse = Warehouse.objects.create(tenant=self.tenant, code="WH1", name="Main")
        zone = Zone.objects.create(tenant=self.tenant, warehouse=warehouse, code="A", name="Zone A")
        self.location = Location.objects.create(
            tenant=self.tenant,
            zone=zone,
            code="A-01-01-01",
            aisle="A",
            bay="01",
            level="01",
            position="01",
        )
        self.inventory = InventoryService()
        self.lpn_service = LPNService()

    def test_allocate_order_line_uses_earliest_expiry_first(self):
        first_lpn = self.lpn_service.create(tenant=self.tenant, quantity=10, item=self.item)
        second_lpn = self.lpn_service.create(tenant=self.tenant, quantity=10, item=self.item)
        early = self.inventory.create_position(
            tenant=self.tenant,
            lpn=first_lpn,
            item=self.item,
            location=self.location,
            quantity=10,
            expiry_date=date(2026, 1, 1),
        )
        self.inventory.create_position(
            tenant=self.tenant,
            lpn=second_lpn,
            item=self.item,
            location=self.location,
            quantity=10,
            expiry_date=date(2026, 6, 1),
        )
        order = OutboundOrder.objects.create(tenant=self.tenant, order_number="SO-1")
        line = OrderLine.objects.create(
            tenant=self.tenant,
            outbound_order=order,
            item=self.item,
            line_number=1,
            quantity_requested=5,
        )

        allocations = AllocationService().allocate_order_line(order_line=line, quantity=5)

        self.assertEqual(allocations[0].position.id, early.id)
        early.refresh_from_db()
        self.assertEqual(early.quantity_allocated, 5)
