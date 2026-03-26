from rest_framework.routers import DefaultRouter

from .views import InventoryMovementViewSet, InventoryPositionViewSet

router = DefaultRouter()
router.register("positions", InventoryPositionViewSet, basename="inventory-position")
router.register("movements", InventoryMovementViewSet, basename="inventory-movement")

urlpatterns = router.urls

