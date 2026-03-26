from django.test import TestCase

from apps.integrations.services import IntegrationService
from apps.tenants.models import Tenant


class IntegrationServiceTests(TestCase):
    def test_log_event_creates_connector_log(self):
        tenant = Tenant.objects.create(schema_name="int", name="Integrations", code="INT")
        log = IntegrationService().log_event(
            tenant=tenant,
            system="erp",
            event_type="order.created",
            status="SUCCESS",
            reference_id="123",
        )

        self.assertEqual(log.system, "erp")
        self.assertEqual(log.event_type, "order.created")

