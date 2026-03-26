from datetime import date

from django.test import TestCase

from apps.inventory.services import InventoryService
from apps.items.models import Item
from apps.lpn.services import LPNService
from apps.outbound.models import OrderLine, OutboundOrder
from apps.outbound.services import PickTaskService, WaveService
from apps.tenants.models import Tenant
from apps.warehouse.models import Location, Warehouse, Zone


class WaveServiceTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(schema_name="wave", name="Wave", code="WAV")
        self.item = Item.objects.create(
            tenant=self.tenant,
            sku="SKU-WAVE",
            description_en="Wave SKU",
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

    def test_release_wave_creates_pick_tasks(self):
        lpn = self.lpn_service.create(tenant=self.tenant, quantity=10, item=self.item)
        self.inventory.create_position(
            tenant=self.tenant,
            lpn=lpn,
            item=self.item,
            location=self.location,
            quantity=10,
            expiry_date=date(2026, 1, 1),
        )
        order = OutboundOrder.objects.create(tenant=self.tenant, order_number="SO-WAVE")
        OrderLine.objects.create(
            tenant=self.tenant,
            outbound_order=order,
            item=self.item,
            line_number=1,
            quantity_requested=4,
        )

        service = WaveService()
        wave = service.create_wave(tenant=self.tenant, orders=[order])
        service.release_wave(wave=wave)

        self.assertEqual(wave.pick_tasks.count(), 1)
        self.assertEqual(wave.pick_tasks.first().quantity_to_pick, 4)


class PickTaskServiceTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(schema_name="pick", name="Pick", code="PCK")
        self.item = Item.objects.create(
            tenant=self.tenant,
            sku="SKU-PICK",
            description_en="Pick SKU",
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
        lpn = LPNService().create(tenant=self.tenant, quantity=5, item=self.item)
        inventory.create_position(
            tenant=self.tenant,
            lpn=lpn,
            item=self.item,
            location=self.location,
            quantity=5,
        )
        self.order = OutboundOrder.objects.create(tenant=self.tenant, order_number="SO-PICK")
        self.line = OrderLine.objects.create(
            tenant=self.tenant,
            outbound_order=self.order,
            item=self.item,
            line_number=1,
            quantity_requested=5,
        )
        wave = WaveService().create_wave(tenant=self.tenant, orders=[self.order])
        self.wave = WaveService().release_wave(wave=wave)

    def test_confirm_pick_marks_task_completed(self):
        task = self.wave.pick_tasks.first()

        PickTaskService().confirm_pick(task=task, quantity=5)

        task.refresh_from_db()
        self.line.refresh_from_db()
        self.order.refresh_from_db()
        self.assertEqual(task.status, "COMPLETED")
        self.assertEqual(self.line.quantity_picked, 5)
        self.assertEqual(self.order.status, "PICKED")
