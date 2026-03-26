from __future__ import annotations

from uuid import uuid4

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.audit.services import AuditService
from apps.outbound.models import Container, OutboundOrder

from .models import Manifest, Shipment


class PackingService:
    def __init__(self, audit_service: AuditService | None = None) -> None:
        self.audit = audit_service or AuditService()

    @transaction.atomic
    def pack_order(
        self,
        *,
        order: OutboundOrder,
        container_type: str = "CARTON",
        actor=None,
    ) -> Container:
        if not all(line.quantity_picked >= line.quantity_requested for line in order.lines.all()):
            raise ValueError("All order lines must be fully picked before packing.")

        container = Container.objects.create(
            tenant=order.tenant,
            outbound_order=order,
            container_number=f"CT-{order.tenant.code}-{uuid4().hex[:10].upper()}",
            container_type=container_type,
            status="SEALED",
            quantity_packed=sum(line.quantity_requested for line in order.lines.all()),
            sealed_at=timezone.now(),
        )
        for line in order.lines.all():
            line.quantity_packed = line.quantity_requested
            line.save(update_fields=["quantity_packed", "updated_at"])
        order.status = "PACKED"
        order.save(update_fields=["status", "updated_at"])
        self.audit.log(
            tenant=order.tenant,
            action="PACK_ORDER",
            entity_type="OutboundOrder",
            entity_id=str(order.id),
            actor=actor,
            payload={"container_id": str(container.id)},
        )
        return container


class ShippingService:
    def __init__(self, audit_service: AuditService | None = None) -> None:
        self.audit = audit_service or AuditService()

    @transaction.atomic
    def create_shipment(
        self,
        *,
        order: OutboundOrder,
        container: Container | None = None,
        carrier_name: str = "",
        service_level: str = "",
    ) -> Shipment:
        if order.status not in {"PACKED", "STAGED"}:
            raise ValueError("Order must be packed before shipment creation.")
        return Shipment.objects.create(
            tenant=order.tenant,
            outbound_order=order,
            container=container,
            shipment_number=f"SHP-{order.tenant.code}-{uuid4().hex[:10].upper()}",
            status="READY",
            carrier_name=carrier_name,
            service_level=service_level,
        )

    @transaction.atomic
    def mark_shipped(self, *, shipment: Shipment, tracking_number: str = "", actor=None) -> Shipment:
        shipment.status = "SHIPPED"
        shipment.tracking_number = tracking_number
        shipment.shipped_at = timezone.now()
        shipment.save(update_fields=["status", "tracking_number", "shipped_at", "updated_at"])
        order = shipment.outbound_order
        order.status = "SHIPPED"
        order.save(update_fields=["status", "updated_at"])
        self.audit.log(
            tenant=shipment.tenant,
            action="SHIP_ORDER",
            entity_type="Shipment",
            entity_id=str(shipment.id),
            actor=actor,
            payload={"tracking_number": tracking_number},
        )
        return shipment

    @transaction.atomic
    def create_manifest(self, *, tenant, shipments: list[Shipment]) -> Manifest:
        manifest = Manifest.objects.create(
            tenant=tenant,
            manifest_number=f"MNF-{tenant.code}-{uuid4().hex[:10].upper()}",
        )
        manifest.shipments.set(shipments)
        return manifest
