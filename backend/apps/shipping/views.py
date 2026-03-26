from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Manifest, Shipment
from .serializers import ManifestSerializer, ShipmentMarkShippedSerializer, ShipmentSerializer
from .services import ShippingService


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all().order_by("-created_at")
    serializer_class = ShipmentSerializer
    service = ShippingService()

    @action(detail=True, methods=["post"], url_path="mark-shipped")
    def mark_shipped(self, request, pk=None):
        shipment = self.get_object()
        serializer = ShipmentMarkShippedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shipment = self.service.mark_shipped(
            shipment=shipment,
            tracking_number=serializer.validated_data.get("tracking_number", ""),
            actor=request.user,
        )
        return Response(self.get_serializer(shipment).data, status=status.HTTP_200_OK)


class ManifestViewSet(viewsets.ModelViewSet):
    queryset = Manifest.objects.prefetch_related("shipments").all().order_by("-created_at")
    serializer_class = ManifestSerializer
