from django.contrib import admin

from .models import Container, OrderLine, OutboundOrder, PickTask, Wave, WaveOrder

admin.site.register(OutboundOrder)
admin.site.register(OrderLine)
admin.site.register(Wave)
admin.site.register(WaveOrder)
admin.site.register(PickTask)
admin.site.register(Container)
