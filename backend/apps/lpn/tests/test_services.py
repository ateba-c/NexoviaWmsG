from django.test import TestCase

from apps.lpn.services import LPNService
from apps.tenants.models import Tenant


class LPNServiceTests(TestCase):
    def test_create_generates_per_tenant_sequence(self):
        tenant = Tenant.objects.create(schema_name="tenant_two", name="Tenant Two", code="T2")
        service = LPNService()

        first = service.create(tenant=tenant, quantity=5)
        second = service.create(tenant=tenant, quantity=3)

        self.assertTrue(first.code.endswith("0000000001"))
        self.assertTrue(second.code.endswith("0000000002"))
