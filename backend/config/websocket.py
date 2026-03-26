from django.urls import path

from apps.notifications.consumers import OperationsConsumer

websocket_urlpatterns = [
    path("ws/operations/", OperationsConsumer.as_asgi(), name="operations"),
]

