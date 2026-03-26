from __future__ import annotations

import uuid

from django.db import models


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TenantAwareModel(TimeStampedModel):
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True


class CodeNameMixin(models.Model):
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True
