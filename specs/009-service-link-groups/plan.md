# Implementation Plan: Tile Link Groups (Services Rebranded as "Tiles")

**Branch**: `009-service-link-groups` | **Date**: 2026-08-31 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/009-service-link-groups/spec.md`

## Summary

Rebrand the dashboard's link section from "services" to **"tiles"** everywhere (config
keys, Python identifiers, CSS classes, tests, docs, and UI labels), and let tiles be
organized into named **tile groups** that are always visible (no collapse, unlike the
bookmarked accordion). A hardcoded "Bookmarks" heading appears above the bookmark
accordion. This is a **breaking change** (Clarification Q1 → A): the former
`services`/`service_groups` keys are renamed to `tiles`/`tile_groups`, and the legacy
keys are NOT supported — existing configs must be updated. Tiles are positioned as
general-purpose links usable for both internal homelab services and external services
(e.g., webmail, cloud account portals).

## Technical Context

**Language/Version**: Python 3.14 backend (unchanged, Flask 3.x). Server-rendered Jinja2
with Bootstrap 5.3; one small vanilla `app.js` for dark mode. No frontend build step.

**Primary Dependencies**: None new. Reuses PyYAML (`yaml.safe_load`), the existing
`parse_dashboard` schema, `ConfigLoader` hot-reload, and the existing
`bookmark_groups` grouping/rendering pattern as the model for tile groups.

**Storage**: No database. Single YAML config file on disk (already-loaded `CONFIG_PATH`).
The change renames the `services` key to `tiles`, adds a `tile_groups` top-level key
alongside `tiles`, `bookmark_groups`, and `editor`/`edit_config` flags, and renames the
`service_groups` concept accordingly.

**Testing**: pytest (`uv run pytest`) — unit + integration + contract. Unit: schema
parsing of the renamed `tiles` and of `tile_groups` (missing name / non-list / icon),
and validation rejection. Integration: flat `tiles` render; grouped tiles render under
labeled headers with no collapse control; the "Bookmarks" heading renders. Contract:
config is `tiles` + `tile_groups` + `bookmark_groups` + flags; the legacy `services`
key is NOT an allowed tile key.

**Target Platform**: Linux server (Docker host) serving the dashboard; modern browsers.

**Project Type**: web application (backend + frontend); a config + rendering enhancement
plus a repository-wide terminology rebrand (breaking rename).

**Performance Goals**: Preserve the existing target (homepage interactive under 2
seconds). Grouped rendering adds only template structure (no extra network/common cache
work), so it must not regress the existing target.

**Constraints**:
- **Breaking rename** (FR-001, Clarification Q1 → A): the config keys `services`→`tiles`
  and `service_groups`→`tile_groups` are renamed, along with every applicable internal
  identifier, CSS class, test, and doc. The legacy `services`/`service_groups` keys are
  NOT supported; existing configs must be updated.
- **No collapse for tile groups** (FR-010): tile group headers are plain headings, NOT
  Bootstrap accordion buttons and NOT collapsible; there is no saved open/closed state.
  Only the existing bookmark accordion remains collapsible.
- **"Bookmarks" header is hardcoded** (FR-011): rendered as fixed text above the bookmark
  accordion when `bookmark_groups` is non-empty; not configurable.
- **No applicable "services" remains** (FR-012): the term "tiles" is used consistently
  across every facet; only git history and unrelated content (e.g., a bookmark label such
  as "National Benefits Services") may retain "services".
- **Tiles are general-purpose links** (FR-013): may point to internal homelab services or
  external services (webmail, cloud portals); any valid `http(s)` URL opens in a new tab.
- **Injection-safe**: any tile/group name or icon rendered into the page is escaped and
  validated, consistent with the Security Requirements.

**Scale/Scope**: Single-owner homelab dashboard; one config file; one template page; a
repository-wide rename sweep.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Testability (IV)** — GATE. Tests MUST be written first (red-green) and alongside this
  change. The renamed `tiles`/`tile_groups` schema, the always-visible grouped rendering,
  the hardcoded "Bookmarks" heading, the breaking-rename rejection of the legacy
  `services` key, and the external-services positioning MUST all have tests.
  — *Covered by the Testing plan; expanded in Phase 1.*
- **Developer Experience (I)** — GATE. The change MUST NOT add friction to
  `uv run pytest` / local run / `pnpm provision`, and the breaking rename must be
  documented so existing owners can migrate. — *Satisfied: no new dependencies, no build
  step, no new runner; the rename is mechanical and documented in README/quickstart.*
- **Readability (II)** — GATE. New code MUST match the surrounding structure and
  conventions. Tile groups mirror the existing `bookmark_groups` parsing/rendering, and
  tile-group headers reuse the existing `.group-title` class. — *Satisfied by mirroring
  the established group pattern consistently under the new `tile*` vocabulary (Phase 1).*
- **Extensibility & Modularity (III)** — PASS. Tile grouping is additive config +
  rendering within the existing single-module layout; the rename is a one-time sweep.
  No new module boundaries are required.
- **YAGNI/Simplicity (V)** — PASS. The simplest design that satisfies grouping is a
  `tile_groups` list that mirrors `bookmark_groups`; no generic "section" abstraction, no
  drag-and-drop, no new storage. The rebrand is a mechanical rename with no new concepts.
- **Security Requirements** — GATE. Tile/group names and icons rendered into the page MUST
  be escaped/validated; external tile URLs remain validated `http(s)` URLs opened with
  `noopener noreferrer`; the feature adds no new network exposure, secrets, or write path.
  — *Satisfied by applying the existing escape/validate handling to the new vocabulary.*
  No complexity justification is required (Complexity Tracking intentionally empty).

*Post-Phase-1 re-check:* See "Post-Design Constitution Re-Check" below.

## Project Structure

### Documentation (this feature)

```text
specs/009-service-link-groups/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output: config syntax + rebrand scope + layout decisions
├── data-model.md        # Phase 1 output: Tile/TileGroup model + rendering model
├── quickstart.md        # Phase 1 output: how to run + verify the feature
├── contracts/           # Phase 1 output: config + UI contracts
└── tasks.md             # Phase 2 output (/speckit.tasks command - already created)
```

### Source Code (repository root)

```text
app/
├── __init__.py            # (no change) app factory, url test filter
├── model.py               # (modified) Service→Tile; add TileGroup (name, icon?, tiles)
│                          #   DashboardConfig: services→tiles; add tile_groups
├── schema.py              # (modified) _parse_service→_parse_tile; services→tiles;
│                          #   add _parse_tile_group + tile_groups; legacy services rejected
├── config.py              # (no change) ConfigLoader hot-reload picks up new key
├── views.py               # (modified) pass tiles + tile_groups to template
├── static/
│   └── app.css            # (modified) .service-* → .tile-*; reuse .group-title for headers
└── templates/
    ├── index.html         # (modified) render tile groups + "Bookmarks" heading;
    │                      #   aria-label/meta/comment → "Tiles"; class names → tile-*
    └── config.html        # (no change)

