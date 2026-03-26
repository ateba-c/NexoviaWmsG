from rest_framework.routers import DefaultRouter

from .views import DispositionViewSet, ReturnLineViewSet, ReturnOrderViewSet

router = DefaultRouter()
router.register("orders", ReturnOrderViewSet, basename="return-order")
router.register("lines", ReturnLineViewSet, basename="return-line")
router.register("dispositions", DispositionViewSet, basename="disposition")

urlpatterns = router.urls
