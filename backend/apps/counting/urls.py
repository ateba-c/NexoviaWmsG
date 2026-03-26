from rest_framework.routers import DefaultRouter

from .views import CountResultViewSet, CountTaskViewSet, CountVarianceViewSet

router = DefaultRouter()
router.register("tasks", CountTaskViewSet, basename="count-task")
router.register("results", CountResultViewSet, basename="count-result")
router.register("variances", CountVarianceViewSet, basename="count-variance")

urlpatterns = router.urls
