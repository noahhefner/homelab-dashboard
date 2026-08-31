# Research: Tile Link Groups (Services Rebranded as "Tiles")

**Feature**: [spec.md](spec.md) · **Phase 0** · **Date**: 2026-08-31

This document consolidates the key planning decisions needed before design. It resolves
the "NEEDS CLARIFICATION" points from the Technical Context against the **clarified**
spec (2026-08-31, which introduced a breaking full-repo rename and external-services
positioning). The prior backward-compatible/verbiage-only research is superseded.

## R1 — Config syntax for grouped tiles

- **Decision**: Grouped tiles are declared under a new `tile_groups` top-level key, each
  entry a mapping `{name, icon?, tiles: [...]}` where `tiles` is the list of tile entries
  using **the same `Tile` shape** as the flat `tiles` list. The flat list lives under a
  top-level `tiles` key. The old `services`/`service_groups` keys are removed.
- **Rationale**: Mirrors the established `bookmark_groups`/`bookmarks` pattern
  (`app/schema.py` `_parse_group`), minimizing new concepts and keeping one tile-entry
  shape everywhere (Principle II/III). Reuses a single `_parse_tile` for both flat and
  nested entries.
- **Alternatives considered**:
  - Hybrid grouping (flat `tiles` list with optional `group:` field per entry) — rejected:
    diverges from the `bookmark_groups` model, complicates ordering/rendering, and mixes
    concerns in one list.
  - A single `tiles` key whose entries may be either a tile or a `{group: ...}` wrapper —
    rejected: heterogeneous list is harder to validate and render.
  - Path: `tiles/<group>/<name>` dotted keys — rejected: not how this config works.

## R2 — Where ungrouped (flat) tiles render when tile groups exist

