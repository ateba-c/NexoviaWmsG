from django.contrib import admin

from .models import InboundLine, InboundOrder, ReceiveEvent

admin.site.register(InboundOrder)
admin.site.register(InboundLine)
admin.site.register(ReceiveEvent)
