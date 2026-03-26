from django.test import TestCase

from apps.counting.models import CountTask
from apps.counting.services import CountingService
from apps.inventory.services import InventoryService
from apps.items.models import Item
from apps.lpn.services import LPNService
from apps.tenants.models import Tenant
from apps.warehouse.models import Location, Warehouse, Zone


class CountingServiceTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(schema_name="cnt", name="Counting", code="CNT")
        self.item = Item.objects.create(tenant=self.tenant, sku="SKU-CNT", description_en="Count item")
        warehouse = Warehouse.objects.create(tenant=self.tenant, code="WH1", name="Main")
        zone = Zone.objects.create(tenant=self.tenant, warehouse=warehouse, code="C", name="Count")
        self.location = Location.objects.create(
            tenant=self.tenant,
            zone=zone,
            code="C-01-01-01",
            aisle="C",
            bay="01",
            level="01",
            position="01",
        )
        lpn = LPNService().create(tenant=self.tenant, quantity=5, item=self.item)
        InventoryService().create_position(
            tenant=self.tenant,
            lpn=lpn,
            item=self.item,
            location=self.location,
            quantity=5,
        )
        self.task = CountTask.objects.create(
            tenant=self.tenant,
            reference="COUNT-1",
            location=self.location,
        )

    def test_execute_count_creates_variance(self):
        result = CountingService().execute_count(count_task=self.task, item=self.item, counted_quantity=3)

        self.task.refresh_from_db()
        self.assertEqual(result.variance_quantity, -2)
        self.assertEqual(self.task.status, "VARIANCE")
