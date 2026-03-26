from rest_framework import viewsets

from .models import ConnectorLog, EDIPartner, WebhookConfig
from .serializers import ConnectorLogSerializer, EDIPartnerSerializer, WebhookConfigSerializer


class ConnectorLogViewSet(viewsets.ModelViewSet):
    queryset = ConnectorLog.objects.all().order_by("-created_at")
    serializer_class = ConnectorLogSerializer


class WebhookConfigViewSet(viewsets.ModelViewSet):
    queryset = WebhookConfig.objects.all().order_by("name")
    serializer_class = WebhookConfigSerializer


class EDIPartnerViewSet(viewsets.ModelViewSet):
    queryset = EDIPartner.objects.all().order_by("name")
    serializer_class = EDIPartnerSerializer
