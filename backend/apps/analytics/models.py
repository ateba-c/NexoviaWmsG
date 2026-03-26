from django.db import models

from shared.models import TenantAwareModel


class MetricSnapshot(TenantAwareModel):
    metric = models.CharField(max_length=64)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    captured_for = models.DateTimeField()
    dimension = models.CharField(max_length=64, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "metric", "captured_for"])]


class KPIReport(TenantAwareModel):
    report_date = models.DateField(db_index=True)
    orders_received = models.PositiveIntegerField(default=0)
    orders_shipped = models.PositiveIntegerField(default=0)
    returns_received = models.PositiveIntegerField(default=0)
    picks_completed = models.PositiveIntegerField(default=0)
    count_tasks_completed = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "report_date"], name="analytics_kpi_tenant_report_date_uniq")
        ]
