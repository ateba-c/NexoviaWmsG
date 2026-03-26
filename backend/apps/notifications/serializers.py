from rest_framework import serializers

from .models import NotificationEvent


class NotificationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationEvent
        fields = "__all__"

