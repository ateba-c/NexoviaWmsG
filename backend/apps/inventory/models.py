from __future__ import annotations

from django.db import models

from shared.models import TenantAwareModel


class InventoryPosition(TenantAwareModel):
    lpn = models.ForeignKey("lpn.LPN", on_delete=models.PROTECT, related_name="positions")
    item = models.ForeignKey("items.Item", on_delete=models.PROTECT, related_name="inventory_positions")
    location = models.ForeignKey("warehouse.Location", on_delete=models.PROTECT, related_name="inventory_positions")
    lot_number = models.CharField(max_length=100, blank=True, db_index=True)
    serial_number = models.CharField(max_length=100, blank=True, db_index=True)
    expiry_date = models.DateField(null=True, blank=True, db_index=True)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    quantity_allocated = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="AVAILABLE")
    is_available = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "lpn", "location"],
                name="inventory_position_tenant_lpn_location_uniq",
            )
        ]
        indexes = [
            models.Index(fields=["tenant", "item", "status"]),
            models.Index(fields=["tenant", "expiry_date"]),
        ]

    @property
    def quantity_available(self) -> int:
        return max(self.quantity_on_hand - self.quantity_allocated, 0)


class InventoryMovement(TenantAwareModel):
    movement_type = models.CharField(max_length=30)
    position = models.ForeignKey(
        InventoryPosition,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="movements",
    )
    lpn = models.ForeignKey("lpn.LPN", on_delete=models.PROTECT, related_name="movements")
    item = models.ForeignKey("items.Item", on_delete=models.PROTECT, related_name="inventory_movements")
    quantity = models.IntegerField()
    from_location = models.ForeignKey(
        "warehouse.Location",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="outbound_movements",
    )
    to_location = models.ForeignKey(
        "warehouse.Location",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="inbound_movements",
    )
    reference_type = models.CharField(max_length=50, blank=True)
    reference_id = models.CharField(max_length=64, blank=True, db_index=True)
    notes = models.TextField(blank=True)
