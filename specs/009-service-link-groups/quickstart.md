# Quickstart / Validation Guide: Tile Link Groups

**Feature**: [spec.md](spec.md) · **Phase 1** · **Date**: 2026-08-31

Validation/run guide for tile grouping (renamed from "services"), the hardcoded
"Bookmarks" heading, the full "Tiles" rebrand, and external-service tile positioning.
Schema and rendering details live in
[contracts/config-contract.md](contracts/config-contract.md),
[contracts/ui-contract.md](contracts/ui-contract.md), and
[data-model.md](data-model.md).

## Prerequisites

- Python 3.14 + [`uv`](https://docs.astral.sh/uv/) (and optionally Node/pnpm for static
  assets) per the repo README.
- A checkout with tests runnable: `uv run pytest`.

## Setup / Run

```bash
uv run pytest            # full test suite (unit + integration + contract)
```

For a manual smoke test, run the app against the example config:

```bash
uv run python -c "from app.config import load_dashboard_from_file; \
print(load_dashboard_from_file('config/example.yaml'))"
```

## Migration Note (breaking change)

This feature renames the config keys `services`→`tiles` and `service_groups`→
`tile_groups` (and `service_groups[].services`→`tile_groups[].tiles`). It is a **breaking
change**: the legacy `services`/`service_groups` keys are not supported, and existing
configs must be renamed by the owner (Clarification Q1 → A). The example config below is
already migrated.

---

## Validation Scenarios

### V1 — Flat `tiles` list renders (SC-001, FR-001)

- **Setup**: config with a flat `tiles` list (the migrated `example.yaml`).
- **Run**: load the homepage.
- **Expect**: all flat tiles render in the main area as `app-tile tile` links; no group
  headers introduced.

### V2 — `tile_groups` render with headers, always visible (SC-002, FR-010)

- **Setup**: config that places tiles under two or more `tile_groups` entries.
- **Run**: load the homepage.
- **Expect**:
  - Each group renders a `<h3 class="group-title">` header showing its `name`.
  - All groups and all tiles are fully visible with **no** collapse/expand control and
    no hidden content.
  - Groups appear in declared order; every tile appears only in its own group.

### V3 — Group icons render (SC-002 / FR-005)

- **Setup**: give one `tile_groups` entry an `icon` (a valid `http(s)` URL), another none.
- **Run**: load the homepage.
- **Expect**: the group with an icon shows it beside the group name; the group without an
  icon shows the name alone (no broken/empty icon element).

### V4 — Mixed flat + grouped renders (FR-006)

- **Setup**: config with both a flat `tiles` list and one or more `tile_groups`.
- **Run**: load the homepage.
- **Expect**: flat tiles render first (unlabeled); each named group renders after, in
  order, with a header. No error.

### V5 — "Bookmarks" heading (FR-011)

- **Setup**: config with at least one `bookmark_groups` entry.
- **Run**: load the homepage.
- **Expect**: a heading reading "Bookmarks" renders above the bookmark accordion; it is
  hardcoded and unaffected by config.

### V6 — Rebrand to "Tiles" everywhere (FR-012, FR-001 / SC-006)

- **Setup**: any migrated config.
- **Run**: load the homepage; also grep the code, CSS, tests, and docs.
- **Expect**:
  - The main section is labeled "Tiles" (`aria-label="Tiles"`), not "Services".
  - Config keys are `tiles`/`tile_groups`; Python types `Tile`/`TileGroup`; CSS classes
    `tile-*` (no `service-*`).
  - README / config comments use "tiles".
  - A repo-wide `grep -rni "service"` (excluding git history and unrelated content such as
    a bookmark label "National Benefits Services") finds no applicable "services"
    reference for the former section.

### V7 — Legacy `services` is not supported (FR-001 / US1 AS3)

- **Setup**: config that still uses the legacy `services` key (no `tiles`).
- **Run**: `load_dashboard_from_file`.
- **Expect**: no error, but **zero tiles** render (the legacy key is not recognized as
  tiles). Migration to `tiles` is required.

### V8 — Malformed `tile_groups` is rejected (FR-007 / SC-004)

- **Setup**: config with a `tile_groups` entry missing `name`, or whose `tiles` is not a
  list.
- **Run**: `load_dashboard_from_file` (or the in-browser editor save).
- **Expect**: a clear `ConfigValidationError`; nothing valid is lost.

### V9 — Tiles link to internal AND external services (FR-013 / SC-007)

- **Setup**: use the migrated `example.yaml`, which has at least one tile pointing to an
  internal homelab service and at least one pointing to an external service (e.g., an
  email provider's webmail or a cloud portal).
- **Run**: load the homepage; click the external tile.
- **Expect**: each tile (internal and external) opens its `http(s)` destination in a new
  tab; README/example comments state tiles may target either kind.

---

## Expected Test Coverage Pointers

- `tests/unit/test_schema.py` — `tiles`/`tile_groups` parsing + validation (V1/V8).
- `tests/unit/test_views_tiles.py` — (renamed from `test_views_services.py`) flat +
  grouped rendering, group headers, "Bookmarks" heading (V2/V3/V5/V6).
- `tests/integration/test_homepage_tiles.py` — (renamed from
  `test_homepage_services.py`) homepage with flat + grouped tiles, "Tiles"/"Bookmarks"
  verbiage (V2/V4/V5/V6/V9).
- `tests/integration/test_mobile_layout.py` — grid classes preserved, `tile-*` classes,
  group header presence (V2).
- `tests/contract/test_config_schema.py` — `tiles` + `tile_groups` allowed keys; legacy
  `services` yields no tiles (V1/V7).
