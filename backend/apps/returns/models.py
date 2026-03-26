from django.db import models

from shared.models import TenantAwareModel


class ReturnOrder(TenantAwareModel):
    rma_number = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="OPEN")
    customer_name = models.CharField(max_length=255, blank=True)
    reason_code = models.CharField(max_length=64, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "rma_number"], name="returns_rma_tenant_number_uniq")
        ]


class ReturnLine(TenantAwareModel):
    return_order = models.ForeignKey(ReturnOrder, on_delete=models.CASCADE, related_name="lines")
    item = models.ForeignKey("items.Item", on_delete=models.PROTECT, related_name="return_lines")
    line_number = models.PositiveIntegerField()
    quantity_expected = models.PositiveIntegerField(default=1)
    quantity_received = models.PositiveIntegerField(default=0)
    disposition_status = models.CharField(max_length=20, default="PENDING")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["return_order", "line_number"], name="returns_line_order_number_uniq")
        ]


class Disposition(TenantAwareModel):
    return_line = models.ForeignKey(ReturnLine, on_delete=models.CASCADE, related_name="dispositions")
    inventory_position = models.ForeignKey(
        "inventory.InventoryPosition",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dispositions",
    )
    action = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
