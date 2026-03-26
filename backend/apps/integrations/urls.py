from rest_framework.routers import DefaultRouter

from .views import ConnectorLogViewSet, EDIPartnerViewSet, WebhookConfigViewSet

router = DefaultRouter()
router.register("logs", ConnectorLogViewSet, basename="connector-log")
router.register("webhooks", WebhookConfigViewSet, basename="webhook-config")
router.register("partners", EDIPartnerViewSet, basename="edi-partner")

urlpatterns = router.urls
