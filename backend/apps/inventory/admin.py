from django.contrib import admin

from .models import InventoryMovement, InventoryPosition

admin.site.register(InventoryPosition)
admin.site.register(InventoryMovement)

