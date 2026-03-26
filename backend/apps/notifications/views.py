from rest_framework import viewsets

from .models import NotificationEvent
from .serializers import NotificationEventSerializer


class NotificationEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationEvent.objects.all().order_by("-created_at")
    serializer_class = NotificationEventSerializer

