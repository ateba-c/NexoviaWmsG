# NexoFlow WMS — Technical Design Document (TDD)

> **Audience:** Backend engineers, DevOps, integration architects, Claude Code  
> **Stack:** Django 5.x · PostgreSQL 16 · React 18 · Celery · Redis · Elasticsearch  
> **Revision:** 1.0

---

## Table of Contents

1. [Repository Structure](#1-repository-structure)
2. [Backend Architecture](#2-backend-architecture)
3. [Database Design](#3-database-design)
4. [Multi-Tenancy Implementation](#4-multi-tenancy-implementation)
5. [Authentication & Authorization](#5-authentication--authorization)
6. [Django Apps & Responsibilities](#6-django-apps--responsibilities)
7. [REST API Conventions](#7-rest-api-conventions)
8. [Celery Task Architecture](#8-celery-task-architecture)
9. [Real-Time with Django Channels](#9-real-time-with-django-channels)
10. [LPN Generation Engine](#10-lpn-generation-engine)
11. [ZPL Label Engine](#11-zpl-label-engine)
12. [Inventory Engine](#12-inventory-engine)
13. [Picking Engine](#13-picking-engine)
14. [Wave Planning Engine](#14-wave-planning-engine)
15. [EDI Adapter](#15-edi-adapter)
16. [Carrier Integration](#16-carrier-integration)
17. [AI Co-Pilot Architecture](#17-ai-co-pilot-architecture)
18. [Frontend Architecture](#18-frontend-architecture)
19. [PWA & Offline Strategy](#19-pwa--offline-strategy)
20. [i18n Architecture](#20-i18n-architecture)
21. [Search & Elasticsearch](#21-search--elasticsearch)
22. [Infrastructure & DevOps](#22-infrastructure--devops)
23. [Testing Strategy](#23-testing-strategy)
24. [Security Implementation](#24-security-implementation)
25. [Performance Targets & SLAs](#25-performance-targets--slas)
26. [Environment Configuration](#26-environment-configuration)
27. [Migration Strategy](#27-migration-strategy)

---

## 1. Repository Structure

```
nexoflow/
├── backend/                          # Django project root
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py               # Shared settings
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   │   └── test.py
│   │   ├── urls.py                   # Root URL config
│   │   ├── asgi.py                   # Channels entrypoint
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── tenants/                  # Tenant management (django-tenants)
│   │   ├── accounts/                 # Users, roles, permissions
│   │   ├── warehouse/                # Warehouse, zones, locations
│   │   ├── items/                    # Item master, UOM, attributes
│   │   ├── inventory/                # Inventory positions, movements
│   │   ├── inbound/                  # Receiving, ASN, PO management
│   │   ├── outbound/                 # Orders, waves, picks, packing
│   │   ├── shipping/                 # Shipments, carriers, manifests
│   │   ├── returns/                  # RMAs, grading, disposition
│   │   ├── counting/                 # Cycle counts, periodic counts
│   │   ├── lpn/                      # LPN generation and lifecycle
│   │   ├── labels/                   # ZPL template engine
│   │   ├── integrations/             # EDI, ERP, carrier connectors
│   │   ├── analytics/                # Aggregation, reporting queries
│   │   ├── ai/                       # AI Co-Pilot, forecasting
│   │   ├── notifications/            # Alerts, emails, push
│   │   └── audit/                    # Immutable audit log
│   ├── shared/
│   │   ├── models.py                 # TenantAwareModel, TimeStampedModel
│   │   ├── permissions.py            # Custom DRF permission classes
│   │   ├── pagination.py             # Cursor + page pagination
│   │   ├── filters.py                # django-filter base classes
│   │   ├── exceptions.py             # Custom API exception handlers
│   │   ├── validators.py             # GS1, barcode, lot format validators
│   │   └── utils/
│   │       ├── barcode.py
│   │       ├── gs1.py
│   │       └── dates.py
│   ├── locale/
│   │   ├── en_CA/LC_MESSAGES/django.po
│   │   └── fr_CA/LC_MESSAGES/django.po
│   ├── manage.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   └── pyproject.toml
│
├── frontend/                         # React PWA
│   ├── src/
│   │   ├── app/                      # App shell, routing, providers
│   │   ├── features/                 # Feature-sliced architecture
│   │   │   ├── receiving/
│   │   │   ├── stowing/
│   │   │   ├── picking/
│   │   │   ├── packing/
│   │   │   ├── shipping/
│   │   │   ├── returns/
│   │   │   ├── inventory/
│   │   │   ├── counting/
│   │   │   ├── analytics/
│   │   │   └── ai/
│   │   ├── components/ui/            # Design system components
│   │   ├── hooks/                    # Shared custom hooks
│   │   ├── stores/                   # Zustand stores
│   │   ├── api/                      # React Query + API client
│   │   ├── locales/                  # i18n JSON files
│   │   │   ├── en-CA/
│   │   │   └── fr-CA/
│   │   ├── utils/
│   │   └── types/                    # Shared TypeScript types
│   ├── public/
│   │   ├── manifest.json             # PWA manifest
│   │   └── service-worker.ts         # Workbox SW
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   └── capacitor.config.ts
│
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── docker-compose.yml        # Local dev full stack
│   ├── k8s/
│   │   ├── base/                     # Kustomize base
│   │   └── overlays/
│   │       ├── staging/
│   │       └── production/
│   └── helm/
│       └── nexoflow/                 # Helm chart
│
├── scripts/
│   ├── seed_tenant.py                # Seed a new tenant with demo data
│   ├── create_tenant.py              # Provision tenant schema
│   └── export_tokens.ts              # Design token export
│
└── docs/
    ├── DESIGN.md                     # ← This file's companion
    ├── TDD.md                        # ← This file
    ├── api/                          # OpenAPI specs
    └── adr/                          # Architecture Decision Records
```

---

## 2. Backend Architecture

### Core Dependencies

```txt
# requirements/base.txt
Django==5.1.*
djangorestframework==3.15.*
django-tenants==3.7.*              # Schema-per-tenant multi-tenancy
djangorestframework-simplejwt==5.* # JWT auth
django-cors-headers==4.*
django-filter==24.*
django-channels==4.*               # WebSocket support
channels-redis==4.*                # Channel layer backend
celery==5.4.*
redis==5.*
psycopg[binary]==3.*               # PostgreSQL adapter (psycopg3)
django-storages[s3]==1.14.*        # S3 file storage
elasticsearch-dsl==8.*             # Elasticsearch client
Pillow==10.*                       # Image processing (label preview)
python-barcode==0.15.*             # Barcode generation
qrcode==7.*
reportlab==4.*                     # PDF generation (manifests)
boto3==1.34.*                      # AWS SDK
pydantic==2.*                      # Data validation for integrations
httpx==0.27.*                      # Async HTTP client for integrations
tenacity==8.*                      # Retry logic for external calls
sentry-sdk==2.*
django-health-check==3.*
drf-spectacular==0.27.*            # OpenAPI 3 schema generation
```

### Request Lifecycle

```
HTTP Request
  → Nginx (TLS termination, rate limiting)
  → Gunicorn (WSGI workers, 4 per CPU core)
  → Django Middleware Stack:
      1. SecurityMiddleware
      2. TenantMiddleware          ← resolves tenant from subdomain
      3. SessionMiddleware
      4. CorsMiddleware
      5. LocaleMiddleware          ← sets language from Accept-Language
      6. AuthenticationMiddleware
      7. AuditMiddleware           ← injects request context for audit log
  → URL Router
  → DRF View (ViewSet)
      → Permission Check
      → Throttle Check
      → Serializer Validation
      → Business Logic (service layer)
      → Serializer Output
  → JSON Response
  → AuditMiddleware (post-response hook writes audit entry async)
```

### Service Layer Pattern

Business logic lives in **service modules**, not in views or models. Views are thin — they validate input and delegate to services. Models are thin — they define structure and basic constraints.

```python
# apps/inbound/services/receiving_service.py

from typing import Optional
from django.db import transaction
from apps.inbound.models import InboundLine, ReceiveEvent
from apps.inventory.services.inventory_service import InventoryService
from apps.lpn.services import LPNService
from apps.labels.services import LabelService
from apps.audit.services import AuditService


class ReceivingService:
    """
    Orchestrates the receive transaction:
    1. Validates receive line against PO
    2. Creates inventory position
    3. Generates LPN
    4. Queues label print
    5. Writes audit entry
    6. Fires webhook if configured
    """

    def __init__(
        self,
        inventory_service: InventoryService,
        lpn_service: LPNService,
        label_service: LabelService,
        audit_service: AuditService,
    ):
        self.inventory = inventory_service
        self.lpn = lpn_service
        self.labels = label_service
        self.audit = audit_service

    @transaction.atomic
    def receive_line(
        self,
        inbound_line: InboundLine,
        quantity: int,
        lot_number: Optional[str],
        expiry_date: Optional[str],
        operator_id: int,
        device_id: str,
    ) -> dict:
        # 1. Validate
        self._validate_receive(inbound_line, quantity)

        # 2. Generate LPN
        lpn = self.lpn.generate(
            tenant=inbound_line.tenant,
            item=inbound_line.item,
            quantity=quantity,
        )

        # 3. Create inventory position (status=RECEIVING, no location yet)
        position = self.inventory.create_position(
            lpn=lpn,
            item=inbound_line.item,
            quantity=quantity,
            lot_number=lot_number,
            expiry_date=expiry_date,
            status="RECEIVING",
        )

        # 4. Record receive event
        event = ReceiveEvent.objects.create(
            inbound_line=inbound_line,
            lpn=lpn,
            quantity_received=quantity,
            operator_id=operator_id,
        )

        # 5. Update PO line received quantity
        inbound_line.qty_received = (inbound_line.qty_received or 0) + quantity
        inbound_line.save(update_fields=["qty_received", "updated_at"])

        # 6. Queue label print (async via Celery)
        self.labels.queue_print.delay(
            lpn_id=str(lpn.id),
            label_type="ITEM_RECEIVE",
            printer_id=self._resolve_printer(device_id),
        )

        # 7. Audit
        self.audit.log(
            action="RECEIVE_LINE",
            entity_type="InboundLine",
            entity_id=str(inbound_line.id),
            operator_id=operator_id,
            payload={
                "lpn": str(lpn.id),
                "quantity": quantity,
                "lot": lot_number,
                "expiry": expiry_date,
            },
        )

        return {"lpn": str(lpn.id), "position_id": str(position.id)}
```

---

## 3. Database Design

### Core Model Conventions

All models inherit from `TenantAwareModel` (which inherits `TimeStampedModel`):

```python
# shared/models.py

import uuid
from django.db import models


class TimeStampedModel(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TenantAwareModel(TimeStampedModel):
    """
    All operational models inherit this.
    django-tenants handles schema isolation, so 'tenant' FK is
    implicitly the current schema — we still store it explicitly
    for cross-schema admin queries and audit.
    """
    class Meta:
        abstract = True
```

### Key Table Definitions

```python
# apps/warehouse/models.py

class Warehouse(TenantAwareModel):
    name        = models.CharField(max_length=200)
    code        = models.CharField(max_length=20, unique=True)
    address     = models.JSONField(default=dict)         # structured address
    timezone    = models.CharField(max_length=50, default='America/Toronto')
    is_active   = models.BooleanField(default=True)

    class Meta:
        db_table = 'warehouse'


class Zone(TenantAwareModel):
    warehouse       = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='zones')
    code            = models.CharField(max_length=20)
    name            = models.CharField(max_length=100)
    zone_type       = models.CharField(max_length=30, choices=ZONE_TYPE_CHOICES)
    temp_controlled = models.BooleanField(default=False)
    temp_min_c      = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temp_max_c      = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'zone'
        unique_together = [('warehouse', 'code')]


LOCATION_TYPES = [
    ('PICK_FACE', 'Pick Face'),
    ('RESERVE',   'Reserve'),
    ('STAGING',   'Staging'),
    ('DOCK',      'Dock'),
    ('PACK',      'Pack Station'),
    ('QC',        'Quality Control'),
    ('VIRTUAL',   'Virtual'),
]

STORAGE_STRATEGIES = [
    ('DEDICATED',   'Dedicated — fixed SKU assignment'),
    ('FLOATING',    'Floating — any SKU'),
    ('ZONE',        'Zone — SKU class restricted'),
    ('MULTI_SKU',   'Multi-SKU — multiple SKUs allowed'),
]

class Location(TenantAwareModel):
    zone            = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name='locations')
    code            = models.CharField(max_length=50)        # e.g. A-07-B-03
    aisle           = models.CharField(max_length=10, db_index=True)
    bay             = models.CharField(max_length=10)
    level           = models.CharField(max_length=10)
    position        = models.CharField(max_length=10)
    location_type   = models.CharField(max_length=20, choices=LOCATION_TYPES, default='PICK_FACE')
    storage_strategy= models.CharField(max_length=20, choices=STORAGE_STRATEGIES, default='FLOATING')
    max_weight_kg   = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    max_volume_m3   = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    max_units       = models.IntegerField(null=True, blank=True)
    length_cm       = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    width_cm        = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    height_cm       = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    is_active       = models.BooleanField(default=True)
    requires_lift   = models.BooleanField(default=False)
    sort_sequence   = models.IntegerField(default=0, db_index=True)  # pick path order

    class Meta:
        db_table = 'location'
        unique_together = [('zone', 'code')]
        indexes = [
            models.Index(fields=['zone', 'location_type', 'is_active']),
        ]
```

```python
# apps/items/models.py

class Item(TenantAwareModel):
    sku             = models.CharField(max_length=100, db_index=True)
    gtin            = models.CharField(max_length=14, blank=True, db_index=True)
    upc             = models.CharField(max_length=12, blank=True)
    description_en  = models.CharField(max_length=300)
    description_fr  = models.CharField(max_length=300, blank=True)
    unit_of_measure = models.CharField(max_length=20, default='EA')
    # UOM hierarchy for cartonization
    units_per_inner = models.IntegerField(default=1)
    units_per_case  = models.IntegerField(default=1)
    cases_per_pallet= models.IntegerField(default=1)
    # Physical
    weight_kg       = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    length_cm       = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    width_cm        = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    height_cm       = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    # Controls
    lot_controlled  = models.BooleanField(default=False)
    expiry_tracked  = models.BooleanField(default=False)
    serial_tracked  = models.BooleanField(default=False)
    catch_weight    = models.BooleanField(default=False)
    min_shelf_life_days = models.IntegerField(null=True, blank=True)
    # Storage rules
    storage_temp    = models.CharField(max_length=20, choices=TEMP_CHOICES, default='AMBIENT')
    hazmat          = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)

    class Meta:
        db_table = 'item'
        unique_together = [('sku',)]   # unique within tenant schema
```

```python
# apps/inventory/models.py

INVENTORY_STATUSES = [
    ('AVAILABLE',    'Available'),
    ('ALLOCATED',    'Allocated'),
    ('ON_HOLD',      'On Hold'),
    ('QUARANTINE',   'Quarantine'),
    ('DAMAGED',      'Damaged'),
    ('EXPIRED',      'Expired'),
    ('IN_TRANSIT',   'In Transit'),
    ('RECEIVING',    'Receiving'),
    ('COUNTING',     'Cycle Count Hold'),
]

class InventoryPosition(TenantAwareModel):
    """
    The core inventory record.
    One row per (LPN, item, lot, location, status) combination.
    Quantity changes via InventoryMovement — never direct update.
    """
    lpn             = models.ForeignKey('lpn.LPN', on_delete=models.PROTECT, related_name='positions')
    item            = models.ForeignKey('items.Item', on_delete=models.PROTECT)
    location        = models.ForeignKey('warehouse.Location', on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='positions')
    lot_number      = models.CharField(max_length=100, blank=True, db_index=True)
    serial_number   = models.CharField(max_length=100, blank=True, db_index=True)
    expiry_date     = models.DateField(null=True, blank=True, db_index=True)
    manufacture_date= models.DateField(null=True, blank=True)
    quantity_on_hand= models.DecimalField(max_digits=12, decimal_places=4, default=0)
    quantity_allocated = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    status          = models.CharField(max_length=20, choices=INVENTORY_STATUSES, default='AVAILABLE', db_index=True)
    catch_weight_kg = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    received_at     = models.DateTimeField(null=True, blank=True)
    received_by_id  = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = 'inventory_position'
        indexes = [
            models.Index(fields=['item', 'status', 'expiry_date']),     # FEFO queries
            models.Index(fields=['location', 'status']),                # Location queries
            models.Index(fields=['lot_number', 'item']),                # Lot traceability
        ]

    @property
    def quantity_available(self):
        return self.quantity_on_hand - self.quantity_allocated


class InventoryMovement(TenantAwareModel):
    """
    Immutable event log of every inventory change.
    Source of truth for audit and reporting.
    """
    MOVEMENT_TYPES = [
        ('RECEIVE',     'Receive'),
        ('STOW',        'Stow'),
        ('PICK',        'Pick'),
        ('PACK',        'Pack'),
        ('SHIP',        'Ship'),
        ('RETURN',      'Return'),
        ('ADJUSTMENT',  'Manual Adjustment'),
        ('COUNT_ADJ',   'Count Adjustment'),
        ('TRANSFER',    'Transfer'),
        ('DISPOSE',     'Disposition'),
        ('ALLOCATE',    'Allocate'),
        ('DEALLOCATE',  'Deallocate'),
    ]

    position        = models.ForeignKey(InventoryPosition, on_delete=models.PROTECT, related_name='movements')
    movement_type   = models.CharField(max_length=20, choices=MOVEMENT_TYPES, db_index=True)
    quantity_delta  = models.DecimalField(max_digits=12, decimal_places=4)
    quantity_before = models.DecimalField(max_digits=12, decimal_places=4)
    quantity_after  = models.DecimalField(max_digits=12, decimal_places=4)
    from_location   = models.ForeignKey('warehouse.Location', on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='+')
    to_location     = models.ForeignKey('warehouse.Location', on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='+')
    reference_type  = models.CharField(max_length=50, blank=True)   # 'PickTask', 'InboundLine', etc.
    reference_id    = models.UUIDField(null=True, blank=True)
    operator_id     = models.UUIDField(db_index=True)
    device_id       = models.CharField(max_length=100, blank=True)
    notes           = models.TextField(blank=True)

    class Meta:
        db_table = 'inventory_movement'
        indexes = [
            models.Index(fields=['position', 'created_at']),
            models.Index(fields=['movement_type', 'created_at']),
            models.Index(fields=['reference_type', 'reference_id']),
        ]
```

### Critical Database Rules

1. **Never update `quantity_on_hand` directly.** Always go through `InventoryService.apply_movement()` which creates the `InventoryMovement` record atomically.
2. **`InventoryMovement` is append-only.** No updates, no deletes.
3. **AuditLog is append-only.** No updates, no deletes. Enforce via database trigger.
4. **Use `SELECT FOR UPDATE` on `InventoryPosition`** when applying movements to prevent race conditions.
5. **All financial/quantity fields use `DecimalField`**, never `FloatField`.

### Database Indexes (Beyond Model Definitions)

```sql
-- Inbound: find open PO lines needing receipt
CREATE INDEX idx_inbound_open_lines
  ON inbound_line(inbound_order_id, status)
  WHERE status IN ('PENDING', 'PARTIAL');

-- Outbound: allocatable inventory (FEFO order)
CREATE INDEX idx_inventory_allocatable
  ON inventory_position(item_id, status, expiry_date NULLS LAST, received_at)
  WHERE status = 'AVAILABLE' AND quantity_on_hand > quantity_allocated;

-- Picking: open pick tasks by wave
CREATE INDEX idx_pick_task_wave_open
  ON pick_task(wave_id, status, sort_sequence)
  WHERE status IN ('PENDING', 'IN_PROGRESS');

-- Expiry alert queries
CREATE INDEX idx_position_expiry
  ON inventory_position(expiry_date, status)
  WHERE expiry_date IS NOT NULL;
```

---

## 4. Multi-Tenancy Implementation

### Schema Strategy (django-tenants)

Each tenant gets an isolated PostgreSQL schema. The `public` schema holds only the `Client` (Tenant) model and the `Domain` model. All operational data is in `{tenant_schema}.*`.

```python
# apps/tenants/models.py

from django_tenants.models import TenantMixin, DomainMixin
from django.db import models


class Tenant(TenantMixin):
    name             = models.CharField(max_length=200)
    slug             = models.SlugField(unique=True)
    language         = models.CharField(max_length=10, default='en-CA',
                                         choices=[('en-CA', 'English'), ('fr-CA', 'Français')])
    timezone         = models.CharField(max_length=50, default='America/Toronto')
    is_active        = models.BooleanField(default=True)
    subscription_tier = models.CharField(max_length=20, default='STANDARD',
                                          choices=[('STANDARD','Standard'),('PROFESSIONAL','Professional'),('ENTERPRISE','Enterprise')])
    feature_flags    = models.JSONField(default=dict)         # {module: bool}
    created_at       = models.DateTimeField(auto_now_add=True)

    auto_create_schema = True
    auto_drop_schema   = False   # Never auto-drop — require explicit admin action

    class Meta:
        app_label = 'tenants'


class Domain(DomainMixin):
    class Meta:
        app_label = 'tenants'
```

### Tenant Provisioning Script

```python
# scripts/create_tenant.py
"""
Usage: python manage.py create_tenant --name="Acme Corp" --slug="acme" --lang="fr-CA"
"""

from django_tenants.utils import schema_context
from apps.tenants.models import Tenant, Domain
from apps.accounts.models import User


def provision_tenant(name: str, slug: str, language: str, admin_email: str) -> Tenant:
    # 1. Create tenant record (triggers schema creation)
    tenant = Tenant.objects.create(
        name=name,
        slug=slug,
        language=language,
        schema_name=slug.replace('-', '_'),
        feature_flags=get_default_feature_flags(),
    )

    # 2. Create domain
    Domain.objects.create(
        domain=f"{slug}.nexoflow.io",
        tenant=tenant,
        is_primary=True,
    )

    # 3. Seed tenant schema with defaults
    with schema_context(tenant.schema_name):
        seed_default_warehouse(tenant)
        seed_default_roles()
        create_admin_user(admin_email, tenant)

    return tenant
```

### Feature Flags

```python
# shared/feature_flags.py

DEFAULT_FLAGS = {
    "receiving":         True,
    "directed_putaway":  True,
    "lot_management":    False,
    "expiry_tracking":   False,
    "serial_tracking":   False,
    "catch_weight":      False,
    "qc_inspection":     False,
    "cross_docking":     False,
    "wave_planning":     True,
    "batch_picking":     True,
    "zone_picking":      False,
    "returns":           False,
    "cycle_counting":    True,
    "replenishment":     True,
    "external_carriers": False,
    "internal_carriers": False,
    "edi":               False,
    "customer_portal":   False,
    "ai_copilot":        False,
    "forecasting":       False,
    "slotting":          False,
    "fsma_204":          False,
    "dscsa":             False,
}


def feature_enabled(tenant, flag_name: str) -> bool:
    return tenant.feature_flags.get(flag_name, DEFAULT_FLAGS.get(flag_name, False))


# DRF Permission class using feature flags
class RequiresFeature:
    def __init__(self, flag: str):
        self.flag = flag

    def __call__(self):
        class FeaturePermission(BasePermission):
            def has_permission(self_, request, view):
                return feature_enabled(request.tenant, self.flag)
        return FeaturePermission
```

---

## 5. Authentication & Authorization

### JWT Configuration

```python
# config/settings/base.py

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS':  True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_OBTAIN_SERIALIZER': 'apps.accounts.serializers.NexoFlowTokenObtainSerializer',
}
```

Custom token payload includes tenant context:

```python
# apps/accounts/serializers.py

class NexoFlowTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['tenant_slug']  = user.tenant_slug
        token['role']         = user.role
        token['language']     = user.language or user.tenant.language
        token['device_type']  = 'handheld'  # overridden per device
        return token
```

### RBAC Roles

```python
ROLES = {
    'ASSOCIATE':      {'level': 10, 'description': 'Floor warehouse associate'},
    'LEAD':           {'level': 20, 'description': 'Team lead — floor + exception resolution'},
    'SUPERVISOR':     {'level': 30, 'description': 'Shift supervisor — floor + dashboard'},
    'INVENTORY_CTRL': {'level': 35, 'description': 'Inventory control — counts + adjustments'},
    'MANAGER':        {'level': 40, 'description': 'Operations manager — full operational access'},
    'DIRECTOR':       {'level': 50, 'description': 'Director — all dashboards + analytics'},
    'IT_ADMIN':       {'level': 60, 'description': 'System admin — config + integrations'},
    'TENANT_ADMIN':   {'level': 70, 'description': 'Tenant owner — all access + billing'},
}

# Permission matrix — expand as needed
PERMISSIONS = {
    'inventory.view':          ['ASSOCIATE', 'LEAD', 'SUPERVISOR', 'INVENTORY_CTRL', 'MANAGER', 'DIRECTOR', 'IT_ADMIN', 'TENANT_ADMIN'],
    'inventory.adjust':        ['INVENTORY_CTRL', 'MANAGER', 'IT_ADMIN', 'TENANT_ADMIN'],
    'count.execute':           ['ASSOCIATE', 'LEAD', 'INVENTORY_CTRL', 'SUPERVISOR'],
    'count.approve_variance':  ['INVENTORY_CTRL', 'SUPERVISOR', 'MANAGER'],
    'wave.create':             ['SUPERVISOR', 'MANAGER'],
    'wave.release':            ['SUPERVISOR', 'MANAGER'],
    'shipment.mark_departed':  ['LEAD', 'SUPERVISOR', 'MANAGER'],
    'config.edit':             ['IT_ADMIN', 'TENANT_ADMIN'],
    'user.manage':             ['IT_ADMIN', 'TENANT_ADMIN'],
    'analytics.view':          ['SUPERVISOR', 'INVENTORY_CTRL', 'MANAGER', 'DIRECTOR', 'IT_ADMIN', 'TENANT_ADMIN'],
    'ai.use':                  ['SUPERVISOR', 'MANAGER', 'DIRECTOR'],
}
```

---

## 6. Django Apps & Responsibilities

### `apps/lpn`

Generates and manages License Plate Numbers.

```python
# apps/lpn/services.py

import uuid
from django.db import transaction


class LPNService:
    """
    LPN format: NF-{tenant_prefix}-{sequence:010d}
    e.g.        NF-ACM-0000012345
    
    For GS1 SSCC: 00 + {company_prefix} + {serial_ref:017d} + {check_digit}
    """

    def generate(self, tenant, item, quantity: int, parent_lpn=None) -> 'LPN':
        with transaction.atomic():
            seq = self._next_sequence(tenant)
            lpn_code = self._format(tenant.lpn_prefix, seq)

            return LPN.objects.create(
                code=lpn_code,
                lpn_type='ITEM',
                status='ACTIVE',
                item=item,
                quantity=quantity,
                parent_lpn=parent_lpn,
            )

    def _next_sequence(self, tenant) -> int:
        # Uses PostgreSQL sequence per tenant — atomic, no gaps in prod
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT nextval('lpn_seq_{tenant.schema_name}')")
            return cursor.fetchone()[0]
```

### `apps/labels`

Renders ZPL from templates.

```python
# apps/labels/services.py

class ZPLRenderer:
    """
    Resolves a label template, injects variable data, outputs ZPL string.
    """

    def render(self, template_code: str, context: dict, language: str = 'en-CA') -> str:
        template = LabelTemplate.objects.get(code=template_code)
        zpl_raw = template.zpl_content

        # Resolve bilingual description
        if language == 'fr-CA' and context.get('description_fr'):
            context['description'] = context['description_fr']

        # Variable substitution — {{variable_name}} syntax
        for key, value in context.items():
            zpl_raw = zpl_raw.replace(f'{{{{{key}}}}}', str(value or ''))

        return zpl_raw

    def send_to_printer(self, zpl: str, printer_id: str):
        import socket
        printer = Printer.objects.get(id=printer_id)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((printer.ip_address, printer.port))
            s.sendall(zpl.encode('utf-8'))
```

### `apps/audit`

Immutable event log. **No deletes, no updates.**

```python
# apps/audit/models.py

class AuditLog(models.Model):
    """Append-only. DB trigger prevents UPDATE/DELETE."""
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp       = models.DateTimeField(auto_now_add=True, db_index=True)
    tenant_schema   = models.CharField(max_length=100, db_index=True)
    action          = models.CharField(max_length=100, db_index=True)
    entity_type     = models.CharField(max_length=100)
    entity_id       = models.UUIDField(null=True, blank=True)
    operator_id     = models.UUIDField(null=True, db_index=True)
    operator_name   = models.CharField(max_length=200, blank=True)
    device_id       = models.CharField(max_length=100, blank=True)
    ip_address      = models.GenericIPAddressField(null=True, blank=True)
    payload         = models.JSONField(default=dict)
    old_value       = models.JSONField(null=True, blank=True)
    new_value       = models.JSONField(null=True, blank=True)
    source          = models.CharField(max_length=20, choices=[
                          ('HANDHELD', 'Handheld'), ('API', 'API'),
                          ('DESKTOP',  'Desktop'),  ('CELERY', 'Background Task')])

    class Meta:
        db_table = 'audit_log'
        # Partition by month for performance on large datasets
        # Implement via pg_partman or manual partition management
```

---

## 7. REST API Conventions

### URL Structure

```
/api/v1/{resource}/                          ← list + create
/api/v1/{resource}/{id}/                     ← retrieve + update + delete
/api/v1/{resource}/{id}/{sub-resource}/      ← nested resources

Examples:
GET  /api/v1/inbound/orders/                          ← list POs
POST /api/v1/inbound/orders/                          ← create PO
GET  /api/v1/inbound/orders/{id}/lines/               ← list PO lines
POST /api/v1/receiving/lines/{id}/receive/            ← action endpoint
POST /api/v1/picking/tasks/{id}/pick/                 ← action endpoint
POST /api/v1/lpn/{id}/reprint/                        ← action endpoint
GET  /api/v1/inventory/positions/?item=SKU&status=AVAILABLE
GET  /api/v1/analytics/throughput/?from=2025-01-01&to=2025-01-31&granularity=hour
```

### Standard Response Envelope

```json
// Success
{
  "data": { ... },
  "meta": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-03-01T14:32:10.123Z"
  }
}

// List response
{
  "data": [ ... ],
  "pagination": {
    "count": 1450,
    "next": "/api/v1/inventory/positions/?cursor=eyJpZCI6IjEyMzQ1In0=",
    "previous": null,
    "page_size": 50
  },
  "meta": { "request_id": "...", "timestamp": "..." }
}

// Error
{
  "error": {
    "code": "SCAN_MISMATCH",
    "message": "Le code scanné ne correspond pas à l'article attendu.",
    "detail": { "scanned": "4501-BLK-L", "expected": "4501-BLK-M" },
    "request_id": "..."
  }
}
```

### Pagination

Use **cursor-based pagination** for all large datasets (inventory, movements, audit log). Cursor pagination is stable under concurrent inserts — page-based pagination skips or duplicates records when data changes mid-pagination.

```python
# shared/pagination.py
from rest_framework.pagination import CursorPagination

class StandardCursorPagination(CursorPagination):
    page_size            = 50
    page_size_query_param = 'page_size'
    max_page_size        = 500
    ordering             = '-created_at'

class SmallCursorPagination(StandardCursorPagination):
    page_size = 20

class LargeCursorPagination(StandardCursorPagination):
    page_size = 200  # for handheld task queues, analytics exports
```

### Idempotency

All `POST` mutation endpoints accept `Idempotency-Key` header:

```python
# shared/mixins.py

class IdempotentCreateMixin:
    """
    If Idempotency-Key header present and key seen before,
    return cached response instead of re-executing.
    """
    def create(self, request, *args, **kwargs):
        key = request.headers.get('Idempotency-Key')
        if key:
            cached = cache.get(f'idem:{request.tenant.schema_name}:{key}')
            if cached:
                return Response(cached, status=status.HTTP_200_OK)

        response = super().create(request, *args, **kwargs)

        if key and response.status_code in (200, 201):
            cache.set(f'idem:{request.tenant.schema_name}:{key}',
                      response.data, timeout=86400)  # 24 hours
        return response
```

---

## 8. Celery Task Architecture

### Queue Configuration

```python
# config/settings/base.py

CELERY_BROKER_URL    = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT  = ['json']

CELERY_TASK_ROUTES = {
    # High priority — floor operations
    'apps.labels.tasks.print_label':          {'queue': 'labels'},
    'apps.lpn.tasks.*':                       {'queue': 'high'},
    'apps.outbound.tasks.allocate_order':     {'queue': 'high'},
    'apps.outbound.tasks.release_wave':       {'queue': 'high'},

    # Standard priority
    'apps.notifications.tasks.*':             {'queue': 'default'},
    'apps.integrations.tasks.send_webhook':   {'queue': 'default'},
    'apps.shipping.tasks.*':                  {'queue': 'default'},

    # Low priority — background processing
    'apps.analytics.tasks.*':                 {'queue': 'analytics'},
    'apps.integrations.tasks.process_edi':    {'queue': 'edi'},
    'apps.ai.tasks.*':                        {'queue': 'ai'},
    'apps.audit.tasks.flush_audit_buffer':    {'queue': 'low'},
}

# Workers to run per queue (Kubernetes deployment)
# labels:    3 workers (dedicated — latency critical)
# high:      4 workers
# default:   4 workers
# analytics: 2 workers
# edi:       2 workers
# ai:        2 workers
# low:       1 worker
```

### Key Celery Tasks

```python
# apps/labels/tasks.py

@shared_task(bind=True, max_retries=3, default_retry_delay=2, queue='labels')
def print_label(self, lpn_id: str, label_type: str, printer_id: str):
    """
    Render ZPL and send to thermal printer.
    Retry on socket errors (printer temporarily unavailable).
    """
    try:
        lpn = LPN.objects.get(id=lpn_id)
        context = build_label_context(lpn, label_type)
        zpl = ZPLRenderer().render(label_type, context)
        ZPLRenderer().send_to_printer(zpl, printer_id)
        PrintJob.objects.create(lpn_id=lpn_id, label_type=label_type,
                                printer_id=printer_id, status='SUCCESS')
    except socket.timeout as exc:
        PrintJob.objects.create(lpn_id=lpn_id, label_type=label_type,
                                printer_id=printer_id, status='FAILED',
                                error=str(exc))
        raise self.retry(exc=exc)


# apps/outbound/tasks.py

@shared_task(bind=True, max_retries=2, queue='high')
def allocate_order(self, order_id: str, tenant_schema: str):
    """
    Reserve inventory for an order.
    Uses FEFO logic. Runs in tenant schema context.
    """
    with schema_context(tenant_schema):
        order = OutboundOrder.objects.get(id=order_id)
        AllocationService().allocate(order)


@shared_task(queue='analytics')
def refresh_analytics_aggregate(tenant_schema: str, date_str: str):
    """Nightly: pre-compute daily analytics aggregates into TimescaleDB."""
    with schema_context(tenant_schema):
        AnalyticsService().refresh_daily(date_str)
```

---

## 9. Real-Time with Django Channels

### WebSocket Events

```python
# apps/realtime/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OperationsConsumer(AsyncWebsocketConsumer):
    """
    Supervisor/manager operations dashboard.
    Groups by tenant + warehouse.
    """
    async def connect(self):
        self.tenant_schema = self.scope['tenant'].schema_name
        self.warehouse_id  = self.scope['url_route']['kwargs']['warehouse_id']
        self.group_name    = f"ops.{self.tenant_schema}.{self.warehouse_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive from channel layer (sent by Celery tasks / signals)
    async def wave_progress_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'wave_progress',
            'wave_id': event['wave_id'],
            'picks_complete': event['picks_complete'],
            'picks_total': event['picks_total'],
            'pct': event['pct'],
        }))

    async def exception_created(self, event):
        await self.send(text_data=json.dumps({
            'type': 'exception',
            'exception_id': event['exception_id'],
            'type_code': event['type_code'],
            'location': event['location'],
            'operator': event['operator'],
        }))

    async def inventory_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'inventory_update',
            'item_id': event['item_id'],
            'location_id': event['location_id'],
            'new_quantity': event['new_quantity'],
        }))
```

### Event Dispatch (from Services)

```python
# shared/realtime.py

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_wave_progress(tenant_schema: str, warehouse_id: str, wave_id: str,
                              picks_complete: int, picks_total: int):
    layer = get_channel_layer()
    group = f"ops.{tenant_schema}.{warehouse_id}"
    async_to_sync(layer.group_send)(group, {
        'type': 'wave_progress_update',
        'wave_id': str(wave_id),
        'picks_complete': picks_complete,
        'picks_total': picks_total,
        'pct': round((picks_complete / picks_total) * 100, 1) if picks_total > 0 else 0,
    })
```

---

## 10. LPN Generation Engine

### Sequence Architecture

Each tenant has a dedicated PostgreSQL sequence, created at tenant provisioning:

```sql
-- Created in create_tenant migration
CREATE SEQUENCE lpn_seq_acme_corp START 1 INCREMENT 1 NO CYCLE;
```

Sequences are atomic, no application-level locking required. Sequence values are never reused even if an LPN record is voided.

### LPN Formats

```python
# apps/lpn/formats.py

class LPNFormat:
    # Standard NexoFlow format
    NEXOFLOW = "NF-{prefix}-{seq:010d}"

    # GS1 SSCC (18 digits + check digit)
    # Format: 00 + extension digit (0) + GS1 company prefix (7-10 digits) + serial ref + check digit
    GS1_SSCC = "00{company_prefix}{serial_ref:0{ref_len}d}{check_digit}"

    @staticmethod
    def gs1_check_digit(digits: str) -> int:
        """GS1 check digit calculation (Luhn mod 10 variant)."""
        total = 0
        for i, d in enumerate(reversed(digits)):
            total += int(d) * (3 if i % 2 == 0 else 1)
        return (10 - (total % 10)) % 10
```

---

## 11. Picking Engine

### Pick Path Optimization

The picking engine determines the optimal sequence of locations to visit for a pick task or batch. Uses a nearest-neighbor algorithm (good enough for warehouse dimensions) with optional 2-opt improvement for batches > 20 locations.

```python
# apps/outbound/services/pick_path_optimizer.py

from typing import List
from apps.warehouse.models import Location


class PickPathOptimizer:
    """
    Optimizes pick sequence to minimize travel distance.
    
    Location.sort_sequence is pre-computed: aisle number * 10000 + bay * 100 + level
    This produces a serpentine (S-curve) traversal pattern naturally.
    
    For simple cases (< 30 locations): sort by sort_sequence.
    For complex cases (30+ locations): nearest-neighbor + 2-opt.
    """

    def optimize(self, pick_tasks: List) -> List:
        locations = [t.location for t in pick_tasks]

        if len(locations) <= 30:
            # Simple sort — fast and 90% optimal for typical warehouse layouts
            return sorted(pick_tasks, key=lambda t: t.location.sort_sequence)

        return self._nearest_neighbor(pick_tasks)

    def _nearest_neighbor(self, tasks: List) -> List:
        unvisited = list(tasks)
        ordered = [unvisited.pop(0)]

        while unvisited:
            last = ordered[-1].location
            nearest = min(unvisited,
                          key=lambda t: abs(t.location.sort_sequence - last.sort_sequence))
            ordered.append(nearest)
            unvisited.remove(nearest)

        return ordered
```

### Allocation Engine (FEFO)

```python
# apps/inventory/services/allocation_service.py

from django.db import transaction


class AllocationService:

    @transaction.atomic
    def allocate_order_line(self, order_line, quantity: int) -> List[dict]:
        """
        Allocate inventory for an order line using FEFO.
        Returns list of {position_id, quantity} allocations.
        Raises InsufficientInventoryError if cannot fulfill.
        """
        item = order_line.item
        remaining = quantity
        allocations = []

        # FEFO: order by expiry_date NULLS LAST, then by received_at (FIFO)
        candidates = (
            InventoryPosition.objects
            .select_for_update(skip_locked=True)
            .filter(
                item=item,
                status='AVAILABLE',
                quantity_on_hand__gt=models.F('quantity_allocated'),
            )
            .order_by('expiry_date', 'received_at')
        )

        for position in candidates:
            if remaining <= 0:
                break

            available = position.quantity_on_hand - position.quantity_allocated
            to_allocate = min(available, remaining)

            position.quantity_allocated += to_allocate
            position.save(update_fields=['quantity_allocated', 'updated_at'])

            allocations.append({'position_id': position.id, 'quantity': to_allocate})
            remaining -= to_allocate

        if remaining > 0:
            raise InsufficientInventoryError(
                item=item, requested=quantity, available=quantity - remaining
            )

        return allocations
```

---

## 12. Wave Planning Engine

```python
# apps/outbound/services/wave_service.py

class WaveService:

    def plan_wave(self, template_id: str, manual_order_ids: List[str] = None) -> Wave:
        """
        1. Select orders matching template criteria
        2. Check inventory availability
        3. Create wave + assign pick tasks
        4. Optimize pick paths
        """
        template = WaveTemplate.objects.get(id=template_id)

        # Select eligible orders
        orders = self._select_orders(template, manual_order_ids)
        if not orders:
            raise NoEligibleOrdersError()

        with transaction.atomic():
            wave = Wave.objects.create(
                template=template,
                status='PLANNED',
                order_count=len(orders),
            )

            # Allocate inventory for all orders
            for order in orders:
                self.allocation_service.allocate_order(order)
                order.wave = wave
                order.status = 'WAVED'

            OutboundOrder.objects.bulk_update(orders, ['wave', 'status'])

            # Create pick tasks
            pick_tasks = self._create_pick_tasks(wave, orders)

            # Optimize pick paths per pick method
            if template.pick_method in ('DISCRETE', 'CLUSTER'):
                for group in self._group_by_associate(pick_tasks):
                    optimized = PickPathOptimizer().optimize(group)
                    for i, task in enumerate(optimized):
                        task.sort_sequence = i
                PickTask.objects.bulk_update(pick_tasks, ['sort_sequence'])

        return wave

    def release_wave(self, wave_id: str, released_by_id: str):
        wave = Wave.objects.get(id=wave_id)
        if wave.status != 'PLANNED':
            raise InvalidWaveStatusError(wave.status)

        wave.status = 'RELEASED'
        wave.released_at = timezone.now()
        wave.released_by_id = released_by_id
        wave.save()

        # Broadcast to floor devices
        broadcast_wave_released(wave)
```

---

## 13. EDI Adapter

```python
# apps/integrations/edi/adapter.py

class EDIAdapter:
    """
    Parses and generates X12 EDI documents.
    Uses the 'pyx12' library for parsing, custom generator for output.
    
    Supported: 850, 855, 856, 860, 940, 943, 944, 945, 947, 997
    """

    def ingest_850(self, raw_edi: str, partner_id: str) -> InboundOrder:
        """Parse EDI 850 Purchase Order → create InboundOrder."""
        parser = X12Parser(raw_edi)
        po_data = parser.parse_850()

        order = InboundOrder.objects.create(
            external_po_number=po_data['po_number'],
            vendor=self._resolve_vendor(po_data['sender_id']),
            must_arrive_by=po_data.get('mabd'),
            cancel_date=po_data.get('cancel_date'),
            status='RECEIVED',
        )

        for line in po_data['lines']:
            InboundLine.objects.create(
                inbound_order=order,
                item=self._resolve_item(line['sku'], line['gtin']),
                qty_ordered=line['quantity'],
                unit_price=line.get('unit_price'),
            )

        # Send 997 functional acknowledgment
        self.send_997.delay(partner_id=partner_id, control_number=po_data['control_number'])
        return order

    def generate_945(self, shipment_id: str) -> str:
        """Generate EDI 945 Warehouse Shipping Advice for completed shipment."""
        shipment = Shipment.objects.get(id=shipment_id)
        # ... build X12 945 segments
        return self._render_x12(segments)
```

---

## 14. Carrier Integration

```python
# apps/shipping/carriers/base.py

from abc import ABC, abstractmethod


class CarrierAdapter(ABC):
    """Base class for all carrier integrations."""

    @abstractmethod
    def create_shipment(self, shipment: 'Shipment') -> dict:
        """Returns {'tracking_number': str, 'label_zpl': str, 'label_pdf': bytes}"""
        ...

    @abstractmethod
    def void_label(self, tracking_number: str) -> bool:
        ...

    @abstractmethod
    def get_rates(self, shipment: 'Shipment') -> List[dict]:
        """Returns list of {'carrier': str, 'service': str, 'rate': Decimal, 'transit_days': int}"""
        ...


# apps/shipping/carriers/easypost_adapter.py

import easypost


class EasyPostAdapter(CarrierAdapter):
    """
    Routes to any EasyPost-supported carrier.
    Tenant configures carrier accounts in EasyPost; we relay.
    """

    def __init__(self, api_key: str):
        self.client = easypost.EasyPostClient(api_key)

    def create_shipment(self, shipment) -> dict:
        ep_shipment = self.client.shipment.create(
            to_address=self._build_address(shipment.to_address),
            from_address=self._build_address(shipment.from_address),
            parcel=self._build_parcel(shipment),
            carrier=shipment.carrier_code,
            service=shipment.service_level,
        )
        purchased = self.client.shipment.buy(ep_shipment.id, rate=ep_shipment.lowest_rate())
        return {
            'tracking_number': purchased.tracking_code,
            'label_zpl': purchased.postage_label.label_zpl_url,  # fetch separately
        }
```

---

## 15. AI Co-Pilot Architecture

### RAG Pipeline

```python
# apps/ai/services/copilot_service.py

class CopilotService:
    """
    Conversational assistant grounded in real-time warehouse data.
    
    Architecture:
    1. User query → Intent classification
    2. Intent → Data retrieval (SQL / Elasticsearch)
    3. Data + query → LLM prompt (Claude claude-sonnet-4-20250514 via Anthropic API)
    4. Response → structured output + optional action execution
    """

    SYSTEM_PROMPT = """
    You are NexoFlow's warehouse operations assistant. You have access to real-time
    data from the warehouse including orders, inventory, pick progress, and exceptions.
    
    Answer questions concisely and accurately. For actions (reprint labels, trigger alerts),
    confirm before executing. Always respond in the user's language: {language}.
    
    Current context:
    - Warehouse: {warehouse_name}
    - Active waves: {active_wave_count}
    - Open exceptions: {open_exception_count}
    - Timestamp: {timestamp}
    """

    def query(self, user_message: str, user_id: str, language: str, 
              conversation_history: List[dict]) -> dict:
        # 1. Retrieve relevant context
        context = self._build_context(user_message)

        # 2. Build messages
        messages = conversation_history + [{"role": "user", "content": user_message}]

        # 3. Call Anthropic API
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.SYSTEM_PROMPT.format(**context),
            messages=messages,
            tools=self._get_tools(),
        )

        # 4. Handle tool calls (data lookups, actions)
        if response.stop_reason == "tool_use":
            return self._handle_tool_calls(response, messages, language)

        return {"message": response.content[0].text, "actions": []}

    def _get_tools(self) -> List[dict]:
        return [
            {
                "name": "lookup_lpn",
                "description": "Find current location and status of an LPN",
                "input_schema": {
                    "type": "object",
                    "properties": {"lpn_code": {"type": "string"}},
                    "required": ["lpn_code"]
                }
            },
            {
                "name": "get_order_status",
                "description": "Get current status and detail for an order",
                "input_schema": {
                    "type": "object",
                    "properties": {"order_number": {"type": "string"}},
                    "required": ["order_number"]
                }
            },
            {
                "name": "reprint_label",
                "description": "Reprint a label for an LPN",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "lpn_code": {"type": "string"},
                        "printer_id": {"type": "string"}
                    },
                    "required": ["lpn_code", "printer_id"]
                }
            },
            {
                "name": "get_exceptions",
                "description": "Get list of open warehouse exceptions",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "type_filter": {"type": "string"},
                        "zone_filter": {"type": "string"}
                    }
                }
            },
        ]
```

---

## 16. Frontend Architecture

### Feature-Sliced Design (FSD)

Each feature is a self-contained module:

```
features/picking/
  ├── api/            ← React Query hooks: usePick, usePickTask
  ├── components/     ← Feature-specific components
  │     ├── PickTaskCard.tsx
  │     ├── PickNavigate.tsx
  │     ├── PickConfirmItem.tsx
  │     └── PickQuantity.tsx
  ├── stores/         ← Zustand slice for picking state
  ├── hooks/          ← usePickWorkflow, usePickScanner
  ├── types.ts
  └── index.ts        ← Public API of feature
```

### API Client (React Query + Axios)

```typescript
// src/api/client.ts

import axios from 'axios';
import { QueryClient } from '@tanstack/react-query';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// JWT token injection
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  config.headers['Accept-Language'] = useI18nStore.getState().language;
  config.headers['Idempotency-Key'] = generateIdempotencyKey();
  return config;
});

// Token refresh on 401
apiClient.interceptors.response.use(
  (res) => res,
  async (err) => {
    if (err.response?.status === 401 && !err.config._retry) {
      err.config._retry = true;
      await refreshTokens();
      return apiClient(err.config);
    }
    return Promise.reject(err);
  }
);

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,      // 30s — floor data refreshes frequently
      retry: 2,
      retryDelay: 1000,
      refetchOnWindowFocus: false,  // disable on handheld (accidental focus events)
    },
  },
});
```

### State Management (Zustand)

```typescript
// features/picking/stores/pickStore.ts

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface PickStore {
  currentTaskId: string | null;
  currentPickIndex: number;
  scannedItems: Record<string, number>;  // locationCode -> scanned count
  setCurrentTask: (taskId: string) => void;
  advancePick: () => void;
  recordScan: (locationCode: string, quantity: number) => void;
  reset: () => void;
}

export const usePickStore = create<PickStore>()(
  persist(
    (set) => ({
      currentTaskId:   null,
      currentPickIndex: 0,
      scannedItems:    {},
      setCurrentTask:  (taskId) => set({ currentTaskId: taskId, currentPickIndex: 0 }),
      advancePick:     () => set((s) => ({ currentPickIndex: s.currentPickIndex + 1 })),
      recordScan:      (code, qty) => set((s) => ({
                          scannedItems: { ...s.scannedItems, [code]: qty }
                        })),
      reset:           () => set({ currentTaskId: null, currentPickIndex: 0, scannedItems: {} }),
    }),
    { name: 'nexoflow-pick-state' }  // persisted to localStorage — survives device sleep
  )
);
```

---

## 17. PWA & Offline Strategy

### Service Worker (Workbox)

```typescript
// public/service-worker.ts

import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, StaleWhileRevalidate, NetworkFirst } from 'workbox-strategies';
import { BackgroundSyncPlugin } from 'workbox-background-sync';

// Precache app shell
precacheAndRoute(self.__WB_MANIFEST);
cleanupOutdatedCaches();

// Static assets: Cache First
registerRoute(
  ({ request }) => request.destination === 'font' || request.destination === 'image',
  new CacheFirst({ cacheName: 'assets-v1', plugins: [{ maxEntries: 60 }] })
);

// API read endpoints: Stale While Revalidate (fast response, background refresh)
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/v1/') && url.method === 'GET',
  new StaleWhileRevalidate({
    cacheName: 'api-cache-v1',
    plugins: [{
      // Only cache GET requests that are floor-critical
      cacheKeyWillBeUsed: async ({ request }) => request.url,
    }]
  })
);

// Background sync for offline mutations (pick confirmations, scan events)
const bgSyncPlugin = new BackgroundSyncPlugin('wms-mutations', {
  maxRetentionTime: 24 * 60,  // 24 hours
});

registerRoute(
  ({ url }) => url.pathname.startsWith('/api/v1/') &&
               ['POST', 'PATCH', 'PUT'].includes(url.method || ''),
  new NetworkFirst({
    plugins: [bgSyncPlugin],
    networkTimeoutSeconds: 5,
  }),
  'POST'
);
```

### Offline Data Cache Strategy

```typescript
// hooks/useOfflineCache.ts

/**
 * Pre-fetches and caches critical data for offline operation:
 * - Active pick tasks for current user
 * - Location codes for current zone
 * - Item master for current wave's SKUs
 * - Label templates
 * 
 * Called on login and wave assignment.
 */
export const usePrimeOfflineCache = () => {
  const queryClient = useQueryClient();

  const prime = async (waveId: string) => {
    await Promise.all([
      queryClient.prefetchQuery(['pickTasks', waveId]),
      queryClient.prefetchQuery(['locations', 'current-zone']),
      queryClient.prefetchQuery(['labelTemplates']),
    ]);
  };

  return { prime };
};
```

---

## 18. i18n Architecture

### React (react-i18next)

```typescript
// src/app/i18n.ts

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import HttpBackend from 'i18next-http-backend';

i18n
  .use(HttpBackend)
  .use(initReactI18next)
  .init({
    lng: 'en-CA',               // overridden by tenant default from JWT
    fallbackLng: 'en-CA',
    ns: ['common'],             // only common namespace loaded at init
    defaultNS: 'common',
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
    interpolation: { escapeValue: false },
    react: { useSuspense: true },
  });

// Load feature namespace on demand
export const loadNamespace = (ns: string) => i18n.loadNamespaces(ns);
```

### Django (gettext)

```python
# config/settings/base.py

LANGUAGE_CODE = 'en-ca'
LANGUAGES = [
    ('en-CA', 'English (Canada)'),
    ('fr-CA', 'Français (Canada)'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
USE_I18N = True
USE_L10N = True

# API response language follows Accept-Language header
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',
    ...
]
```

```python
# In serializers, model verbose names, error messages:
from django.utils.translation import gettext_lazy as _

class ReceivingSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        min_value=1,
        error_messages={
            'min_value': _('La quantité doit être supérieure à zéro.')
        }
    )
```

---

## 19. Search & Elasticsearch

```python
# apps/inventory/search.py

from elasticsearch_dsl import Document, Text, Keyword, Integer, Date, Boolean


class InventoryDocument(Document):
    """
    Elasticsearch document for inventory search.
    Synced from PostgreSQL via post_save signals + Celery.
    """
    lpn_code        = Keyword()
    sku             = Keyword()
    description_en  = Text(analyzer='english')
    description_fr  = Text(analyzer='french')
    lot_number      = Keyword()
    serial_number   = Keyword()
    location_code   = Keyword()
    zone_code       = Keyword()
    status          = Keyword()
    expiry_date     = Date()
    quantity_on_hand = Integer()
    is_available    = Boolean()

    class Index:
        name = 'inventory'
        settings = {
            'number_of_shards': 2,
            'number_of_replicas': 1,
        }


# Global search endpoint — powers Cmd+K
class GlobalSearchView(APIView):
    def get(self, request):
        q = request.query_params.get('q', '')
        if not q or len(q) < 2:
            return Response({'results': []})

        # Multi-index search across LPNs, orders, SKUs, locations
        results = (
            MultiSearch()
            .add(InventoryDocument.search().query('multi_match', query=q,
                  fields=['lpn_code^3', 'sku^3', 'description_en', 'description_fr', 'lot_number']))
            .add(OrderDocument.search().query('multi_match', query=q,
                  fields=['order_number^3', 'customer_po']))
            .add(LocationDocument.search().query('term', code=q.upper()))
            .execute()
        )

        return Response({'results': self._format(results)})
```

---

## 20. Infrastructure & DevOps

### Docker Compose (Local Dev)

```yaml
# docker-compose.yml

services:
  db:
    image: timescale/timescaledb:latest-pg16
    environment:
      POSTGRES_DB: nexoflow
      POSTGRES_USER: nexoflow
      POSTGRES_PASSWORD: dev_password
    ports: ["5432:5432"]
    volumes: [postgres_data:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    environment:
      discovery.type: single-node
      ES_JAVA_OPTS: "-Xms512m -Xmx512m"
      xpack.security.enabled: "false"
    ports: ["9200:9200"]

  backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    environment:
      DATABASE_URL: postgres://nexoflow:dev_password@db:5432/nexoflow
      REDIS_URL: redis://redis:6379/0
      ELASTICSEARCH_URL: http://elasticsearch:9200
      DJANGO_SETTINGS_MODULE: config.settings.development
    ports: ["8000:8000"]
    depends_on: [db, redis, elasticsearch]
    volumes: [./backend:/app]

  celery:
    build: ./backend
    command: celery -A config worker -Q high,default,labels -l info --concurrency=4
    environment: *backend-env
    depends_on: [db, redis]

  celery-beat:
    build: ./backend
    command: celery -A config beat -l info
    depends_on: [redis]

  channels:
    build: ./backend
    command: daphne -b 0.0.0.0 -p 8001 config.asgi:application
    ports: ["8001:8001"]
    depends_on: [redis]

  frontend:
    build: ./frontend
    command: npm run dev -- --host
    ports: ["5173:5173"]
    volumes: [./frontend:/app, /app/node_modules]
```

### Kubernetes Deployment (Production)

```yaml
# k8s/base/backend-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexoflow-backend
spec:
  replicas: 4
  selector:
    matchLabels: { app: nexoflow-backend }
  template:
    spec:
      containers:
        - name: backend
          image: nexoflow/backend:latest
          command: [gunicorn, config.wsgi:application]
          args: [-b, "0.0.0.0:8000", -w, "4", --timeout, "60",
                 --worker-class, uvicorn.workers.UvicornWorker]
          resources:
            requests: { cpu: 250m, memory: 512Mi }
            limits:   { cpu: 1000m, memory: 1Gi }
          livenessProbe:
            httpGet: { path: /health/, port: 8000 }
            initialDelaySeconds: 30
          readinessProbe:
            httpGet: { path: /health/ready/, port: 8000 }
          envFrom:
            - secretRef: { name: nexoflow-secrets }
            - configMapRef: { name: nexoflow-config }
```

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres: { image: timescale/timescaledb:latest-pg16, ... }
      redis:    { image: redis:7-alpine }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements/test.txt
      - run: python manage.py test --parallel --verbosity=2
      - run: coverage run manage.py test && coverage report --fail-under=85

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run test:coverage
      - run: npm run build
      - run: npx playwright test  # E2E tests

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install bandit safety
      - run: bandit -r backend/ -ll
      - run: safety check -r requirements/base.txt
```

---

## 21. Testing Strategy

### Backend Testing

```python
# Rule: every service method has a unit test. Every API endpoint has an integration test.

# apps/outbound/tests/test_allocation_service.py

from django.test import TestCase
from django_tenants.test.cases import TenantTestCase   # runs in tenant schema


class AllocationServiceTest(TenantTestCase):

    def setUp(self):
        self.item = ItemFactory()
        self.location = LocationFactory()

    def test_allocate_fefo_order(self):
        """Verify FEFO: earlier expiry allocated first."""
        pos_later  = InventoryPositionFactory(item=self.item, expiry_date=date(2026, 6, 1), quantity_on_hand=10)
        pos_earlier = InventoryPositionFactory(item=self.item, expiry_date=date(2026, 1, 1), quantity_on_hand=10)

        allocations = AllocationService().allocate_order_line(
            order_line=OrderLineFactory(item=self.item),
            quantity=5
        )

        assert allocations[0]['position_id'] == pos_earlier.id
        pos_earlier.refresh_from_db()
        assert pos_earlier.quantity_allocated == 5

    def test_raises_on_insufficient_stock(self):
        InventoryPositionFactory(item=self.item, quantity_on_hand=3)
        with self.assertRaises(InsufficientInventoryError):
            AllocationService().allocate_order_line(
                order_line=OrderLineFactory(item=self.item), quantity=10
            )

    def test_allocation_creates_movement_record(self):
        InventoryPositionFactory(item=self.item, quantity_on_hand=20)
        AllocationService().allocate_order_line(
            order_line=OrderLineFactory(item=self.item), quantity=5
        )
        assert InventoryMovement.objects.filter(movement_type='ALLOCATE').count() == 1
```

### Frontend Testing

```typescript
// features/picking/components/__tests__/PickConfirmItem.test.tsx

import { render, fireEvent, waitFor } from '@testing-library/react';
import { ScanInput } from '@/components/ui/ScanInput';

describe('ScanInput', () => {
  it('calls onScan with scanned value on Enter', async () => {
    const onScan = vi.fn();
    const { getByRole } = render(<ScanInput onScan={onScan} autoFocus />);

    const input = getByRole('textbox');
    fireEvent.change(input, { target: { value: 'NF-ACM-0000012345' } });
    fireEvent.keyDown(input, { key: 'Enter' });

    await waitFor(() => expect(onScan).toHaveBeenCalledWith('NF-ACM-0000012345'));
  });

  it('shows error state on scan mismatch', async () => {
    const onError = vi.fn();
    // ... test error visual state
  });
});
```

### Coverage Targets

| Layer | Tool | Target |
|-------|------|--------|
| Django services | pytest-django | 90% line coverage |
| Django API endpoints | APIClient tests | 100% endpoint coverage |
| React components | Vitest + RTL | 80% line coverage |
| Critical flows (receive, pick, ship) | Playwright E2E | 100% happy path |
| Integration (EDI parsing) | pytest | 95% coverage |

---

## 22. Security Implementation

### Django Security Checklist

```python
# config/settings/production.py

SECURE_SSL_REDIRECT            = True
SECURE_HSTS_SECONDS            = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD            = True
SECURE_CONTENT_TYPE_NOSNIFF    = True
X_FRAME_OPTIONS                = 'DENY'
CSRF_COOKIE_SECURE             = True
SESSION_COOKIE_SECURE          = True
SESSION_COOKIE_HTTPONLY        = True

# Rate limiting (django-ratelimit)
RATELIMIT_DEFAULT = '100/m'   # per IP per minute

# Tenant-specific limits via Redis
RATELIMIT_ENABLE = True
```

### Database Security

```sql
-- Audit log protection: prevent UPDATE and DELETE
CREATE OR REPLACE RULE protect_audit_update AS ON UPDATE TO audit_log DO INSTEAD NOTHING;
CREATE OR REPLACE RULE protect_audit_delete AS ON DELETE TO audit_log DO INSTEAD NOTHING;

-- Row-level security (extra layer for shared-schema scenarios in future)
ALTER TABLE inventory_position ENABLE ROW LEVEL SECURITY;
```

---

## 23. Performance Targets & SLAs

| Endpoint / Operation | P50 | P95 | P99 | Notes |
|---|---|---|---|---|
| Scan confirmation (receive/pick/stow) | < 200ms | < 500ms | < 1s | Critical — blocks associate |
| Task queue load (handheld) | < 300ms | < 600ms | < 1.2s | First screen after login |
| Label print (queue to TCP send) | < 1s | < 2s | < 3s | Includes Celery queue time |
| Wave release (1000 orders) | < 5s | < 10s | < 20s | Background task |
| Dashboard KPIs load | < 400ms | < 800ms | < 1.5s | Pre-computed aggregates |
| Global search (Cmd+K) | < 150ms | < 300ms | < 500ms | Elasticsearch |
| Inventory position query | < 100ms | < 250ms | < 500ms | Indexed query |
| EDI 856 ingest | < 2s | < 5s | < 10s | Per document |
| Analytics report (30 days) | < 3s | < 8s | < 15s | TimescaleDB aggregates |
| AI Co-Pilot response | < 3s | < 6s | < 10s | Anthropic API call |

### Uptime SLA

- **Production:** 99.9% monthly uptime (< 43 min/month downtime)
- **Planned maintenance:** Tenant-specific maintenance windows (configurable per tenant timezone)
- **Zero-downtime deploys:** Rolling deployments via Kubernetes, database migrations backward-compatible

---

## 24. Environment Configuration

```bash
# .env.example — all required environment variables

# Django
DJANGO_SECRET_KEY=
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_ALLOWED_HOSTS=*.nexoflow.io

# Database
DATABASE_URL=postgres://nexoflow:password@db:5432/nexoflow
DATABASE_POOL_MIN=5
DATABASE_POOL_MAX=20

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_CHANNEL_URL=redis://redis:6379/1

# Elasticsearch
ELASTICSEARCH_URL=https://es:9200
ELASTICSEARCH_USERNAME=
ELASTICSEARCH_PASSWORD=

# AWS S3 (label templates, documents)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET_NAME=nexoflow-tenant-data
AWS_S3_REGION=ca-central-1

# Anthropic (AI Co-Pilot)
ANTHROPIC_API_KEY=

# EasyPost (carrier labels)
EASYPOST_API_KEY=

# Sentry (error tracking)
SENTRY_DSN=

# Email
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@nexoflow.io

# JWT
JWT_SIGNING_KEY=
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30
JWT_REFRESH_TOKEN_LIFETIME_DAYS=1
```

---

## 25. Migration Strategy

### Django Migration Rules

1. **All migrations must be backward-compatible.** A deployed migration cannot break the running version of the code. Use two-phase migrations for breaking changes (add column nullable → deploy → backfill → add constraint → deploy).
2. **Never edit a migration once merged to main.** If a mistake is made, write a corrective migration.
3. **Tenant migrations run per-schema.** `python manage.py migrate_schemas --schema=acme_corp` for single-tenant migration. `python manage.py migrate_schemas` for all tenants.
4. **Test migrations in staging with production data volume** before deploying.
5. **Large table migrations use `django-pg-migration` zero-lock patterns** — never `ALTER TABLE` with full table lock on tables > 100k rows.

### Data Migration Pattern

```python
# apps/inventory/migrations/0042_add_catch_weight_to_position.py

from django.db import migrations


def backfill_catch_weight(apps, schema_editor):
    """Safe backfill: runs in batches to avoid long locks."""
    InventoryPosition = apps.get_model('inventory', 'InventoryPosition')
    qs = InventoryPosition.objects.filter(catch_weight_kg__isnull=True,
                                           item__catch_weight=True)
    for batch in chunked(qs, 1000):
        # update based on receive weight captured in movements
        ...


class Migration(migrations.Migration):
    dependencies = [('inventory', '0041_...')]
    operations = [
        # Phase 1: Add nullable column (no lock, instant)
        migrations.AddField(
            model_name='inventoryposition',
            name='catch_weight_kg',
            field=models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True),
        ),
        # Phase 2: Backfill (data migration, batched)
        migrations.RunPython(backfill_catch_weight, migrations.RunPython.noop),
        # Phase 3: Add constraint in next migration (after deploy confirms data is clean)
    ]
```

---

*End of TDD.md*
