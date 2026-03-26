from __future__ import annotations

from apps.audit.middleware import get_current_request

from .models import AuditLog


class AuditService:
    def log(
        self,
        *,
        tenant,
        action: str,
        entity_type: str,
        entity_id: str,
        actor=None,
        payload: dict | None = None,
    ) -> AuditLog:
        request = get_current_request()
        actor_identifier = ""
        if actor is not None:
            actor_identifier = getattr(actor, "username", "") or str(actor.pk)
        elif request is not None and getattr(request, "user", None) and request.user.is_authenticated:
            actor = request.user
            actor_identifier = request.user.username

        return AuditLog.objects.create(
            tenant=tenant,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            actor=actor,
            actor_identifier=actor_identifier,
            payload=payload or {},
        )
