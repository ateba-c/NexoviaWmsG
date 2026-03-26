from django.db import models

from shared.models import TenantAwareModel


class Conversation(TenantAwareModel):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="OPEN")
    model = models.CharField(max_length=100, blank=True)
    last_response_id = models.CharField(max_length=255, blank=True)


class ConversationMessage(TenantAwareModel):
    ROLE_USER = "USER"
    ROLE_ASSISTANT = "ASSISTANT"
    ROLE_SYSTEM = "SYSTEM"

    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ASSISTANT, "Assistant"),
        (ROLE_SYSTEM, "System"),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    response_id = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