- **Decision**: Flat `tiles` render first in an unlabeled main-section grid; each
  `tile_groups` entry renders after it, in declared order. (Spec Edge Case: "ungrouped
  tiles, when grouped tile sections exist, appear in a default/unnamed section at a
  consistent location (e.g., top or after all groups — to be confirmed in planning)".)
- **Rationale**: Renders the simplest config (flat only) identically to today, and
  keeps the flat list visually primary. Consistent with the "flat is the foundation"
  framing of US1 and the existing template structure (`index.html` renders the flat list
  in `<main>` before the bookmarks `<aside>`).
- **Alternatives considered**: rendering groups first, then ungrouped at the end —
  rejected because it would move the flat (default) case below grouped content for mixed
  configs and complicate the existing template.

## R3 — Tile groups are always visible (no collapse)

- **Decision**: Tile group headers are plain `<h3 class="group-title">` headings, **not**
  Bootstrap accordion buttons. No collapse/expand control, no `data-bs-toggle`, no
  persisted open/closed state. Only the existing bookmark accordion remains collapsible
  (FR-010).
- **Rationale**: Explicit requirement (spec FR-010, US2 AS4, Edge Cases). The existing
  `.group-title` class in `app/static/app.css` (line 112) is currently unused and is
  reused for these headers — no new CSS concept needed (YAGNI).
- **Alternatives considered**: reusing the accordion with forced-open state — rejected
  (adds controls/state that must then be suppressed; violates the "never a collapse
  control" constraint).

## R4 — Applies the `Tile`/`TileGroup` data model

- **Decision**: Rename the existing `Service` dataclass to `Tile` (fields `name`, `url`,
  `icon?` unchanged) and its container field `services`→`tiles`. Add a `TileGroup`
  dataclass mirroring `BookmarkGroup` but **without** a `collapsed` field: `{name,
  tiles: list[Tile], icon?}`. `DashboardConfig.services`→`DashboardConfig.tiles`, and add
  `DashboardConfig.tile_groups`.
- **Rationale**: The clarified spec (Q1→A) mandates the breaking rename of config keys and
  identifiers, and explicitly reframes the entities as `Tile` and `TileGroup` (Key
  Entities). Following the existing `BookmarkGroup` shape keeps the codebase uniform.
- **Alternatives considered**: keeping Python identifiers stable while only changing the
  config key — rejected by Q1→A (full internal + user-facing rename, FR-001/FR-012).

## R5 — Full-repo rebrand scope (what "tile" replaces "service")

- **Decision**: The rebrand changes **every** applicable `service`→`tile` facet:
  - Config keys: `services`→`tiles`, `service_groups`→`tile_groups`.
  - Python: `Service`→`Tile`, `ServiceGroup`→`TileGroup`, `_parse_service`→`_parse_tile`,
    `_parse_service_group`→`_parse_tile_group`, variables `services`/`raw_services`→
    `tiles`/`raw_tiles`, `config.services`→`config.tiles`.
  - CSS classes: `.service-icon`→`.tile-icon`, `.service-icon img`→`.tile-icon img`,
    `.service-monogram`→`.tile-monogram`, `.service-name`→`.tile-name`,
    `.service-tile`→`.tile` (in both `index.html` and `app.css`, including mobile
    `@media` refinements).
  - Template: `aria-label="Services"`→`"Tiles"`, `<meta description>`, HTML comment,
    loop variables `service`→`tile`.
  - Tests: `test_views_services.py`→`test_views_tiles.py`,
    `test_homepage_services.py`→`test_homepage_tiles.py`, function names/variables
    (`test_services_render_*`→`test_tiles_render_*`), `services["..."]`→`tiles["..."]`.
  - Docs: README feature bullet, config comments, example YAML.
- **Rationale**: The clarified spec (FR-012, US6, SC-006) explicitly requires **no
  applicable "services" reference remains** for the former services feature across every
  facet, excluding git history and unrelated content (e.g., the `bookmark` label "National
  Benefits Services").
- **Alternatives considered**: verbiage-only rebrand (keep internal `Service`/`services`
  identifiers and CSS classes) — this was the pre-clarification design and is **rejected**
  by Q1→A.
- **Note on the final sweep**: a case-insensitive `grep -rni "service"` will still match
  "Services" in the unrelated bookmark label "National Benefits Services", the string
  "Dashboard Services" if any, and other unrelated words containing "service" (e.g.,
  "service" in third-party asset filenames is out of scope unless it refers to the former
  section). The sweep filters these to "no applicable reference".

## R6 — Tiles may target homelab OR external services

- **Decision**: Documentation and `config/example.yaml` present a tile as a general-purpose
  link to either an internal homelab service or an external service (webmail, cloud
  portal, SaaS admin console). Example config gains at least one external tile alongside
  internal homelab tiles (FR-013, US7, SC-007).
- **Rationale**: Explicit requirement (spec FR-013, US7). The mechanics are unchanged:
  any valid `http(s)` URL renders and opens in a new tab (`target="_blank"` +
  `rel="noopener noreferrer"`), regardless of target.
- **Alternatives considered**: restricting tiles to `.lan`/internal hosts — rejected; the
  spec explicitly allows any `http(s)` URL and external services are in scope.

## R7 — Validation & error reporting for tile groups

- **Decision**: `tile_groups` must be a list when present; each entry a mapping with a
  non-empty `name`; each entry's `tiles` must be a list (empty list valid). Nested tiles
  validated with the same `_parse_tile` as flat tiles. Violations raise a specific
  `ConfigValidationError` with the `tile_groups[i]` path (FR-007, SC-004). No partial
  application: `parse_dashboard` only returns a fully valid config.
- **Rationale**: Mirrors the existing `_parse_group` validation pattern and error-message
  style, keeping readable, specific messages (Principle I — actionable diagnostics).
- **Alternatives considered**: lenient parsing that skips malformed groups — rejected
  (silently hides config errors; violates FR-007/SC-004 and Security "escape/validate").

## R8 — Live reload & editor interaction

- **Decision**: `tile_groups` participates in the existing load/reload cycle unchanged.
  The `ConfigLoader` hot-reloads on mtime change and `parse_dashboard` validates the new
  key. The in-browser editor (`POST /config/save`) writes raw YAML text; grouped config
  is validated by `parse_dashboard` on the next reload exactly like flat config. A
  malformed save is rejected with a clear error and the last valid config is preserved
  (FR-008, FR-009; existing feature-008 behavior).
- **Rationale**: No editor UI change is required because the editor is a raw-text editor
  and validation is centralized in `parse_dashboard` (YAGNI, Principle I).
- **Alternatives considered**: adding a structured group editor UI — rejected (YAGNI; out
  of scope, config-text organization is the documented workflow).

## R9 — "Bookmarks" header behavior with zero/empty bookmark groups

- **Decision**: The hardcoded `<h3 class="group-title">Bookmarks</h3>` renders only when
  `bookmark_groups` is non-empty; when empty, the existing "No bookmarks configured yet."
  message renders instead (spec Edge Case: "show it when the accordion is present").
- **Rationale**: FR-011 requires the heading "directly above the bookmark accordion"; with
  no accordion present there is nothing to label, so the "No bookmarks" placeholder
  remains. Hardcoded, not configurable.
- **Alternatives considered**: always showing the "Bookmarks" heading even with zero
  groups — rejected; it would label an empty section and conflict with the placeholder
  text path.
