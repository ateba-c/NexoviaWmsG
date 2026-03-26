from django.db import models

from shared.models import TenantAwareModel


class Printer(TenantAwareModel):
    name = models.CharField(max_length=128)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField(default=9100)

