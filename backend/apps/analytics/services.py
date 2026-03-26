from __future__ import annotations

from datetime import date
from decimal import Decimal

from apps.counting.models import CountTask
from apps.outbound.models import OutboundOrder, PickTask
from apps.returns.models import ReturnOrder

from .models import KPIReport, MetricSnapshot


class AnalyticsService:
    def refresh_daily_report(self, *, tenant, report_date: date) -> KPIReport:
        orders_received = OutboundOrder.objects.filter(
            tenant=tenant,
            created_at__date=report_date,
        ).count()
        orders_shipped = OutboundOrder.objects.filter(
            tenant=tenant,
            status="SHIPPED",
            updated_at__date=report_date,
        ).count()
        returns_received = ReturnOrder.objects.filter(
            tenant=tenant,
            updated_at__date=report_date,
        ).count()
        picks_completed = PickTask.objects.filter(
            tenant=tenant,
            status="COMPLETED",
            completed_at__date=report_date,
        ).count()
        count_tasks_completed = CountTask.objects.filter(
            tenant=tenant,
            status="COMPLETED",
            updated_at__date=report_date,
        ).count()

        report, _ = KPIReport.objects.update_or_create(
            tenant=tenant,
            report_date=report_date,
            defaults={
                "orders_received": orders_received,
                "orders_shipped": orders_shipped,
                "returns_received": returns_received,
                "picks_completed": picks_completed,
                "count_tasks_completed": count_tasks_completed,
            },
        )

        MetricSnapshot.objects.create(
            tenant=tenant,
            metric="orders_shipped",
            value=Decimal(orders_shipped),
            captured_for=report_date,
            metadata={"report_date": report_date.isoformat()},
        )
        return report

    def summary(self, *, tenant) -> dict:
        latest_report = KPIReport.objects.filter(tenant=tenant).order_by("-report_date").first()
        if latest_report is None:
            return {
                "orders_received": 0,
                "orders_shipped": 0,
                "returns_received": 0,
                "picks_completed": 0,
                "count_tasks_completed": 0,
            }
        return {
            "orders_received": latest_report.orders_received,
            "orders_shipped": latest_report.orders_shipped,
            "returns_received": latest_report.returns_received,
            "picks_completed": latest_report.picks_completed,
            "count_tasks_completed": latest_report.count_tasks_completed,
        }
