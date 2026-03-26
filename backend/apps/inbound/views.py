from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.warehouse.models import Location

from .models import InboundLine, InboundOrder, ReceiveEvent
from .serializers import (
    InboundLineSerializer,
    InboundOrderSerializer,
    ReceiveEventSerializer,
    ReceiveLineSerializer,
)
from .services import ReceivingService


class InboundOrderViewSet(viewsets.ModelViewSet):
    queryset = InboundOrder.objects.all().order_by("-created_at")
    serializer_class = InboundOrderSerializer


class InboundLineViewSet(viewsets.ModelViewSet):
    queryset = InboundLine.objects.select_related("inbound_order", "item").all().order_by("line_number")
    serializer_class = InboundLineSerializer
    service = ReceivingService()

    @action(detail=True, methods=["post"], url_path="receive")
    def receive(self, request, pk=None):
        inbound_line = self.get_object()
        serializer = ReceiveLineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = Location.objects.get(pk=serializer.validated_data["location"])
        result = self.service.receive_line(
            inbound_line=inbound_line,
            quantity=serializer.validated_data["quantity"],
            location=location,
            lot_number=serializer.validated_data.get("lot_number", ""),
            expiry_date=serializer.validated_data.get("expiry_date"),
            actor=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
        )
        return Response(result, status=status.HTTP_200_OK)


class ReceiveEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReceiveEvent.objects.select_related("inbound_line", "lpn", "location").all().order_by("-created_at")
    serializer_class = ReceiveEventSerializer
