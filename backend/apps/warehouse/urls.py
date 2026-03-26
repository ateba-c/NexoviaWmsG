from rest_framework.routers import DefaultRouter

from .views import LocationViewSet, WarehouseViewSet, ZoneViewSet

router = DefaultRouter()
router.register("warehouses", WarehouseViewSet, basename="warehouse")
router.register("zones", ZoneViewSet, basename="zone")
router.register("locations", LocationViewSet, basename="location")

urlpatterns = router.urls

