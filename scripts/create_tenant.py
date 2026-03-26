from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

import django

django.setup()

from apps.tenants.models import Domain, Tenant


def main() -> None:
    tenant, _ = Tenant.objects.get_or_create(
        schema_name="demo",
        defaults={"name": "Demo Tenant", "code": "DEMO"},
    )
    Domain.objects.get_or_create(domain="demo.localhost", tenant=tenant, defaults={"is_primary": True})
    print(f"Tenant ready: {tenant.schema_name}")


if __name__ == "__main__":
    main()
