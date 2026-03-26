from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction

from .models import Conversation, ConversationMessage


@dataclass
class CopilotReplyResult:
    conversation: Conversation
    user_message: ConversationMessage
    assistant_message: ConversationMessage


class CopilotService:
    def _get_client(self):
        api_key = getattr(settings, "OPENAI_API_KEY", "")
        if not api_key:
            raise ImproperlyConfigured("OPENAI_API_KEY is not configured.")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImproperlyConfigured("The openai package is not installed.") from exc
        return OpenAI(api_key=api_key)

    def _get_model(self) -> str:
        return getattr(settings, "OPENAI_MODEL", "gpt-5")

    def _get_instructions(self) -> str:
        return getattr(
            settings,
            "OPENAI_SYSTEM_PROMPT",
            (
                "You are the NexoFlow warehouse copilot. Give concise operational guidance for warehouse staff, "
                "inventory control, inbound, outbound, counting, shipping, and tenant-safe workflows."
            ),
        )

    def _extract_text(self, response) -> str:
        output_text = getattr(response, "output_text", "")
        if output_text:
            return output_text.strip()
        return ""

    @transaction.atomic
    def reply(
        self,
        *,
        conversation: Conversation,
        user_message: str,
        actor=None,
    ) -> CopilotReplyResult:
        user_record = ConversationMessage.objects.create(
            tenant=conversation.tenant,
            conversation=conversation,
            role=ConversationMessage.ROLE_USER,
            content=user_message,
            metadata={"actor_id": str(getattr(actor, "id", ""))},
        )

        client = self._get_client()
        request_kwargs = {
            "model": self._get_model(),
            "instructions": self._get_instructions(),
            "input": user_message,
            "store": True,
        }
        if conversation.last_response_id:
            request_kwargs["previous_response_id"] = conversation.last_response_id

        response = client.responses.create(**request_kwargs)
        assistant_text = self._extract_text(response) or "No response text returned."

        conversation.model = self._get_model()
        conversation.last_response_id = getattr(response, "id", "") or ""
        if not conversation.title:
            conversation.title = user_message[:80]
        conversation.save(update_fields=["model", "last_response_id", "title", "updated_at"])

        assistant_record = ConversationMessage.objects.create(
            tenant=conversation.tenant,
            conversation=conversation,
            role=ConversationMessage.ROLE_ASSISTANT,
            content=assistant_text,
            response_id=getattr(response, "id", "") or "",
            metadata={"model": conversation.model},
        )

        return CopilotReplyResult(
            conversation=conversation,
            user_message=user_record,
            assistant_message=assistant_record,
        )
