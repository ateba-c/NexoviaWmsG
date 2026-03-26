from django.db import models

from shared.models import TenantAwareModel


class InboundOrder(TenantAwareModel):
    order_number = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="OPEN")
    supplier_name = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "order_number"], name="inbound_order_tenant_number_uniq")
        ]


class InboundLine(TenantAwareModel):
    inbound_order = models.ForeignKey(InboundOrder, on_delete=models.CASCADE, related_name="lines")
    item = models.ForeignKey("items.Item", on_delete=models.PROTECT, related_name="inbound_lines")
    line_number = models.PositiveIntegerField()
    qty_expected = models.PositiveIntegerField()
    qty_received = models.PositiveIntegerField(default=0)
    requires_lot = models.BooleanField(default=False)
    requires_expiry = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["inbound_order", "line_number"],
                name="inbound_line_order_line_number_uniq",
            )
        ]


class ReceiveEvent(TenantAwareModel):
    inbound_line = models.ForeignKey(InboundLine, on_delete=models.CASCADE, related_name="receive_events")
    lpn = models.ForeignKey("lpn.LPN", on_delete=models.PROTECT, related_name="receive_events")
    location = models.ForeignKey("warehouse.Location", on_delete=models.PROTECT, related_name="receive_events")
    quantity_received = models.PositiveIntegerField()
    lot_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    operator_id = models.CharField(max_length=64, blank=True)
