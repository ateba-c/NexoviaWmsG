from rest_framework.routers import DefaultRouter

from .views import ManifestViewSet, ShipmentViewSet

router = DefaultRouter()
router.register("shipments", ShipmentViewSet, basename="shipment")
router.register("manifests", ManifestViewSet, basename="manifest")

urlpatterns = router.urls
