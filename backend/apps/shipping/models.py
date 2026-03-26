from django.db import models

from shared.models import TenantAwareModel


class Shipment(TenantAwareModel):
    outbound_order = models.ForeignKey(
        "outbound.OutboundOrder",
        on_delete=models.CASCADE,
        related_name="shipments",
    )
    container = models.ForeignKey(
        "outbound.Container",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="shipments",
    )
    shipment_number = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="DRAFT")
    carrier_name = models.CharField(max_length=128, blank=True)
    service_level = models.CharField(max_length=64, blank=True)
    tracking_number = models.CharField(max_length=128, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "shipment_number"], name="shipping_shipment_tenant_number_uniq")
        ]


class Manifest(TenantAwareModel):
    manifest_number = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="OPEN")
    shipped_at = models.DateTimeField(null=True, blank=True)
    shipments = models.ManyToManyField(Shipment, related_name="manifests", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "manifest_number"], name="shipping_manifest_tenant_number_uniq")
        ]
