from datetime import date

from django.test import TestCase

from apps.analytics.services import AnalyticsService
from apps.outbound.models import OutboundOrder
from apps.tenants.models import Tenant


class AnalyticsServiceTests(TestCase):
    def test_refresh_daily_report_creates_report(self):
        tenant = Tenant.objects.create(schema_name="anl", name="Analytics", code="ANL")
        OutboundOrder.objects.create(tenant=tenant, order_number="SO-1")

        report = AnalyticsService().refresh_daily_report(tenant=tenant, report_date=date.today())

        self.assertEqual(report.orders_received, 1)
