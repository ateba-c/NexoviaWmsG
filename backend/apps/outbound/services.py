from __future__ import annotations

from uuid import uuid4

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.inventory.services import AllocationService

from .models import OrderLine, OutboundOrder, PickTask, Wave, WaveOrder


class WaveService:
    def __init__(self, allocation_service: AllocationService | None = None) -> None:
        self.allocation_service = allocation_service or AllocationService()

    @transaction.atomic
    def create_wave(self, *, tenant, orders: list[OutboundOrder], release_notes: str = "") -> Wave:
        wave = Wave.objects.create(
            tenant=tenant,
            wave_number=f"WAVE-{tenant.code}-{timezone.now():%Y%m%d%H%M%S}",
            release_notes=release_notes,
        )
        WaveOrder.objects.bulk_create(
            [WaveOrder(tenant=tenant, wave=wave, outbound_order=order) for order in orders]
        )
        return wave

    @transaction.atomic
    def release_wave(self, *, wave: Wave) -> Wave:
        sequence = 10
        for wave_order in wave.wave_orders.select_related("outbound_order").all():
            order = wave_order.outbound_order
            for line in order.lines.select_related("item").all().order_by("line_number"):
                remaining = line.quantity_requested - line.quantity_allocated
                if remaining <= 0:
                    continue
                allocations = self.allocation_service.allocate_order_line(order_line=line, quantity=remaining)
                tasks: list[PickTask] = []
                for allocation in allocations:
                    tasks.append(
                        PickTask(
                            tenant=wave.tenant,
                            wave=wave,
                            order_line=line,
                            inventory_position=allocation.position,
                            task_number=f"PT-{wave.tenant.code}-{uuid4().hex[:10].upper()}",
                            quantity_to_pick=allocation.quantity,
                            sequence=sequence,
                        )
                    )
                    sequence += 10
                PickTask.objects.bulk_create(tasks)
                order.status = "WAVED"
                order.save(update_fields=["status", "updated_at"])
        wave.status = "RELEASED"
        wave.released_at = timezone.now()
        wave.save(update_fields=["status", "released_at", "updated_at"])
        return wave


class PickTaskService:
    @transaction.atomic
    def start_task(self, *, task: PickTask, user) -> PickTask:
        if task.status not in {"OPEN", "ASSIGNED"}:
            raise ValueError("Only open or assigned tasks can be started.")
        task.status = "IN_PROGRESS"
        task.assigned_to = user
        task.started_at = task.started_at or timezone.now()
        task.save(update_fields=["status", "assigned_to", "started_at", "updated_at"])
        return task

    @transaction.atomic
    def confirm_pick(self, *, task: PickTask, quantity: int) -> PickTask:
        if quantity <= 0:
            raise ValueError("Picked quantity must be greater than zero.")
        if quantity > task.quantity_to_pick:
            raise ValueError("Picked quantity exceeds requested quantity.")

        task.quantity_picked = quantity
        task.status = "COMPLETED" if quantity == task.quantity_to_pick else "SHORT"
        task.completed_at = timezone.now()
        task.save(update_fields=["quantity_picked", "status", "completed_at", "updated_at"])

        line = task.order_line
        line.quantity_picked = (
            line.pick_tasks.aggregate(total=Sum("quantity_picked")).get("total") or 0
        )
        line.save(update_fields=["quantity_picked", "updated_at"])

        order = line.outbound_order
        if all(order.lines.values_list("quantity_picked", flat=True)):
            if all(
                current_line.quantity_picked >= current_line.quantity_requested
                for current_line in order.lines.all()
            ):
                order.status = "PICKED"
                order.save(update_fields=["status", "updated_at"])
        return task
