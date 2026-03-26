from rest_framework import serializers

from .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = "__all__"

    def get_message_count(self, obj: Conversation) -> int:
        return obj.messages.count()


class ConversationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMessage
        fields = "__all__"


class ConversationReplySerializer(serializers.Serializer):
    user_message = serializers.CharField()


class CopilotReplyResultSerializer(serializers.Serializer):
    conversation = ConversationSerializer()
    user_message = ConversationMessageSerializer()
    assistant_message = ConversationMessageSerializer()
