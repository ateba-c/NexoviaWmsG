from rest_framework import viewsets

from .models import Printer
from .serializers import PrinterSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all().order_by("name")
    serializer_class = PrinterSerializer

