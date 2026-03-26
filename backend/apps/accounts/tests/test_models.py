from django.test import TestCase

from apps.accounts.models import Role, User
from apps.tenants.models import Tenant


class UserModelTests(TestCase):
    def test_display_name_defaults_from_username(self):
        tenant = Tenant.objects.create(schema_name="tenant_one", name="Tenant One", code="T1")
        role = Role.objects.create(tenant=tenant, code="associate", name="Associate")
        user = User.objects.create_user(
            username="picker1",
            password="secret123",
            tenant=tenant,
            role=role,
        )
        self.assertEqual(user.display_name, "picker1")

