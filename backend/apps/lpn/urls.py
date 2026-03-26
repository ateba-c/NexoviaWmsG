from rest_framework.routers import DefaultRouter

from .views import LPNViewSet

router = DefaultRouter()
router.register("", LPNViewSet, basename="lpn")

urlpatterns = router.urls
