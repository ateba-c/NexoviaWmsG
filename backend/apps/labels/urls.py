from rest_framework.routers import DefaultRouter

from .views import PrinterViewSet

router = DefaultRouter()
router.register("printers", PrinterViewSet, basename="printer")

urlpatterns = router.urls

