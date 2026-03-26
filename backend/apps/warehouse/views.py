from rest_framework import viewsets

from shared.pagination import DefaultCursorPagination

from .models import Location, Warehouse, Zone
from .serializers import LocationSerializer, WarehouseSerializer, ZoneSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all().order_by("code")
    serializer_class = WarehouseSerializer
    pagination_class = DefaultCursorPagination


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.select_related("warehouse").all().order_by("code")
    serializer_class = ZoneSerializer
    pagination_class = DefaultCursorPagination


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.select_related("zone", "zone__warehouse").all().order_by("code")
    serializer_class = LocationSerializer
    pagination_class = DefaultCursorPagination

