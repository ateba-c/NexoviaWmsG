from __future__ import annotations

from django.db import transaction

from apps.audit.services import AuditService
from apps.inventory.services import InventoryService
from apps.lpn.services import LPNService

from .models import Disposition, ReturnLine


class ReturnsService:
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
    def receive_return_line(self, *, return_line: ReturnLine, quantity: int, location, actor=None):
        if quantity <= 0:
            raise ValueError("Return quantity must be greater than zero.")
        if return_line.quantity_received + quantity > return_line.quantity_expected:
            raise ValueError("Return quantity exceeds expected quantity.")

        lpn = self.lpn.create(
            tenant=return_line.tenant,
            quantity=quantity,
            item=return_line.item,
            quantity_unit=return_line.item.unit_of_measure,
        )
        position = self.inventory.create_position(
            tenant=return_line.tenant,
            lpn=lpn,
            item=return_line.item,
            location=location,
            quantity=quantity,
            status="AVAILABLE",
        )
        return_line.quantity_received += quantity
        return_line.save(update_fields=["quantity_received", "updated_at"])
        self.audit.log(
            tenant=return_line.tenant,
            action="RECEIVE_RETURN",
            entity_type="ReturnLine",
            entity_id=str(return_line.id),
            actor=actor,
            payload={"position_id": str(position.id), "quantity": quantity},
        )
        return position

    @transaction.atomic
    def dispose_return_line(
        self,
        *,
        return_line: ReturnLine,
        action: str,
        quantity: int,
        notes: str = "",
        actor=None,
    ) -> Disposition:
        position = (
            return_line.item.inventory_positions.filter(tenant=return_line.tenant)
            .order_by("-created_at")
            .first()
        )
        disposition = Disposition.objects.create(
            tenant=return_line.tenant,
            return_line=return_line,
            inventory_position=position,
            action=action,
            quantity=quantity,
            notes=notes,
        )
        return_line.disposition_status = action
        return_line.save(update_fields=["disposition_status", "updated_at"])
        self.audit.log(
            tenant=return_line.tenant,
            action="DISPOSE_RETURN",
            entity_type="ReturnLine",
            entity_id=str(return_line.id),
            actor=actor,
            payload={"action": action, "quantity": quantity},
        )
        return disposition
