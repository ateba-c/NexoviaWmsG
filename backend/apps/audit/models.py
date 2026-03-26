from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models

from shared.models import TenantAwareModel


class AuditLog(TenantAwareModel):
    action = models.CharField(max_length=64, db_index=True)
    entity_type = models.CharField(max_length=64, db_index=True)
    entity_id = models.CharField(max_length=64, db_index=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    request_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    actor_identifier = models.CharField(max_length=255, blank=True)
    payload = models.JSONField(default=dict, blank=True)