config/
└── example.yaml           # (modified) services→tiles; add a tile_groups example; add an
                           #   external-service tile; update comments to "tiles"

README.md                 # (modified) Services→Tiles documentation + migration note +
                           #   external-services positioning

tests/
├── unit/test_schema.py                # (modified) tiles/tile_groups parsing + validation
├── unit/test_views_services.py        # (renamed→test_views_tiles.py) grouped + flat rendering
├── integration/test_homepage_services.py  # (renamed→test_homepage_tiles.py) grouped/flat; "Tiles"
├── integration/test_mobile_layout.py  # (modified) keep col-grid contract; rename service-*→tile-*
└── contract/test_config_schema.py     # (modified) allowed keys: tiles+tile_groups; legacy rejected
```

**Structure Decision**: Keep the single-project Flask layout. Tile groups are a config +
rendering extension that exactly mirrors the existing `bookmark_groups` code path
(`model.py` → `schema.py` → `index.html`), and the rebrand is a mechanical per-file sweep
under the same structure — no reorganization is needed.

## Post-Design Constitution Re-Check

*Must be confirmed after Phase 1 (data-model, contracts, quickstart) is generated.*

- **Testability (IV)** — GATE. Design adds tests for: renamed `tiles` schema, `tile_groups`
  parsing/validation, always-visible grouped rendering (no collapse), the hardcoded
  "Bookmarks" heading, external-service tiles, and legacy `services` rejection.
  — *Confirmed in quickstart.md (V1–V7) and contracts.*
- **Developer Experience (I)** — GATE. No new deps/build; README migration note covers the
  breaking `tiles`/`tile_groups` rename. — *Confirmed.*
- **Readability (II)** — GATE. `Tile`/`TileGroup` mirror `BookmarkGroup`; `.group-title`
  reused; `_parse_tile_group` mirrors `_parse_group`. — *Confirmed in data-model.md.*
- **Extensibility & Modularity (III)** — PASS.
- **YAGNI/Simplicity (V)** — PASS.
- **Security Requirements** — GATE. Names/icons escaped/validated; external URLs validated
  `http(s)` opened with `noopener noreferrer`; no new exposure. — *Confirmed in contracts.*
- **Gate result**: PASS — no violations unjustified; no Complexity Tracking entry required.

## Complexity Tracking

> Intentionally empty — no Constitution violations require justification. Grouping reuses
> the established `bookmark_groups` pattern (PASS on III/V), the rebrand is a mechanical
> rename (no new concept), and no new dependency or build step is introduced.
