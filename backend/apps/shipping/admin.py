from django.contrib import admin

from .models import Manifest, Shipment

admin.site.register(Shipment)
admin.site.register(Manifest)
