from __future__ import annotations

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from shared.models import TenantAwareModel


class Role(TenantAwareModel):
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=list, blank=True)
    is_system = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "code"], name="accounts_role_tenant_code_uniq")
        ]

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.PROTECT, related_name="users")
    preferred_language = models.CharField(max_length=10, default="en-CA")
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    display_name = models.CharField(max_length=255, blank=True)
    is_floor_user = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "username"], name="accounts_user_tenant_username_uniq")
        ]

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.get_full_name().strip() or self.username
        super().save(*args, **kwargs)
