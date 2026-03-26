from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.items.models import Item

from .models import CountResult, CountTask, CountVariance
from .serializers import (
    CountResultSerializer,
    CountTaskSerializer,
    CountVarianceSerializer,
    ExecuteCountSerializer,
)
from .services import CountingService


class CountTaskViewSet(viewsets.ModelViewSet):
    queryset = CountTask.objects.select_related("location", "assigned_to").prefetch_related("results__item").all().order_by(
        "-created_at"
    )
    serializer_class = CountTaskSerializer
    service = CountingService()

    @action(detail=True, methods=["post"], url_path="execute")
    def execute(self, request, pk=None):
        count_task = self.get_object()
        serializer = ExecuteCountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = Item.objects.get(pk=serializer.validated_data["item"])
        result = self.service.execute_count(
            count_task=count_task,
            item=item,
            counted_quantity=serializer.validated_data["counted_quantity"],
            actor=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
        )
        return Response(CountResultSerializer(result).data, status=status.HTTP_200_OK)


class CountResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CountResult.objects.select_related("count_task", "item").all().order_by("-created_at")
    serializer_class = CountResultSerializer


class CountVarianceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CountVariance.objects.select_related("count_result", "approved_by").all().order_by("-created_at")
    serializer_class = CountVarianceSerializer
    service = CountingService()

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        variance = self.get_object()
        variance = self.service.approve_variance(
            variance=variance,
            actor=request.user,
            notes=request.data.get("notes", ""),
        )
        return Response(self.get_serializer(variance).data, status=status.HTTP_200_OK)
