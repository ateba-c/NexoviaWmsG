from __future__ import annotations

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer


@shared_task
def broadcast_event(payload: dict) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "operations",
        {"type": "operations.event", "payload": payload},
    )

