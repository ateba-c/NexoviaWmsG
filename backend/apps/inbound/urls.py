from rest_framework.routers import DefaultRouter

from .views import InboundLineViewSet, InboundOrderViewSet, ReceiveEventViewSet

router = DefaultRouter()
router.register("orders", InboundOrderViewSet, basename="inbound-order")
router.register("lines", InboundLineViewSet, basename="inbound-line")
router.register("events", ReceiveEventViewSet, basename="receive-event")

urlpatterns = router.urls
