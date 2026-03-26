from __future__ import annotations

from django.db import models
from django_tenants.models import DomainMixin, TenantMixin


class Tenant(TenantMixin):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    default_language = models.CharField(max_length=10, default="en-CA")
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    def __str__(self) -> str:
        return self.name


class Domain(DomainMixin):
    pass

