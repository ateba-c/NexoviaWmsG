from django.db import models

from shared.models import TenantAwareModel


class WebhookConfig(TenantAwareModel):
    name = models.CharField(max_length=128)
    event_type = models.CharField(max_length=64)
    target_url = models.URLField()
    is_active = models.BooleanField(default=True)
    secret = models.CharField(max_length=255, blank=True)


class ConnectorLog(TenantAwareModel):
    system = models.CharField(max_length=64)
    direction = models.CharField(max_length=20, default="OUTBOUND")
    event_type = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, default="PENDING")
    reference_id = models.CharField(max_length=64, blank=True, db_index=True)
    request_payload = models.JSONField(default=dict, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    payload = models.JSONField(default=dict, blank=True)


class EDIPartner(TenantAwareModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=32)
    protocol = models.CharField(max_length=20, default="API")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "code"], name="integrations_partner_tenant_code_uniq")
        ]
