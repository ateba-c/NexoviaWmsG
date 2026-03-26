from __future__ import annotations

from dataclasses import dataclass

from django.db import transaction
from django.db.models import F, QuerySet

from .models import InventoryMovement, InventoryPosition


class InsufficientInventoryError(Exception):
    pass


@dataclass(slots=True)
class AllocationResult:
    position: InventoryPosition
    quantity: int


class InventoryService:
    """Core stock mutation service."""

    @transaction.atomic
    def create_position(
        self,
        *,
        tenant,
        lpn,
        item,
        location,
        quantity: int,
        lot_number: str = "",
        serial_number: str = "",
        expiry_date=None,
        status: str = "AVAILABLE",
    ) -> InventoryPosition:
        position = InventoryPosition.objects.create(
            tenant=tenant,
            lpn=lpn,
            item=item,
            location=location,
            lot_number=lot_number,
            serial_number=serial_number,
            expiry_date=expiry_date,
            quantity_on_hand=quantity,
            status=status,
            is_available=status == "AVAILABLE",
        )
        InventoryMovement.objects.create(
            tenant=tenant,
            position=position,
            lpn=lpn,
            item=item,
            movement_type="RECEIVE",
            quantity=quantity,
            to_location=location,
            reference_type="INVENTORY_POSITION",
            reference_id=str(position.id),
        )
        return position

    @transaction.atomic
    def move(self, *, position: InventoryPosition, to_location, quantity: int) -> InventoryPosition:
        previous_location = position.location
        position.location = to_location
        position.save(update_fields=["location", "updated_at"])
        InventoryMovement.objects.create(
            tenant=position.tenant,
            position=position,
            movement_type="MOVE",
            lpn=position.lpn,
            item=position.item,
            quantity=quantity,
            from_location=previous_location,
            to_location=to_location,
            reference_type="INVENTORY_POSITION",
            reference_id=str(position.id),
        )
        return position

    @transaction.atomic
    def allocate(self, *, position: InventoryPosition, quantity: int, reference_type: str, reference_id: str) -> InventoryPosition:
        if position.quantity_available < quantity:
            raise InsufficientInventoryError("Not enough available stock to allocate.")
        position.quantity_allocated = F("quantity_allocated") + quantity
        position.save(update_fields=["quantity_allocated", "updated_at"])
        position.refresh_from_db()
        InventoryMovement.objects.create(
            tenant=position.tenant,
            position=position,
            lpn=position.lpn,
            item=position.item,
            movement_type="ALLOCATE",
            quantity=quantity,
            from_location=position.location,
            to_location=position.location,
            reference_type=reference_type,
            reference_id=reference_id,
        )
        return position


class AllocationService:
    """Allocates inventory using FEFO semantics and row locking."""

    def _candidate_positions(self, *, tenant, item) -> QuerySet[InventoryPosition]:
        return (
            InventoryPosition.objects.select_for_update()
            .filter(tenant=tenant, item=item, status="AVAILABLE", is_available=True, quantity_on_hand__gt=0)
            .order_by(F("expiry_date").asc(nulls_last=True), "created_at")
        )

    @transaction.atomic
    def allocate_order_line(self, *, order_line, quantity: int) -> list[AllocationResult]:
        remaining = quantity
        allocations: list[AllocationResult] = []
        inventory_service = InventoryService()

        for position in self._candidate_positions(tenant=order_line.tenant, item=order_line.item):
            available = position.quantity_available
            if available <= 0:
                continue
            allocated_qty = min(available, remaining)
            inventory_service.allocate(
                position=position,
                quantity=allocated_qty,
                reference_type="ORDER_LINE",
                reference_id=str(order_line.id),
            )
            allocations.append(AllocationResult(position=position, quantity=allocated_qty))
            remaining -= allocated_qty
            if remaining == 0:
                break

        if remaining > 0:
            raise InsufficientInventoryError("Insufficient stock for requested allocation.")

        order_line.quantity_allocated = F("quantity_allocated") + quantity
        order_line.save(update_fields=["quantity_allocated", "updated_at"])
        order_line.refresh_from_db()
        return allocations
