from django.core.exceptions import ImproperlyConfigured
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Conversation, ConversationMessage
from .serializers import (
    ConversationMessageSerializer,
    ConversationReplySerializer,
    ConversationSerializer,
)
from .services import CopilotService


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.prefetch_related("messages").all().order_by("-created_at")
    serializer_class = ConversationSerializer
    service = CopilotService()

    @action(detail=True, methods=["post"], url_path="reply")
    def reply(self, request, pk=None):
        conversation = self.get_object()
        serializer = ConversationReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = self.service.reply(
                conversation=conversation,
                user_message=serializer.validated_data["user_message"],
                actor=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
            )
        except ImproperlyConfigured as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(
            {
                "conversation": ConversationSerializer(result.conversation).data,
                "user_message": ConversationMessageSerializer(result.user_message).data,
                "assistant_message": ConversationMessageSerializer(result.assistant_message).data,
            },
            status=status.HTTP_200_OK,
        )


class ConversationMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConversationMessage.objects.select_related("conversation").all().order_by("created_at")
    serializer_class = ConversationMessageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset
