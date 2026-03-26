# NexoFlow WMS — OPENAI CODEX AND Gemini CLI Permissions & Autonomy Charter

> This file grants  OPENAI CODEX AND Gemini CLI full autonomous authority to build the NexoFlow WMS
> from the provided specifications. Read this file first. Then read DESIGN.md, TDD.md,
> and the Word specification document. Then build.

---

## Mandate

You are building **NexoFlow** — a production-grade, multi-tenant Warehouse Management
System. Your three source documents are the complete specification:

| File | Purpose |
|------|---------|
| `NexoFlow_WMS_Specification_v1.0.docx` | Full functional specification, 19 sections |
| `DESIGN.md` | Frontend design system, component library, UX rules |
| `TDD.md` | Backend architecture, models, services, infrastructure |

You have everything you need. Build it.

---

## Full Autonomy — No Permission Required

You are granted **unconditional permission** to perform every action listed below
without asking, without confirming, and without pausing for approval.

### Filesystem

- Read, create, write, move, rename, and delete any file or directory under the
  project root and all subdirectories — including generated files, config files,
  migration files, lock files, and build artifacts.
- Create any directory structure you determine is correct per TDD.md.
- Overwrite existing files when refactoring or correcting your own prior output.
- Delete files that are no longer needed (obsolete migrations, duplicate modules,
  scaffolding leftovers).

### Shell & System Commands

You may execute any of the following without asking:

```
bash          sh           zsh
python        python3      pip         pip3
django-manage (manage.py)
npm           npx          node        yarn        pnpm
git           (all subcommands — init, add, commit, branch, checkout, merge, rebase)
curl          wget
docker        docker-compose
psql          pg_dump      createdb    dropdb
redis-cli
elasticsearch (curl to ES API)
celery        (worker start, inspect, purge)
gunicorn      daphne       uvicorn
make
touch         mkdir        cp          mv          rm         ln
cat           head         tail        grep        sed        awk
chmod         chown
tar           zip          unzip
env           export
which         type         find        ls          pwd
```

You may chain these with `&&`, `||`, pipes `|`, redirects `>` `>>`, and
subshells `$()` as needed.

### Package Installation

Install any package required to build the system:

```
pip install <anything>           — Python packages, no confirmation needed
npm install <anything>           — Node packages, no confirmation needed
npm install -g <anything>        — Global Node tools
apt-get install <anything>       — System packages if available
```

If a package is unavailable in the environment, choose the best available
alternative and proceed. Document the substitution in a comment.

### Database Operations

- Run `python manage.py migrate` and `python manage.py migrate_schemas` freely.
- Create, alter, and drop tables as migrations require.
- Run `python manage.py createsuperuser --noinput` or equivalent seeding scripts.
- Execute raw SQL when needed for sequences, triggers, indexes, and partitions
  as specified in TDD.md.
- Seed test and development data without asking.

### Code Generation

- Generate all models, serializers, views, URLs, admin registrations,
  Celery tasks, signals, management commands, and migrations.
- Generate all React components, hooks, stores, API clients, utility functions,
  type definitions, and test files.
- Generate all configuration files: `settings/*.py`, `docker-compose.yml`,
  `Dockerfile.*`, `tailwind.config.ts`, `vite.config.ts`, `capacitor.config.ts`,
  `pyproject.toml`, `package.json`, `.env.example`, and all others.
- Generate all translation files (`locale/*/LC_MESSAGES/django.po`,
  `src/locales/en-CA/*.json`, `src/locales/fr-CA/*.json`).
- Generate Kubernetes manifests, Helm chart values, and CI/CD pipeline files.

### Testing

- Write and run tests freely: `pytest`, `python manage.py test`, `npm test`,
  `npm run test:coverage`, `npx playwright test`.
- Generate test fixtures, factories (`factory_boy`, `faker`), and seed data.
- If a test fails, fix the code and re-run — repeat until green, no check-in needed.

### Refactoring

- Refactor any code you previously wrote if you determine a better approach.
- Rename files, split modules, merge modules — whatever produces the cleanest
  architecture per TDD.md.
- Do not preserve bad decisions out of caution. Fix them.

---

## How to Work

### Start Here

1. Read this file completely.
2. Read `TDD.md` completely.
3. Read `DESIGN.md` completely.
4. Skim `NexoFlow_WMS_Specification_v1.0.docx` for functional detail.
5. Set up the project structure per TDD.md Section 1.
6. Build in the order below.

### Build Order

Work in this sequence. Each phase should be fully functional before moving to the next.

```
Phase 1 — Foundation
  ├── Django project scaffold (config/, apps/, shared/)
  ├── PostgreSQL connection + TimescaleDB
  ├── django-tenants setup (public schema, Tenant model, Domain model)
  ├── Redis connection
  ├── Celery config (queues as per TDD.md Section 8)
  ├── Django Channels + ASGI config
  ├── Base settings (base/development/production/test)
  ├── .env.example with all variables
  └── docker-compose.yml (full local stack)

Phase 2 — Auth & Core Models
  ├── accounts app (User, Role, RBAC permissions)
  ├── JWT auth (simplejwt, custom token payload with tenant + role + language)
  ├── warehouse app (Warehouse, Zone, Location models)
  ├── items app (Item model with all attributes)
  ├── lpn app (LPN model + LPNService + sequence-per-tenant)
  └── audit app (AuditLog append-only model + DB protection rules)

Phase 3 — Inventory Engine
  ├── inventory app (InventoryPosition, InventoryMovement)
  ├── AllocationService (FEFO, SELECT FOR UPDATE)
  ├── InventoryService (apply_movement, adjust, transfer)
  └── inventory signals → Elasticsearch sync

Phase 4 — Inbound
  ├── inbound app (InboundOrder, InboundLine, ReceiveEvent)
  ├── ReceivingService (full receive transaction per TDD.md)
  ├── QC workflow models and service
  ├── ASN / PO ingest API endpoints
  └── Receiving API (scan, receive line, complete)

Phase 5 — Labels & Printing
  ├── labels app (LabelTemplate, Printer, PrintJob models)
  ├── ZPLRenderer service
  ├── Bilingual label context builder
  └── print_label Celery task (retry logic per TDD.md)

Phase 6 — Outbound
  ├── outbound app (OutboundOrder, OrderLine, Wave, PickTask, Container)
  ├── WaveService (plan, release per TDD.md Section 12)
  ├── PickPathOptimizer (nearest-neighbor + 2-opt)
  ├── Pick workflow API (navigate → scan location → scan item → qty → next)
  └── Pack workflow API (scan tote → verify items → select carton → close → print label)

Phase 7 — Shipping
  ├── shipping app (Shipment, Manifest, CarrierAccount)
  ├── EasyPostAdapter (CarrierAdapter base class)
  ├── Internal fleet (push-ship UI endpoints, mark-departed)
  └── Carrier rate shopping endpoint

Phase 8 — Returns
  ├── returns app (RMA, ReturnLine, Disposition)
  ├── Returns receiving workflow
  └── Disposition engine (restock / RTV / quarantine / destroy)

Phase 9 — Inventory Control
  ├── counting app (CountTask, CountResult, CountVariance)
  ├── Cycle count task generation (ABC-driven)
  ├── Count execute API (scan location → enter qty → submit)
  └── Variance approval workflow

Phase 10 — Integrations
  ├── integrations app (EDIPartner, WebhookConfig, ConnectorLog)
  ├── EDI adapter (X12 parser for 850, 856, 940; generator for 855, 945, 947, 997)
  └── Outbound webhook dispatcher (Celery task, retry with backoff)

Phase 11 — Analytics
  ├── analytics app (pre-computed aggregate models)
  ├── TimescaleDB continuous aggregates for throughput, accuracy, cycle time
  ├── Analytics API endpoints (throughput, PPH, accuracy, forecasting)
  └── Nightly refresh Celery beat task

Phase 12 — AI Co-Pilot
  ├── ai app (Conversation, Message models)
  ├── CopilotService with Anthropic tool-use per TDD.md Section 15
  ├── Tool implementations (lookup_lpn, get_order_status, reprint_label, get_exceptions)
  └── AI API endpoint (POST /api/v1/ai/query/)

Phase 13 — Real-Time
  ├── Django Channels consumers (OperationsConsumer per TDD.md Section 9)
  ├── WebSocket routing
  └── broadcast_* helper functions wired into all relevant services

Phase 14 — React PWA Frontend
  ├── Vite + React 18 + TypeScript project scaffold
  ├── Tailwind config with full design token extension from DESIGN.md
  ├── Design system components (ScanInput, Button, StatusBadge, KPICard,
  │     DataTable, ScanFeedback, Toast, Modal, Drawer, Skeleton, EmptyState)
  ├── react-i18next setup (all namespaces, fr-CA + en-CA JSON files)
  ├── React Query + Axios API client (JWT refresh, Accept-Language, Idempotency-Key)
  ├── Zustand stores (auth, i18n, per-feature state)
  ├── PWA manifest + Workbox service worker (offline strategy per TDD.md Section 17)
  ├── App routing (all routes per DESIGN.md Section 15)
  ├── Floor PWA screens (all 20 handheld screens per DESIGN.md Section 9)
  ├── Desktop dashboard screens (Operations Overview, all management screens)
  └── Capacitor config for native device wrapping

Phase 15 — OpenAPI & Documentation
  ├── drf-spectacular schema generation (auto from ViewSets)
  ├── /api/schema/swagger-ui/ endpoint
  └── /api/schema/redoc/ endpoint
```

