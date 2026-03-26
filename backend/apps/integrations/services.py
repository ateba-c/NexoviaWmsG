from __future__ import annotations

from .models import ConnectorLog, WebhookConfig


class IntegrationService:
    def log_event(
        self,
        *,
        tenant,
        system: str,
        event_type: str,
        status: str = "PENDING",
        direction: str = "OUTBOUND",
        reference_id: str = "",
        request_payload: dict | None = None,
        response_payload: dict | None = None,
    ) -> ConnectorLog:
        return ConnectorLog.objects.create(
            tenant=tenant,
            system=system,
            event_type=event_type,
            status=status,
            direction=direction,
            reference_id=reference_id,
            request_payload=request_payload or {},
            response_payload=response_payload or {},
            payload={"event_type": event_type},
        )

    def get_active_webhooks(self, *, tenant, event_type: str):
        return WebhookConfig.objects.filter(tenant=tenant, event_type=event_type, is_active=True).order_by("name")
