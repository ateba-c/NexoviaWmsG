from __future__ import annotations

from dataclasses import dataclass

from django.db import transaction

from apps.tenants.models import Tenant

from .models import LPN, LPNSequence


@dataclass(slots=True)
class LPNCodeParts:
    prefix: str
    tenant_code: str


class LPNService:
    @transaction.atomic
    def generate_code(self, parts: LPNCodeParts) -> str:
        sequence, _ = LPNSequence.objects.select_for_update().get_or_create(
            tenant=Tenant.objects.get(code=parts.tenant_code),
            defaults={"prefix": parts.prefix},
        )
        sequence.last_value += 1
        if sequence.prefix != parts.prefix:
            sequence.prefix = parts.prefix
        sequence.save(update_fields=["prefix", "last_value"])
        return f"{sequence.prefix}-{parts.tenant_code}-{sequence.last_value:010d}"

    @transaction.atomic
    def create(self, *, tenant: Tenant, quantity: int = 0, item=None, quantity_unit: str = "EA") -> LPN:
        code = self.generate_code(LPNCodeParts(prefix="NF", tenant_code=tenant.code))
        return LPN.objects.create(
            tenant=tenant,
            code=code,
            quantity=quantity,
            item=item,
            quantity_unit=quantity_unit,
        )
