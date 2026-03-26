from django.db import models

from shared.models import TenantAwareModel


class OutboundOrder(TenantAwareModel):
    order_number = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="RECEIVED")
    customer_name = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "order_number"], name="outbound_order_tenant_number_uniq")
        ]


class OrderLine(TenantAwareModel):
    outbound_order = models.ForeignKey(OutboundOrder, on_delete=models.CASCADE, related_name="lines")
    item = models.ForeignKey("items.Item", on_delete=models.PROTECT, related_name="order_lines")
    line_number = models.PositiveIntegerField()
    quantity_requested = models.PositiveIntegerField()
    quantity_allocated = models.PositiveIntegerField(default=0)
    quantity_picked = models.PositiveIntegerField(default=0)
    quantity_packed = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["outbound_order", "line_number"],
                name="outbound_order_line_number_uniq",
            )
        ]


class Wave(TenantAwareModel):
    wave_number = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="DRAFT")
    release_notes = models.TextField(blank=True)
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "wave_number"], name="outbound_wave_tenant_number_uniq")
        ]


class WaveOrder(TenantAwareModel):
    wave = models.ForeignKey(Wave, on_delete=models.CASCADE, related_name="wave_orders")
    outbound_order = models.ForeignKey(OutboundOrder, on_delete=models.CASCADE, related_name="wave_orders")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["wave", "outbound_order"], name="outbound_wave_order_uniq")
        ]


class PickTask(TenantAwareModel):
    wave = models.ForeignKey(Wave, on_delete=models.CASCADE, related_name="pick_tasks")
    order_line = models.ForeignKey(OrderLine, on_delete=models.CASCADE, related_name="pick_tasks")
    inventory_position = models.ForeignKey(
        "inventory.InventoryPosition",
        on_delete=models.PROTECT,
        related_name="pick_tasks",
    )
    task_number = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="OPEN")
    quantity_to_pick = models.PositiveIntegerField()
    quantity_picked = models.PositiveIntegerField(default=0)
    sequence = models.PositiveIntegerField(default=0)
    assigned_to = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pick_tasks",
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "task_number"], name="outbound_pick_task_number_uniq")
        ]


class Container(TenantAwareModel):
    outbound_order = models.ForeignKey(OutboundOrder, on_delete=models.CASCADE, related_name="containers")
    container_number = models.CharField(max_length=64)
    container_type = models.CharField(max_length=30, default="CARTON")
    status = models.CharField(max_length=20, default="OPEN")
    quantity_packed = models.PositiveIntegerField(default=0)
    sealed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "container_number"],
                name="outbound_container_tenant_number_uniq",
            )
        ]
