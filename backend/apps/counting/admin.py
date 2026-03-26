from django.contrib import admin

from .models import CountResult, CountTask, CountVariance

admin.site.register(CountTask)
admin.site.register(CountResult)
admin.site.register(CountVariance)
