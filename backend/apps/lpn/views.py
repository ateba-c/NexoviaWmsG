from rest_framework import viewsets

from shared.pagination import DefaultCursorPagination

from .models import LPN
from .serializers import LPNSerializer


class LPNViewSet(viewsets.ModelViewSet):
    queryset = LPN.objects.all().order_by("-created_at")
    serializer_class = LPNSerializer
    pagination_class = DefaultCursorPagination

