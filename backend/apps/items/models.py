from __future__ import annotations

from django.db import models

from shared.models import TenantAwareModel


class Item(TenantAwareModel):
    sku = models.CharField(max_length=100, db_index=True)
    gtin = models.CharField(max_length=14, blank=True, db_index=True)
    upc = models.CharField(max_length=12, blank=True)
    description_en = models.CharField(max_length=300)
    description_fr = models.CharField(max_length=300, blank=True)
    unit_of_measure = models.CharField(max_length=20, default="EA")
    units_per_inner = models.PositiveIntegerField(default=1)
    units_per_case = models.PositiveIntegerField(default=1)
    cases_per_pallet = models.PositiveIntegerField(default=1)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    length_cm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    width_cm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    lot_controlled = models.BooleanField(default=False)
    serial_tracked = models.BooleanField(default=False)
    expiry_tracked = models.BooleanField(default=False)
    catch_weight = models.BooleanField(default=False)
    shelf_life_days = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sku"]
        constraints = [
            models.UniqueConstraint(fields=["tenant", "sku"], name="items_tenant_sku_uniq")
        ]

    def __str__(self) -> str:
        return self.sku
