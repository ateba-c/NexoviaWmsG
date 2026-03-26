from __future__ import annotations

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def queue_print(self, *, lpn_id: str, label_type: str, printer_id: str | None = None) -> None:
    logger.info(
        "Queueing label print",
        extra={"lpn_id": lpn_id, "label_type": label_type, "printer_id": printer_id},
    )

