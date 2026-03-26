from django.contrib import admin

from .models import Location, Warehouse, Zone

admin.site.register(Warehouse)
admin.site.register(Zone)
admin.site.register(Location)

