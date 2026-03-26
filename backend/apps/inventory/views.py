from rest_framework import viewsets

from .models import InventoryMovement, InventoryPosition
from .serializers import InventoryMovementSerializer, InventoryPositionSerializer


class InventoryPositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        InventoryPosition.objects.select_related("tenant", "lpn", "item", "location")
        .all()
        .order_by("-created_at")
    )
    serializer_class = InventoryPositionSerializer


class InventoryMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        InventoryMovement.objects.select_related("tenant", "position", "lpn", "item")
        .all()
        .order_by("-created_at")
    )
    serializer_class = InventoryMovementSerializer

