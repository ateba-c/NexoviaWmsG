from rest_framework.routers import DefaultRouter

from .views import KPIReportViewSet, MetricSnapshotViewSet

router = DefaultRouter()
router.register("metrics", MetricSnapshotViewSet, basename="metric-snapshot")
router.register("reports", KPIReportViewSet, basename="kpi-report")

urlpatterns = router.urls
