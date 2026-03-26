from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Disposition, ReturnLine, ReturnOrder
from .serializers import DispositionSerializer, ReturnLineSerializer, ReturnOrderSerializer
from .services import ReturnsService


class ReturnOrderViewSet(viewsets.ModelViewSet):
    queryset = ReturnOrder.objects.all().order_by("-created_at")
    serializer_class = ReturnOrderSerializer


class ReturnLineViewSet(viewsets.ModelViewSet):
    queryset = ReturnLine.objects.select_related("return_order", "item").all().order_by("line_number")
    serializer_class = ReturnLineSerializer


class DispositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Disposition.objects.select_related("return_line", "inventory_position").all().order_by("-created_at")
    serializer_class = DispositionSerializer
    service = ReturnsService()

    @action(detail=False, methods=["post"], url_path="dispose")
    def dispose(self, request):
        return_line = ReturnLine.objects.get(pk=request.data["return_line"])
        disposition = self.service.dispose_return_line(
            return_line=return_line,
            action=request.data["action"],
            quantity=int(request.data.get("quantity", 1)),
            notes=request.data.get("notes", ""),
            actor=request.user,
        )
        return Response(DispositionSerializer(disposition).data, status=status.HTTP_201_CREATED)
