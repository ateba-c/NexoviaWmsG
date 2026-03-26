from rest_framework import viewsets

from shared.pagination import DefaultCursorPagination

from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by("sku")
    serializer_class = ItemSerializer
    pagination_class = DefaultCursorPagination
    search_fields = ("sku", "gtin", "description_en", "description_fr")

