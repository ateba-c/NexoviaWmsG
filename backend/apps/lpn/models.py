from __future__ import annotations

from django.db import models

from shared.models import TenantAwareModel


class LPNSequence(models.Model):
    tenant = models.OneToOneField("tenants.Tenant", on_delete=models.CASCADE, related_name="lpn_sequence")
    prefix = models.CharField(max_length=16, default="NF")
    last_value = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.tenant.code}:{self.last_value}"


class LPN(TenantAwareModel):
    code = models.CharField(max_length=40, db_index=True)
    item = models.ForeignKey("items.Item", null=True, blank=True, on_delete=models.PROTECT, related_name="lpns")
    quantity_unit = models.CharField(max_length=20, default="EA")
    status = models.CharField(max_length=20, default="OPEN")
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "code"], name="lpn_tenant_code_uniq")
        ]

    def __str__(self) -> str:
        return self.code
