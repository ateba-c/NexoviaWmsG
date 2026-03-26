from rest_framework.routers import DefaultRouter

from .views import NotificationEventViewSet

router = DefaultRouter()
router.register("events", NotificationEventViewSet, basename="notification-event")

urlpatterns = router.urls

