from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Container, OrderLine, OutboundOrder, PickTask, Wave
from .serializers import (
    ContainerSerializer,
    OrderLineSerializer,
    OutboundOrderSerializer,
    PickTaskConfirmSerializer,
    PickTaskSerializer,
    WaveSerializer,
)
from .services import PickTaskService, WaveService


class OutboundOrderViewSet(viewsets.ModelViewSet):
    queryset = OutboundOrder.objects.all().order_by("-created_at")
    serializer_class = OutboundOrderSerializer


class OrderLineViewSet(viewsets.ModelViewSet):
    queryset = OrderLine.objects.select_related("outbound_order", "item").all().order_by("line_number")
    serializer_class = OrderLineSerializer


class WaveViewSet(viewsets.ModelViewSet):
    queryset = Wave.objects.all().order_by("-created_at")
    serializer_class = WaveSerializer
    service = WaveService()

    @action(detail=True, methods=["post"], url_path="release")
    def release(self, request, pk=None):
        wave = self.get_object()
        wave = self.service.release_wave(wave=wave)
        return Response(self.get_serializer(wave).data)


class PickTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        PickTask.objects.select_related(
            "wave",
            "order_line",
            "order_line__item",
            "inventory_position",
            "inventory_position__location",
            "assigned_to",
        )
        .all()
        .order_by("sequence", "created_at")
    )
    serializer_class = PickTaskSerializer
    service = PickTaskService()

    @action(detail=True, methods=["post"], url_path="start")
    def start(self, request, pk=None):
        task = self.get_object()
        task = self.service.start_task(task=task, user=request.user)
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"], url_path="confirm")
    def confirm(self, request, pk=None):
        task = self.get_object()
        serializer = PickTaskConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = self.service.confirm_pick(task=task, quantity=serializer.validated_data["quantity"])
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.select_related("outbound_order").all().order_by("-created_at")
    serializer_class = ContainerSerializer
