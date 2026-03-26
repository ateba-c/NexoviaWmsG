from rest_framework.routers import DefaultRouter

from .views import ContainerViewSet, OrderLineViewSet, OutboundOrderViewSet, PickTaskViewSet, WaveViewSet

router = DefaultRouter()
router.register("orders", OutboundOrderViewSet, basename="outbound-order")
router.register("lines", OrderLineViewSet, basename="order-line")
router.register("waves", WaveViewSet, basename="wave")
router.register("pick-tasks", PickTaskViewSet, basename="pick-task")
router.register("containers", ContainerViewSet, basename="container")

urlpatterns = router.urls
