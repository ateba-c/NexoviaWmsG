from __future__ import annotations

from django.db import transaction

from apps.audit.services import AuditService
from apps.inventory.services import InventoryService
from apps.lpn.services import LPNService

from .models import InboundLine, ReceiveEvent


class ReceivingService:
    """Orchestrates a receive transaction for an inbound line."""

    def __init__(
        self,
        inventory_service: InventoryService | None = None,
        lpn_service: LPNService | None = None,
        audit_service: AuditService | None = None,
    ) -> None:
        self.inventory = inventory_service or InventoryService()
        self.lpn = lpn_service or LPNService()
        self.audit = audit_service or AuditService()

    @transaction.atomic
    def receive_line(
        self,
        *,
        inbound_line: InboundLine,
        quantity: int,
        location,
        lot_number: str = "",
        expiry_date=None,
        actor=None,
    ) -> dict:
        if quantity <= 0:
            raise ValueError("Received quantity must be greater than zero.")
        if inbound_line.qty_received + quantity > inbound_line.qty_expected:
            raise ValueError("Received quantity exceeds expected quantity.")

        lpn = self.lpn.create(
            tenant=inbound_line.tenant,
            quantity=quantity,
            item=inbound_line.item,
            quantity_unit=inbound_line.item.unit_of_measure,
        )
        position = self.inventory.create_position(
            tenant=inbound_line.tenant,
            lpn=lpn,
            item=inbound_line.item,
            location=location,
            quantity=quantity,
            lot_number=lot_number,
            expiry_date=expiry_date,
            status="AVAILABLE",
        )
        event = ReceiveEvent.objects.create(
            tenant=inbound_line.tenant,
            inbound_line=inbound_line,
            lpn=lpn,
            location=location,
            quantity_received=quantity,
            lot_number=lot_number,
            expiry_date=expiry_date,
            operator_id=str(actor.pk) if actor is not None else "",
        )
        inbound_line.qty_received += quantity
        inbound_line.save(update_fields=["qty_received", "updated_at"])
        self.audit.log(
            tenant=inbound_line.tenant,
            action="RECEIVE_LINE",
            entity_type="InboundLine",
            entity_id=str(inbound_line.id),
            actor=actor,
            payload={
                "event_id": str(event.id),
                "lpn_id": str(lpn.id),
                "position_id": str(position.id),
                "quantity": quantity,
            },
        )
        return {
            "lpn_id": str(lpn.id),
            "position_id": str(position.id),
            "receive_event_id": str(event.id),
        }
