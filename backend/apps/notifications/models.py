from django.db import models

from shared.models import TenantAwareModel


class NotificationEvent(TenantAwareModel):
    event_type = models.CharField(max_length=64)
    payload = models.JSONField(default=dict, blank=True)

