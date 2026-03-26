from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import KPIReport, MetricSnapshot
from .serializers import KPIReportSerializer, MetricSnapshotSerializer
from .services import AnalyticsService


class MetricSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetricSnapshot.objects.all().order_by("-captured_for")
    serializer_class = MetricSnapshotSerializer
    service = AnalyticsService()

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        tenant = getattr(request.user, "tenant", None)
        return Response(self.service.summary(tenant=tenant))

    @action(detail=False, methods=["post"], url_path="refresh")
    def refresh(self, request):
        tenant = getattr(request.user, "tenant", None)
        report = self.service.refresh_daily_report(tenant=tenant, report_date=date.today())
        return Response(KPIReportSerializer(report).data)


class KPIReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KPIReport.objects.all().order_by("-report_date")
    serializer_class = KPIReportSerializer