### Decision Rules

When the specifications are silent on an implementation detail, apply these rules
in order:

1. **Follow TDD.md** — it is the authoritative technical reference.
2. **Follow DESIGN.md** — for all frontend decisions.
3. **Follow the Word spec** — for functional behavior.
4. **Apply industry best practice** — Django conventions, React conventions,
   security defaults, performance defaults.
5. **Prefer explicit over implicit** — readable code over clever code.
6. **Never sacrifice correctness for speed** — if something needs a transaction,
   use one. If something needs an index, add it.

### When You Hit a Problem

Do not stop. Do not ask. Apply this decision tree:

```
Package not available?
  → Find best alternative, install it, add a comment explaining the substitution.

Migration conflict?
  → Resolve it, squash if needed, continue.

Test failing?
  → Fix the code until the test passes. Do not skip or delete tests.

Docker/service not available in environment?
  → Mock the service for local dev, configure real service for production settings.
     Add a clear TODO comment and continue.

Type error / import error?
  → Fix it. Don't leave broken imports.

Environment variable missing?
  → Use a sensible default for development, raise ImproperlyConfigured in production.

Specification ambiguity?
  → Make the most defensible technical decision, leave a one-line comment
     explaining your reasoning, move on.
```

---

## Quality Standards

Every file you produce must meet these standards. No exceptions.

### Python / Django

- Type hints on all function signatures.
- Docstrings on all service methods and non-obvious functions.
- No bare `except:` — always catch specific exceptions.
- No `print()` — use `logging.getLogger(__name__)`.
- All strings that appear in the UI use `gettext_lazy`.
- All database queries touching > 1 table use `select_related` or `prefetch_related`.
- All bulk operations use `bulk_create` / `bulk_update`.
- All financial/quantity fields are `DecimalField` — never `FloatField`.
- All primary keys are UUID.
- `transaction.atomic()` on every service method that writes to multiple tables.

### TypeScript / React

- Strict TypeScript (`"strict": true` in tsconfig). No `any` except where
  genuinely unavoidable, and then annotated with a `// TODO: type this` comment.
- Every component accepts and forwards `className` prop.
- All text via `useTranslation()` — zero hardcoded user-facing strings.
- No inline styles — Tailwind classes only.
- Custom hooks prefixed `use`.
- All async operations handle loading, error, and empty states.
- All forms use controlled components with validation.

### General

- Every new Django app has: `models.py`, `serializers.py`, `views.py`, `urls.py`,
  `services.py`, `admin.py`, `tests/` directory.
- Every React feature has: `api/`, `components/`, `hooks/`, `types.ts`, `index.ts`.
- No dead code, no commented-out blocks, no `TODO` items that are actually
  necessary for the feature to function.
- Git commits after each phase with a clear message.

---

## Scope Boundaries

### In Scope — Build This

Everything in TDD.md, DESIGN.md, and the Word specification.

### Out of Scope — Do Not Build

- Billing / subscription management (Stripe integration, invoicing)
- GDPR consent UI (note it as a future module in a TODO comment in the returns app)
- Customer-facing portal (stub the URL, return 501 Not Implemented)
- AMR / robotics integration (stub the interface only)
- Blockchain traceability (stub only)
- Augmented reality picking (stub only)

For everything out of scope: create the stub (empty view returning 501,
placeholder route, commented interface) so the architecture is ready,
then move on.

---

## Final Check Before Shipping Each Phase

Before considering a phase complete, verify:

- [ ] All models have migrations and migrations are clean (`showmigrations` shows no issues)
- [ ] All API endpoints return correct HTTP status codes
- [ ] All endpoints are authenticated (no accidental public endpoints)
- [ ] All service methods are covered by at least one test
- [ ] `python manage.py check --deploy` passes (in production settings)
- [ ] No hardcoded secrets, passwords, or API keys in any file
- [ ] FR/EN translations present for every user-facing string added in this phase
- [ ] Audit log entries written for every state-changing operation in this phase

---

## You Have Everything You Need. Start Building.
