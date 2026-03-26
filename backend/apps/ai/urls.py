from rest_framework.routers import DefaultRouter

from .views import ConversationMessageViewSet, ConversationViewSet

router = DefaultRouter()
router.register("conversations", ConversationViewSet, basename="conversation")
router.register("messages", ConversationMessageViewSet, basename="conversation-message")

urlpatterns = router.urls
