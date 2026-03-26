from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_: object) -> JsonResponse:
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/inbound/", include("apps.inbound.urls")),
    path("api/v1/inventory/", include("apps.inventory.urls")),
    path("api/v1/outbound/", include("apps.outbound.urls")),
    path("api/v1/shipping/", include("apps.shipping.urls")),
    path("api/v1/returns/", include("apps.returns.urls")),
    path("api/v1/counting/", include("apps.counting.urls")),
    path("api/v1/warehouse/", include("apps.warehouse.urls")),
    path("api/v1/items/", include("apps.items.urls")),
    path("api/v1/lpns/", include("apps.lpn.urls")),
    path("api/v1/labels/", include("apps.labels.urls")),
    path("api/v1/integrations/", include("apps.integrations.urls")),
    path("api/v1/analytics/", include("apps.analytics.urls")),
    path("api/v1/ai/", include("apps.ai.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/audit/", include("apps.audit.urls")),
]
