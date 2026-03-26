from django.contrib import admin

from .models import ConnectorLog, EDIPartner, WebhookConfig

admin.site.register(ConnectorLog)
admin.site.register(WebhookConfig)
admin.site.register(EDIPartner)
