from django.contrib import admin

from .models import Disposition, ReturnLine, ReturnOrder

admin.site.register(ReturnOrder)
admin.site.register(ReturnLine)
admin.site.register(Disposition)
