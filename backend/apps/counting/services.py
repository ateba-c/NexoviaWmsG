from __future__ import annotations

from django.db import transaction

from apps.audit.services import AuditService
from apps.inventory.models import InventoryPosition

from .models import CountResult, CountTask, CountVariance


class CountingService:
    def __init__(self, audit_service: AuditService | None = None) -> None:
        self.audit = audit_service or AuditService()

    @transaction.atomic
    def execute_count(self, *, count_task: CountTask, item, counted_quantity: int, actor=None) -> CountResult:
        expected_quantity = (
            InventoryPosition.objects.filter(
                tenant=count_task.tenant,
                item=item,
                location=count_task.location,
            )
            .values_list("quantity_on_hand", flat=True)
            .first()
            or 0
        )
        variance_quantity = counted_quantity - expected_quantity
        result = CountResult.objects.create(
            tenant=count_task.tenant,
            count_task=count_task,
            item=item,
            expected_quantity=expected_quantity,
            counted_quantity=counted_quantity,
            variance_quantity=variance_quantity,
        )
        if variance_quantity != 0:
            CountVariance.objects.create(
                tenant=count_task.tenant,
                count_result=result,
                status="OPEN",
            )
            count_task.status = "VARIANCE"
        else:
            count_task.status = "COMPLETED"
        count_task.save(update_fields=["status", "updated_at"])
        self.audit.log(
            tenant=count_task.tenant,
            action="EXECUTE_COUNT",
            entity_type="CountTask",
            entity_id=str(count_task.id),
            actor=actor,
            payload={"result_id": str(result.id), "variance_quantity": variance_quantity},
        )
        return result

    @transaction.atomic
    def approve_variance(self, *, variance: CountVariance, actor=None, notes: str = "") -> CountVariance:
        variance.status = "APPROVED"
        variance.approved_by = actor
        variance.approval_notes = notes
        variance.save(update_fields=["status", "approved_by", "approval_notes", "updated_at"])

        result = variance.count_result
        position = (
            InventoryPosition.objects.filter(
                tenant=result.tenant,
                item=result.item,
                location=result.count_task.location,
            )
            .order_by("-created_at")
            .first()
        )
        if position is not None:
            position.quantity_on_hand = result.counted_quantity
            position.save(update_fields=["quantity_on_hand", "updated_at"])
        result.count_task.status = "COMPLETED"
        result.count_task.save(update_fields=["status", "updated_at"])
        self.audit.log(
            tenant=variance.tenant,
            action="APPROVE_VARIANCE",
            entity_type="CountVariance",
            entity_id=str(variance.id),
            actor=actor,
            payload={"count_result_id": str(result.id)},
        )
        return variance
