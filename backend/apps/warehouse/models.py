from __future__ import annotations

from django.db import models

from shared.models import TenantAwareModel


class Warehouse(TenantAwareModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    address = models.JSONField(default=dict, blank=True)
    timezone = models.CharField(max_length=50, default="America/Toronto")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "code"], name="warehouse_tenant_code_uniq")
        ]

    def __str__(self) -> str:
        return self.name


class Zone(TenantAwareModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="zones")
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    zone_type = models.CharField(max_length=30, default="GENERAL")
    temp_controlled = models.BooleanField(default=False)
    temp_min_c = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temp_max_c = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["warehouse", "code"], name="warehouse_zone_code_uniq")
        ]


class Location(TenantAwareModel):
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="locations")
    code = models.CharField(max_length=50)
    aisle = models.CharField(max_length=10, db_index=True)
    bay = models.CharField(max_length=10)
    level = models.CharField(max_length=10)
    position = models.CharField(max_length=10)
    location_type = models.CharField(max_length=20, default="PICK_FACE")
    storage_strategy = models.CharField(max_length=20, default="FLOATING")
    max_weight_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    max_volume_m3 = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    max_units = models.PositiveIntegerField(null=True, blank=True)
    length_cm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    width_cm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    requires_lift = models.BooleanField(default=False)
    sort_sequence = models.IntegerField(default=0, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["zone", "code"], name="warehouse_location_zone_code_uniq")
        ]
