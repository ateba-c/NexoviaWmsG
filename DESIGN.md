# NexoFlow WMS — Design Document

> **Audience:** Frontend engineers, UX leads, design system contributors  
> **Stack:** React 18 + Vite, Tailwind CSS, react-i18next, Capacitor.js  
> **Revision:** 1.0

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Design System — Tokens & Primitives](#2-design-system--tokens--primitives)
3. [Typography](#3-typography)
4. [Color System](#4-color-system)
5. [Spacing & Layout Grid](#5-spacing--layout-grid)
6. [Component Library](#6-component-library)
7. [Iconography](#7-iconography)
8. [Motion & Animation](#8-motion--animation)
9. [PWA Floor Interface — Handheld UX](#9-pwa-floor-interface--handheld-ux)
10. [Desktop Dashboard Interface](#10-desktop-dashboard-interface)
11. [Responsive Breakpoints](#11-responsive-breakpoints)
12. [Accessibility (WCAG 2.1 AA)](#12-accessibility-wcag-21-aa)
13. [Bilingual UI Design (FR/EN)](#13-bilingual-ui-design-fren)
14. [Dark Mode](#14-dark-mode)
15. [Page & Screen Catalogue](#15-page--screen-catalogue)
16. [State Design — Loading, Empty, Error](#16-state-design--loading-empty-error)
17. [ZPL Label Design Guidelines](#17-zpl-label-design-guidelines)
18. [Design Tokens Export](#18-design-tokens-export)

---

## 1. Design Philosophy

NexoFlow operates in two radically different contexts that must feel like one coherent product:

**The Floor** — A warehouse associate wearing gloves, holding a Zebra TC55 in one hand and a carton in the other, under fluorescent lights, surrounded by noise. Every tap must land. Every scan result must be instantly understood. There is no room for ambiguity, no tolerance for small touch targets, no place for decorative flourish that competes with signal.

**The Office** — A warehouse director reviewing throughput at 7 AM, a supervisor triaging pick exceptions on a desktop, an inventory analyst drilling into cycle count accuracy over the past quarter. Dense information, multi-panel layouts, data-rich charts, and rapid navigation between views.

### Core Design Principles

**1. Signal Over Decoration**  
Every visual element must earn its place. If it doesn't communicate state, hierarchy, or action — remove it. This is especially critical on handheld devices.

**2. Clarity at a Glance**  
A user should understand the current state and required next action within 1 second of looking at the screen. Use size, color, and position hierarchy to make the primary action unmistakable.

**3. Fail Loudly, Succeed Quietly**  
Errors are large, red, and demand attention. Successes are brief, green, and get out of the way. The system should feel calm when things are working and urgent when they are not.

**4. Context Collapse Resistance**  
Every screen must be self-sufficient. A floor associate interrupted mid-task, who puts down the device and picks it up 20 minutes later, must immediately understand where they are and what they were doing without re-reading the screen.

**5. Industrial Aesthetic — Refined**  
Not brutalist. Not clinical. Think: the cockpit of a well-designed aircraft. Purposeful density, clear hierarchy, confidence. Dark navy primary, electric blue accent. Authoritative but not aggressive.

---

## 2. Design System — Tokens & Primitives

The entire design system is expressed as CSS custom properties (design tokens). No hardcoded values anywhere in component code. Tokens are defined at `:root` and overridden for dark mode at `[data-theme="dark"]`.

```css
/* tokens.css — Single source of truth */
:root {
  /* ── Brand ─────────────────────────────── */
  --color-brand-900: #0d1f3c;
  --color-brand-800: #1b3a6b;   /* primary */
  --color-brand-700: #214a87;
  --color-brand-600: #2a5ea8;
  --color-brand-500: #3572c6;
  --color-brand-400: #5b8fd4;
  --color-brand-300: #8db3e2;
  --color-brand-200: #c0d7f0;
  --color-brand-100: #e8f2fb;
  --color-brand-50:  #f4f8fd;

  /* ── Accent (Electric Blue) ─────────────── */
  --color-accent-600: #0660a8;
  --color-accent-500: #0f7cbf;   /* primary accent */
  --color-accent-400: #2894d4;
  --color-accent-300: #56aee0;
  --color-accent-200: #a0d0ee;
  --color-accent-100: #e0f2fb;

  /* ── Success / Green ────────────────────── */
  --color-success-700: #166534;
  --color-success-500: #16a34a;
  --color-success-400: #22c55e;
  --color-success-100: #dcfce7;

  /* ── Warning / Amber ────────────────────── */
  --color-warning-700: #92400e;
  --color-warning-500: #d97706;
  --color-warning-400: #f59e0b;
  --color-warning-100: #fef3c7;

  /* ── Danger / Red ───────────────────────── */
  --color-danger-700: #991b1b;
  --color-danger-500: #dc2626;
  --color-danger-400: #ef4444;
  --color-danger-100: #fee2e2;

  /* ── Neutral ────────────────────────────── */
  --color-neutral-950: #0a0a0f;
  --color-neutral-900: #111827;
  --color-neutral-800: #1f2937;
  --color-neutral-700: #374151;
  --color-neutral-600: #4b5563;
  --color-neutral-500: #6b7280;
  --color-neutral-400: #9ca3af;
  --color-neutral-300: #d1d5db;
  --color-neutral-200: #e5e7eb;
  --color-neutral-100: #f3f4f6;
  --color-neutral-50:  #f9fafb;

  /* ── Semantic Surface ───────────────────── */
  --surface-page:       #f4f6f9;
  --surface-card:       #ffffff;
  --surface-card-hover: #f8fafc;
  --surface-overlay:    rgba(11, 21, 41, 0.72);
  --surface-sidebar:    #1b3a6b;

  /* ── Semantic Text ──────────────────────── */
  --text-primary:   #111827;
  --text-secondary: #4b5563;
  --text-tertiary:  #9ca3af;
  --text-inverse:   #ffffff;
  --text-link:      #0f7cbf;

  /* ── Semantic Border ────────────────────── */
  --border-default: #e5e7eb;
  --border-strong:  #d1d5db;
  --border-focus:   #0f7cbf;

  /* ── Shadow ─────────────────────────────── */
  --shadow-xs:  0 1px 2px rgba(0,0,0,0.05);
  --shadow-sm:  0 1px 3px rgba(0,0,0,0.10), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md:  0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
  --shadow-lg:  0 10px 15px rgba(0,0,0,0.10), 0 4px 6px rgba(0,0,0,0.05);
  --shadow-xl:  0 20px 25px rgba(0,0,0,0.10), 0 10px 10px rgba(0,0,0,0.04);

  /* ── Radius ─────────────────────────────── */
  --radius-xs:  2px;
  --radius-sm:  4px;
  --radius-md:  8px;
  --radius-lg:  12px;
  --radius-xl:  16px;
  --radius-2xl: 24px;
  --radius-full: 9999px;

  /* ── Spacing Scale (4px base) ───────────── */
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;

  /* ── Z-Index ────────────────────────────── */
  --z-base:    0;
  --z-raised:  10;
  --z-dropdown:200;
  --z-sticky:  300;
  --z-overlay: 400;
  --z-modal:   500;
  --z-toast:   600;

  /* ── Transitions ────────────────────────── */
  --transition-fast:   100ms ease;
  --transition-base:   200ms ease;
  --transition-slow:   350ms ease;
  --transition-spring: 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 3. Typography

### Font Stack

```css
/* Display / Headings — DM Sans: geometric, authoritative, excellent at large sizes */
--font-display: 'DM Sans', 'Segoe UI', system-ui, sans-serif;

/* Body / UI — IBM Plex Sans: engineered, technical, exceptional legibility */
--font-body: 'IBM Plex Sans', 'Segoe UI', system-ui, sans-serif;

/* Monospace — for LPNs, barcodes, SKU codes, scan IDs */
--font-mono: 'IBM Plex Mono', 'Courier New', monospace;
```

**Why these fonts:**
- **DM Sans** has a distinctly purposeful, non-corporate feel at headline sizes. Pairs exceptionally with data-dense content.
- **IBM Plex Sans** was designed for technical interfaces. It renders sharply at small sizes on low-DPI screens (common on industrial handhelds). Its FR/EN bilingual character support is complete.
- **IBM Plex Mono** for codes and identifiers: visually distinguishes machine-readable data from prose text at a glance.

### Type Scale

```css
/* Fluid type scale — clamps between mobile and desktop */
--text-xs:   0.75rem;   /* 12px — labels, captions, metadata */
--text-sm:   0.875rem;  /* 14px — secondary body, table cells */
--text-base: 1rem;      /* 16px — primary body */
--text-lg:   1.125rem;  /* 18px — emphasized body, card titles */
--text-xl:   1.25rem;   /* 20px — section headings */
--text-2xl:  1.5rem;    /* 24px — page headings */
--text-3xl:  1.875rem;  /* 30px — dashboard KPI numbers */
--text-4xl:  2.25rem;   /* 36px — large KPIs, hero numbers */
--text-5xl:  3rem;      /* 48px — scan feedback numbers */

/* Line heights */
--leading-tight:  1.25;
--leading-snug:   1.375;
--leading-normal: 1.5;
--leading-relaxed:1.625;

/* Font weights */
--weight-regular: 400;
--weight-medium:  500;
--weight-semibold:600;
--weight-bold:    700;
```

### Handheld-Specific Type Rules

On devices with screen width < 480px (handheld scanners):
- Minimum body text: `--text-lg` (18px). Never smaller.
- Minimum touch target label: `--text-xl` (20px).
- SKU/LPN codes: `--font-mono`, `--text-2xl`, `--weight-bold`.
- Quantity confirmations: `--text-5xl`, `--weight-bold`, centered.
- Error messages: `--text-xl`, `--color-danger-500`, `--weight-semibold`.

---

## 4. Color System

### Status Color Usage — Strict Rules

| Status | Background | Text | Border | Use For |
|--------|-----------|------|--------|---------|
| Success | `--color-success-100` | `--color-success-700` | `--color-success-500` | Scan confirmed, task complete, shipment departed |
| Warning | `--color-warning-100` | `--color-warning-700` | `--color-warning-500` | Approaching SLA, low stock, pending QC |
| Danger | `--color-danger-100` | `--color-danger-700` | `--color-danger-500` | Scan mismatch, short pick, expired lot, critical alert |
| Info | `--color-accent-100` | `--color-accent-600` | `--color-accent-500` | Directed instruction, tip, system info |
| Neutral | `--color-neutral-100` | `--color-neutral-700` | `--color-neutral-300` | Inactive, historical, not-started |

### Inventory Status Colors (Pill/Badge)

```
Available     → success-500 background  (green)
Allocated     → accent-500 background   (blue)
On Hold       → warning-500 background  (amber)
Quarantine    → danger-500 background   (red)
In Transit    → brand-500 background    (navy)
Expired       → neutral-600 background  (gray)
Damaged       → danger-700 background   (dark red)
```

### Order Status Colors

```
Received      → neutral-400   (gray)
Waved         → brand-400     (light navy)
Picking       → accent-400    (light blue) — animate pulse
Packing       → warning-400   (amber)
Staged        → success-300   (light green)
Shipped       → success-600   (mid green)
Exception     → danger-500    (red) — animate pulse
```

---

## 5. Spacing & Layout Grid

### Grid System

**Desktop Dashboard:** 12-column grid, 24px gutters, max-width 1440px, centered.  
**Tablet (Pack Station / Supervisor):** 8-column grid, 20px gutters.  
**Handheld PWA:** Single column, full width, 16px horizontal padding.  

### Layout Zones — Desktop

```
┌─────────────────────────────────────────────────────┐
│  Topbar (64px)                                       │
├──────────────┬──────────────────────────────────────┤
│              │                                       │
│  Sidebar     │   Main Content Area                   │
│  (240px)     │   (fluid)                             │
│              │                                       │
│  collapsed:  │                                       │
│  (64px)      │                                       │
└──────────────┴──────────────────────────────────────┘
```

### Layout Zones — Handheld PWA

```
┌─────────────────────┐
│  Context Bar (56px) │  ← Current task, LPN, order ID
├─────────────────────┤
│                     │
│  Primary Content    │  ← The ONE thing to do now
│  (flex-grow)        │
│                     │
├─────────────────────┤
│  Action Bar (80px)  │  ← Primary CTA, secondary action
└─────────────────────┘
```

The handheld layout is **always three zones**. The context bar tells them where they are. The primary content tells them what to do. The action bar lets them do it or report a problem.

---

## 6. Component Library

All components live in `src/components/ui/`. Each component is:
- Typed with TypeScript
- i18n-ready (no hardcoded strings — all text via `useTranslation()`)
- Dark mode aware (tokens only, no manual `dark:` overrides except where necessary)
- ARIA compliant
- Tested with Storybook + Chromatic visual regression

### Button

```tsx
// Variants: primary | secondary | ghost | danger | success
// Sizes: sm | md | lg | xl (xl = handheld touch target, min 56px height)

<Button
  variant="primary"
  size="xl"
  loading={isSubmitting}
  leftIcon={<CheckIcon />}
  fullWidth          // always fullWidth on handheld
>
  {t('common.confirm')}
</Button>
```

**Touch target rule:** All interactive elements on handheld must be minimum `56px` height × `full width`. Never stack two buttons vertically with less than `16px` gap.

### ScanInput

The most critical component in the floor PWA. Receives input from physical scanner (keyboard wedge) or soft keyboard.

```tsx
<ScanInput
  label={t('receiving.scan_barcode')}
  onScan={(value) => handleScan(value)}
  onError={(err) => showScanError(err)}
  autoFocus
  playSound           // plays success/error tone via Web Audio API
  haptic              // navigator.vibrate() on mobile
  expectedFormat="LPN | SKU | SSCC"
  placeholder="___________________________"
/>
```

Visual states:
- **Idle:** Dark border, blinking cursor, subtle pulse animation on border
- **Scanning:** Border turns blue, spinner
- **Success:** Border turns green, checkmark icon, 300ms hold then reset
- **Error:** Border turns red, shake animation, error message below, stays red until next scan attempt

### StatusBadge

```tsx
<StatusBadge status="picking" size="sm" animated />
// status: 'available' | 'allocated' | 'on-hold' | 'quarantine' |
//         'in-transit' | 'expired' | 'damaged' |
//         'received' | 'waved' | 'picking' | 'packing' |
//         'staged' | 'shipped' | 'exception'
```

### KPICard

Desktop dashboard card for key metrics.

```tsx
<KPICard
  label={t('dashboard.orders_shipped_today')}
  value={847}
  delta={+12.4}         // % vs yesterday
  deltaLabel={t('dashboard.vs_yesterday')}
  icon={<TruckIcon />}
  trend={sparklineData} // 7-day trend data
  status="success"      // colors the card accent
/>
```

### DataTable

```tsx
<DataTable
  columns={columns}
  data={orders}
  loading={isLoading}
  sortable
  filterable
  selectable
  onRowClick={(row) => navigate(`/orders/${row.id}`)}
  emptyState={<EmptyState icon="inbox" message={t('orders.none_found')} />}
  stickyHeader
  virtualRows  // react-virtual for large datasets
/>
```

### ScanFeedback (Handheld full-screen feedback)

For actions where confirmation needs to be unmistakable:

```tsx
<ScanFeedback
  type="success"        // 'success' | 'error' | 'warning'
  title={t('stow.location_confirmed')}
  subtitle="A-07-B-03"
  icon={<MapPinIcon />}
  autoDismiss={1500}    // ms, then advance to next step
/>
```

Full-screen takeover. Green background, white 4xl text, large icon. Unmistakable. Auto-dismisses and advances.

### Toast / Alert System

```tsx
// Programmatic toasts from anywhere
toast.success(t('shipment.departed'))
toast.error(t('scan.mismatch'), { duration: 0 }) // stays until dismissed
toast.warning(t('lot.expiring_soon', { days: 14 }))
```

Toasts appear bottom-center on mobile, top-right on desktop. Maximum 3 visible at once. Stack from bottom up.

### Modal / Drawer

- **Modal:** Confirmation dialogs, exception forms, supervisor overrides. Max-width 480px on desktop.
- **Drawer:** Detail panels that slide in from the right (desktop) or bottom (mobile). Used for order details, inventory lookup, LPN history.

### Charts (Recharts)

All charts use the NexoFlow color palette via CSS variables. Chart components:
- `<ThroughputLineChart>` — picks/hour over time, area variant
- `<OrderFunnelChart>` — orders by status, horizontal bar
- `<AccuracyGauge>` — inventory accuracy %, circular gauge
- `<CapacityHeatmap>` — warehouse location utilization heatmap grid
- `<WaveProgressBar>` — wave completion, animated segmented bar
- `<SparkLine>` — 7/30-day trend inline in KPI cards

---

## 7. Iconography

**Icon Library:** `lucide-react` — clean, consistent, 24px grid, 1.5px stroke.  
**Do not mix icon libraries.** Every icon in the product comes from Lucide.

### Domain Icon Mapping

```
Receiving:      PackageOpen
Stow/Putaway:   ArrowDownToLine
Picking:        ShoppingCart → Boxes
Packing:        Box
Shipping:       Truck
Returns:        RotateCcw
Inventory:      Layers
Counting:       ClipboardCheck
LPN:            QrCode
Label/Print:    Printer
Scanner:        ScanLine
Location:       MapPin
Exception:      AlertTriangle
Hold/Quarantine:Lock
Lot:            FlaskConical
Expiry:         CalendarX2
Carrier:        Package2
Dock:           Warehouse
Dashboard:      LayoutDashboard
Analytics:      TrendingUp
AI Co-Pilot:    Sparkles
Settings:       SlidersHorizontal
Users:          Users2
Tenant:         Building2
```

### Icon Sizes

```
16px (--icon-xs):  inline text, table cells, dense lists
20px (--icon-sm):  button icons, form labels, nav items
24px (--icon-md):  card headers, section icons (default)
32px (--icon-lg):  empty states, feature icons
48px (--icon-xl):  handheld action prompts, scan feedback
64px (--icon-2xl): onboarding, full-screen feedback states
```

---

## 8. Motion & Animation

### Principles
- Animations must be functional — they communicate state change, not decoration.
- Duration: fast (100ms) for micro-feedback, medium (200–350ms) for transitions, never over 500ms for UI.
- Respect `prefers-reduced-motion` — all animations behind `@media (prefers-reduced-motion: no-preference)`.

### Animation Catalogue

```css
/* Scan success pulse — brief green flash */
@keyframes scan-success {
  0%   { background-color: var(--color-success-500); transform: scale(1.02); }
  100% { background-color: transparent; transform: scale(1); }
}

/* Scan error shake */
@keyframes scan-error {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-8px); }
  40%, 80% { transform: translateX(8px); }
}
.scan-error { animation: scan-error 400ms ease; }

/* Status badge pulse for active states (picking, exception) */
@keyframes status-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.6; }
}
.badge-animated { animation: status-pulse 2s ease infinite; }

/* KPI card number count-up — handled via useCountUp hook */

/* Skeleton loading shimmer */
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.skeleton {
  background: linear-gradient(90deg,
    var(--color-neutral-200) 25%,
    var(--color-neutral-100) 50%,
    var(--color-neutral-200) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease infinite;
}

/* Page transition — slide in from right */
.page-enter  { opacity: 0; transform: translateX(20px); }
.page-active { opacity: 1; transform: translateX(0); transition: all 200ms ease; }
```

---

## 9. PWA Floor Interface — Handheld UX

### Screen Architecture

The floor PWA is a guided, linear workflow engine. Associates do not browse or navigate freely — the system tells them exactly where to go next. Navigation is forward/back within a task, not free exploration.

```
Login Screen
    └── Task Queue (home — list of assigned tasks)
            ├── Receive Task Flow
            │     ├── Scan PO / ASN
            │     ├── Scan Item (loop per line)
            │     ├── Enter Lot / Expiry (if applicable)
            │     ├── QC Gate (if applicable)
            │     └── Print Label → Complete
            ├── Stow Task Flow
            │     ├── Scan LPN
            │     ├── Navigate to Location (map/aisle guide)
            │     ├── Scan Location
            │     └── Confirm → Complete
            ├── Pick Task Flow
            │     ├── Navigate to Location
            │     ├── Scan Location
            │     ├── Scan Item / LPN
            │     ├── Confirm Quantity
            │     └── Scan Destination Container → Next Pick
            ├── Pack Task Flow
            │     ├── Scan Order / Tote
            │     ├── Scan each Item (verify)
            │     ├── Select Carton Type
            │     └── Close Carton → Print Shipping Label
            ├── Count Task Flow
            │     ├── Navigate to Location
            │     ├── Scan Location
            │     ├── Enter Count per SKU
            │     └── Submit → Next Location
            └── Exception Reporting
                  ├── Report Damage
                  ├── Item Out of Location
                  └── Short Pick Declaration
```

### Handheld Screen Design Rules

1. **One action per screen.** The screen asks for exactly one thing: scan this, confirm this quantity, go to this location.
2. **The primary action is always at the bottom.** Associates hold devices at waist height; thumbs reach the bottom.
3. **Location display:** Bold, monospace, `--text-4xl`. Aisle-Bay-Level-Position on separate lines if needed.
4. **SKU/Description:** `--text-xl`, two lines max, truncate with ellipsis.
5. **Quantity confirmation:** Numeric keypad overlay (custom, not native keyboard). Large digit display `--text-5xl`.
6. **Progress indicator:** Subtle linear progress bar at top of screen showing current task completion (e.g., 3 of 12 picks).
7. **Exception button:** Always accessible via secondary action — never hidden. Red outline button or "!" icon in top-right corner.
8. **Logout:** Accessible from task queue home only — not during active tasks to prevent accidental logout.

### Scan Sound Design

```javascript
// src/utils/audio.ts
// Web Audio API — no audio files needed, generated tones

export const playSuccess = () => {
  const ctx = new AudioContext();
  const osc = ctx.createOscillator();
  osc.frequency.setValueAtTime(880, ctx.currentTime);      // A5
  osc.frequency.setValueAtTime(1047, ctx.currentTime + 0.1); // C6
  osc.connect(ctx.destination);
  osc.start(); osc.stop(ctx.currentTime + 0.2);
};

export const playError = () => {
  const ctx = new AudioContext();
  const osc = ctx.createOscillator();
  osc.type = 'sawtooth';
  osc.frequency.setValueAtTime(200, ctx.currentTime);
  osc.frequency.setValueAtTime(150, ctx.currentTime + 0.15);
  osc.connect(ctx.destination);
  osc.start(); osc.stop(ctx.currentTime + 0.3);
};
```

Sounds are generated via Web Audio API (no file dependencies). Associates can disable sounds in profile preferences. The sounds are distinct enough to understand without looking at the screen.

---

## 10. Desktop Dashboard Interface

### Sidebar Navigation

The sidebar is navy (`--color-brand-800`), with white text. It collapses to icon-only mode (64px) to maximize content area.

```
┌─────────────────────────┐
│  ⬡ NexoFlow             │  Logo + collapse toggle
├─────────────────────────┤
│  [Dashboard icon]       │  Operations Overview
│  [Package icon]         │  Receiving
│  [Arrow icon]           │  Stow / Putaway
│  [Cart icon]            │  Picking
│  [Box icon]             │  Packing
│  [Truck icon]           │  Shipping
│  [Rotate icon]          │  Returns
├── ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤
│  [Layers icon]          │  Inventory
│  [Clipboard icon]       │  Counting
│  [TrendingUp icon]      │  Analytics
├── ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤
│  [Sparkles icon]        │  AI Co-Pilot
├── ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤
│  [Settings icon]        │  Settings
│  [User icon]            │  Profile
└─────────────────────────┘
```

Active nav item: white background with 2px left border in `--color-accent-500`. Non-active: white/70 opacity, no border.

### Operations Overview Dashboard Layout

```
┌────────┬────────┬────────┬────────┐
│ KPI 1  │ KPI 2  │ KPI 3  │ KPI 4  │  Row 1: 4 KPI cards (orders/hr, accuracy, shipped today, exceptions)
└────────┴────────┴────────┴────────┘
┌───────────────────────┬────────────┐
│ Order Funnel Chart    │ Wave       │  Row 2: funnel (8 cols) + wave progress (4 cols)
│ (8 cols)              │ Progress   │
│                       │ (4 cols)   │
└───────────────────────┴────────────┘
┌────────────┬──────────────────────┐
│ Active     │ Exception Queue      │  Row 3: associate activity (4 cols) + exceptions (8 cols)
│ Associates │ (real-time list)     │
│ (4 cols)   │                      │
└────────────┴──────────────────────┘
┌──────────────────────────────────┐
│ Throughput Line Chart (12 cols)  │  Row 4: full-width throughput trend
└──────────────────────────────────┘
```

### Topbar

Height: 64px. White background, bottom border `--border-default`.

Left: Breadcrumb navigation (page context).  
Center: Global search (Cmd+K / Ctrl+K) — searches orders, LPNs, SKUs, locations.  
Right: [Language toggle FR/EN] [Notification bell with badge] [User avatar + name + role dropdown]

---

## 11. Responsive Breakpoints

```css
/* Tailwind config extension */
screens: {
  'handheld': '320px',   // Zebra TC55, MC32 — portrait mode
  'sm':       '480px',   // Large handheld, compact phones
  'md':       '768px',   // Tablet — pack stations, supervisor
  'lg':       '1024px',  // Laptop — operations manager
  'xl':       '1280px',  // Desktop — standard
  '2xl':      '1440px',  // Wide desktop — director dashboard
  '3xl':      '1920px',  // 1080p — wall-mounted displays
}
```

### Layout Behavior by Breakpoint

| Breakpoint | Sidebar | Navigation | KPI Grid | Charts |
|---|---|---|---|---|
| handheld (320px) | Hidden — bottom tab bar | Bottom tabs (5 max) | 1 col | Hidden |
| sm (480px) | Hidden — bottom tab bar | Bottom tabs | 1 col | Simplified |
| md (768px) | Collapsed icon-only (64px) | Sidebar | 2 col | Compact |
| lg (1024px) | Expanded (240px) | Sidebar | 2 col | Full |
| xl (1280px) | Expanded (240px) | Sidebar | 4 col | Full |
| 2xl (1440px) | Expanded (240px) | Sidebar | 4 col | Full + density |

---

## 12. Accessibility (WCAG 2.1 AA)

### Requirements

- **Color contrast:** Minimum 4.5:1 for body text, 3:1 for large text and UI components. Status colors meet AA against both white and dark backgrounds.
- **Focus indicators:** All interactive elements have a visible focus ring: `outline: 2px solid var(--border-focus); outline-offset: 2px;`. Never `outline: none` without an alternative.
- **Touch targets:** Minimum 44×44px per WCAG 2.5.8 (we exceed this at 56px minimum for floor UI).
- **Screen reader support:** All icons paired with `aria-label` or visually hidden text. Dynamic content updates via `aria-live` regions (scan results, toast notifications).
- **Keyboard navigation:** Complete keyboard navigation for all desktop workflows. Tab order follows logical reading order.
- **Forms:** All inputs have associated `<label>` elements. Error messages linked via `aria-describedby`. Required fields indicated with both asterisk and `aria-required`.
- **Motion:** All animations wrapped in `@media (prefers-reduced-motion: no-preference)`. Reduced motion provides instant state change without animation.

### ARIA Live Regions

```tsx
// Scan result — assertive (interrupts screen reader immediately)
<div aria-live="assertive" aria-atomic="true" className="sr-only">
  {scanResult}
</div>

// Toast notifications — polite (waits for current announcement)
<div aria-live="polite" aria-atomic="false">
  {toasts}
</div>
```

---

## 13. Bilingual UI Design (FR/EN)

### String Externalization

**Zero hardcoded strings anywhere in component code.** Every user-facing string is a translation key.

```tsx
// ❌ Never
<Button>Confirm Receipt</Button>

// ✅ Always
const { t } = useTranslation('receiving');
<Button>{t('confirm_receipt')}</Button>
```

### Translation File Structure

```
src/
  locales/
    en-CA/
      common.json         ← buttons, status labels, pagination, errors
      receiving.json
      picking.json
      packing.json
      shipping.json
      returns.json
      inventory.json
      counting.json
      analytics.json
      admin.json
      ai.json
    fr-CA/
      common.json         ← (mirrors en-CA structure exactly)
      receiving.json
      ... (all same files)
```

### French String Design Considerations

French strings are typically 20–40% longer than English equivalents. Design all components to handle this gracefully:

```json
// en-CA: "Confirm Receipt" (16 chars)
// fr-CA: "Confirmer la réception" (22 chars) — 37% longer

// en-CA: "Directed Putaway"
// fr-CA: "Rangement dirigé"
```

**Rules for FR/EN resilient components:**
1. Buttons must support text wrapping on two lines at handheld widths (never `white-space: nowrap` on buttons unless icon-only).
2. Table column headers: allow up to 2 lines with `hyphens: auto` for long French compound words.
3. KPI card labels: allow 3 lines, font-size scales down to `--text-xs` if label exceeds 2 lines.
4. Navigation items: sidebar nav collapses to icon-only at medium screen anyway — label length is only an issue on desktop expanded mode.
5. Test every new component against the `fr-CA` locale before marking as done.

### Language Toggle

Available in topbar (desktop) and profile menu (mobile). Switches instantly without page reload via i18next language change.

```tsx
<LanguageToggle
  options={[
    { code: 'en-CA', label: 'EN', fullLabel: 'English' },
    { code: 'fr-CA', label: 'FR', fullLabel: 'Français' },
  ]}
  onChange={(lang) => i18n.changeLanguage(lang)}
/>
```

The toggle persists language choice to user profile API so the preference follows the user across devices.

---

## 14. Dark Mode

Dark mode is supported as a tenant-configurable option and user preference override. The floor PWA defaults to **dark mode** — high contrast dark theme performs better in variable warehouse lighting conditions.

### Dark Mode Tokens

```css
[data-theme="dark"] {
  --surface-page:       #0f1923;
  --surface-card:       #1a2535;
  --surface-card-hover: #1f2e42;
  --surface-sidebar:    #0d1829;

  --text-primary:   #f1f5f9;
  --text-secondary: #94a3b8;
  --text-tertiary:  #64748b;

  --border-default: #2d3d54;
  --border-strong:  #3d5068;

  /* Shadows deeper in dark mode */
  --shadow-sm:  0 1px 3px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md:  0 4px 6px rgba(0,0,0,0.35), 0 2px 4px rgba(0,0,0,0.3);
}
```

Semantic status colors remain identical between light and dark mode — no adjustment needed for success/warning/danger as they are already contrast-safe.

---

## 15. Page & Screen Catalogue

### Floor PWA Screens

| Screen | Route | Description |
|--------|-------|-------------|
| Login | `/login` | PIN or username + password. Large keypad for PIN mode. |
| Task Queue | `/tasks` | List of assigned tasks, grouped by type. Pull to refresh. |
| Receive — Scan PO | `/receive/scan-po` | Scan PO barcode or search by PO number |
| Receive — Item Loop | `/receive/:poId/item` | Scan item, enter quantity, lot, expiry |
| Receive — QC Gate | `/receive/:poId/qc` | Pass/Fail/Hold with reason codes |
| Receive — Complete | `/receive/:poId/done` | Summary + print labels |
| Stow — Scan LPN | `/stow/scan-lpn` | Scan the LPN to stow |
| Stow — Navigate | `/stow/:lpnId/navigate` | Display directed location with aisle guide |
| Stow — Confirm | `/stow/:lpnId/confirm` | Scan location barcode to confirm stow |
| Pick — Navigate | `/pick/:taskId/navigate` | Display location to go to |
| Pick — Confirm Location | `/pick/:taskId/location` | Scan location |
| Pick — Scan Item | `/pick/:taskId/item` | Scan item/LPN |
| Pick — Quantity | `/pick/:taskId/qty` | Confirm/enter quantity |
| Pack — Scan Tote | `/pack/scan-tote` | Scan incoming tote/batch |
| Pack — Verify Item | `/pack/:orderId/verify` | Scan each item to verify against order |
| Pack — Select Carton | `/pack/:orderId/carton` | Choose carton type |
| Pack — Complete | `/pack/:orderId/done` | Print shipping label |
| Count — Scan Location | `/count/:taskId/location` | Scan location to count |
| Count — Enter Quantity | `/count/:taskId/qty` | Enter counts per SKU |
| Exception Report | `/exception` | Report damage, out-of-location, short pick |
| LPN Lookup | `/lookup/lpn` | Utility: look up any LPN location and history |

### Desktop Screens

| Screen | Route | Description |
|--------|-------|-------------|
| Operations Overview | `/dashboard` | Real-time KPIs, wave progress, exceptions |
| Orders | `/orders` | Order list with filters, status, SLA indicators |
| Order Detail | `/orders/:id` | Full order detail, line items, containers, events |
| Inbound | `/inbound` | PO/ASN list, receiving progress |
| Inventory | `/inventory` | SKU inventory positions, lot details |
| Location Map | `/locations` | Warehouse location grid, capacity heatmap |
| Wave Planner | `/waves` | Wave list, create/release waves |
| Picking Dashboard | `/picking` | Active picks, PPH, associate activity |
| Shipping | `/shipping` | Staged shipments, carrier manifest, departures |
| Returns | `/returns` | RMA list, grading queue, disposition workflow |
| Cycle Counting | `/counting` | Count task list, variance review |
| Analytics | `/analytics` | Throughput, accuracy, cycle time, forecasting |
| AI Co-Pilot | `/ai` | Conversational assistant + insight cards |
| Label Designer | `/labels` | ZPL label template editor |
| Admin — Tenant Config | `/admin/config` | Feature flags, storage rules, business rules |
| Admin — Users | `/admin/users` | User management, roles, device assignments |
| Admin — Integrations | `/admin/integrations` | EDI, carrier, ERP connector configuration |
| Admin — Printers | `/admin/printers` | Printer fleet, queue management |

---

## 16. State Design — Loading, Empty, Error

### Loading States

- **Page load:** Full-page skeleton (not spinner). Every KPI card, table, and chart has a skeleton variant that matches its shape exactly.
- **Data refresh:** Stale content visible with 30% opacity overlay + spinner. Never blank the page on refresh.
- **Action loading:** Button shows spinner + disabled state. Never block the entire screen for a button action.
- **Scan processing:** `ScanInput` internal loading state — 200ms max before visual feedback.

### Empty States

Every empty state has: an icon (64px), a heading, a body sentence, and a primary CTA.

```tsx
<EmptyState
  icon={<PackageOpenIcon size={64} />}
  heading={t('receiving.no_pos_heading')}
  body={t('receiving.no_pos_body')}
  action={<Button onClick={createPO}>{t('receiving.create_po')}</Button>}
/>
```

Illustrations for empty states: simple geometric SVGs using brand colors. Not photographs, not complex illustrations that add weight.

### Error States

- **Network error:** Persistent banner at top of page. Auto-retries with exponential backoff. Shows "Reconnecting…" status.
- **Scan mismatch:** Red shake animation on `ScanInput`. Large red message below. Never auto-advance on error.
- **Form validation:** Inline error below each field. Summary error banner above form for submit-time errors.
- **404:** Simple centered message with back navigation.
- **500:** "Something went wrong" with error ID (for support). Never expose stack traces.

---

## 17. ZPL Label Design Guidelines

### Label Template Anatomy

```
┌─────────────────────────────────┐
│  NEXOFLOW    [Tenant Logo Zone] │  ← 4mm header
├─────────────────────────────────┤
│  SKU: 4501-BLK-M                │  ← Bold, large
│  Black Polo Shirt — Medium      │  ← Description
├─────────────────────────────────┤
│  LOT: 2024-B42    EXP: 12/2026  │  ← Lot / Expiry row
├─────────────────────────────────┤
│  QTY: 24          RCV: 2025-03  │  ← Quantity / Receive date
├─────────────────────────────────┤
│  ████ ████ ████ ████ ████ ████  │  ← Code 128 barcode (LPN)
│  00123456789012345678           │  ← Human-readable LPN
└─────────────────────────────────┘
```

### ZPL Template Variables

Every field in a label template is a `{{variable}}` resolved at print time:

```
{{lpn}}           License Plate Number
{{sku}}           Item SKU code
{{description}}   Item description (tenant language)
{{description_fr}} French description (if bilingual label)
{{lot}}           Lot number
{{expiry}}        Expiration date (DD/MM/YYYY)
{{mfg_date}}      Manufacture date
{{qty}}           Quantity
{{rcv_date}}      Receive date
{{po_number}}     Purchase Order number
{{location}}      Current location code
{{tenant_name}}   Tenant name
{{operator_id}}   Receiving operator
{{barcode_lpn}}   ZPL ^BC barcode command block
{{barcode_sku}}   ZPL ^BQ (QR) or ^BC barcode block
```

### ZPL Print Pipeline

```
Label Request → Template Resolver → Variable Injection
    → ZPL Generator → Print Queue (Redis)
    → Printer Dispatcher (Celery worker)
    → TCP/IP socket to Zebra printer
    → Print confirmation callback
```

Printers are registered by IP + port per location. Printer health checked every 60 seconds. Failed print jobs retry 3× then alert supervisor.

---

## 18. Design Tokens Export

Tokens are auto-exported to three formats on every design system build:

```bash
# CSS custom properties (consumed by React app)
dist/tokens/tokens.css

# JSON (consumed by Storybook, design tools, documentation)
dist/tokens/tokens.json

# Tailwind config extension (merged into tailwind.config.ts)
dist/tokens/tailwind-tokens.js
```

The single `tokens.css` file is the canonical source. The JSON and Tailwind exports are derived from it via a build script (`scripts/export-tokens.ts`). Never edit the derived files directly.

---

*End of DESIGN.md*
