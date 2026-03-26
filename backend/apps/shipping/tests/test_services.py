from django.test import TestCase

from apps.inventory.services import InventoryService
from apps.items.models import Item
from apps.lpn.services import LPNService
from apps.outbound.models import OrderLine, OutboundOrder
from apps.outbound.services import PickTaskService, WaveService
from apps.shipping.services import PackingService, ShippingService
from apps.tenants.models import Tenant
from apps.warehouse.models import Location, Warehouse, Zone


class ShippingFlowTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(schema_name="ship", name="Ship", code="SHP")
        self.item = Item.objects.create(
            tenant=self.tenant,
            sku="SKU-SHIP",
            description_en="Shipping SKU",
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
        inventory = InventoryService()
        lpn = LPNService().create(tenant=self.tenant, quantity=3, item=self.item)
        inventory.create_position(
            tenant=self.tenant,
            lpn=lpn,
            item=self.item,
            location=self.location,
            quantity=3,
        )
        self.order = OutboundOrder.objects.create(tenant=self.tenant, order_number="SO-SHIP")
        OrderLine.objects.create(
            tenant=self.tenant,
            outbound_order=self.order,
            item=self.item,
            line_number=1,
            quantity_requested=3,
        )
        wave = WaveService().create_wave(tenant=self.tenant, orders=[self.order])
        self.wave = WaveService().release_wave(wave=wave)
        PickTaskService().confirm_pick(task=self.wave.pick_tasks.first(), quantity=3)

    def test_pack_and_ship_order(self):
        container = PackingService().pack_order(order=self.order)
        shipment = ShippingService().create_shipment(order=self.order, container=container)
        shipment = ShippingService().mark_shipped(shipment=shipment, tracking_number="TRACK-123")

        self.order.refresh_from_db()
        container.refresh_from_db()
        self.assertEqual(container.status, "SEALED")
        self.assertEqual(self.order.status, "SHIPPED")
        self.assertEqual(shipment.status, "SHIPPED")
