from rest_framework import serializers

from .models import ConnectorLog, EDIPartner, WebhookConfig


class ConnectorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectorLog
        fields = "__all__"


class WebhookConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookConfig
        fields = "__all__"


class EDIPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EDIPartner
        fields = "__all__"
