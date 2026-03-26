from django.db import models

from shared.models import TenantAwareModel


class CountTask(TenantAwareModel):
    reference = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="OPEN")
    location = models.ForeignKey("warehouse.Location", on_delete=models.PROTECT, related_name="count_tasks")
    task_type = models.CharField(max_length=20, default="CYCLE")
    assigned_to = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="count_tasks",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "reference"], name="counting_task_tenant_reference_uniq")
        ]


class CountResult(TenantAwareModel):
    count_task = models.ForeignKey(CountTask, on_delete=models.CASCADE, related_name="results")
    item = models.ForeignKey("items.Item", on_delete=models.PROTECT, related_name="count_results")
    expected_quantity = models.PositiveIntegerField(default=0)
    counted_quantity = models.PositiveIntegerField(default=0)
    variance_quantity = models.IntegerField(default=0)


class CountVariance(TenantAwareModel):
    count_result = models.OneToOneField(CountResult, on_delete=models.CASCADE, related_name="variance")
    status = models.CharField(max_length=20, default="OPEN")
    approved_by = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_variances",
    )
    approval_notes = models.TextField(blank=True)
