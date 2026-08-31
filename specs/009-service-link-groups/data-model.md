# Data Model: Tile Link Groups (Services Rebranded as "Tiles")

**Feature**: [spec.md](spec.md) · **Phase 1** · **Date**: 2026-08-31

## Overview

This feature renames the dashboard's link section from "services" to **"tiles"** and adds
an optional `tile_groups` list alongside the flat `tiles` list. Each `tile_groups` entry is
a named, optional-icon collection of tiles (a "tile group"). The rename is **breaking**:
the `Service` type, the `services`/`service_groups` config keys, and all related
identifiers/classes become `Tile`, `tiles`/`tile_groups`, etc.; the legacy keys are not
supported. No new entity kind beyond the rename + group container is introduced; the change
extends `DashboardConfig` and adds a `TileGroup` data class mirroring the existing
`BookmarkGroup` (minus `collapsed`).

## Entities

### Tile (renamed from `Service`)

Represents a clickable tile (a general-purpose link to an internal homelab service or an
external service such as webmail or a cloud portal). Same shape as the former `Service`.

| Field | Type | Config key | Validation |
|-------|------|------------|------------|
| `name` | `str` | `tiles[].name` / `tile_groups[].tiles[].name` | Required, non-empty. |
| `url` | `str` | `tiles[].url` / `tile_groups[].tiles[].url` | Required, valid `http(s)` URL (internal or external). |
| `icon` | `str | None` | `tiles[].icon` / `tile_groups[].tiles[].icon` | Optional. Rendered as `<img>` if `http(s)`, else monogram fallback. |

Opening behavior: any tile link opens in a new tab (`target="_blank"` +
`rel="noopener noreferrer"`), regardless of internal/external target (spec FR-013).

### TileGroup (new; renamed concept from `ServiceGroup`)

A named collection of tiles. Mirrors the `BookmarkGroup` shape but **without** a
`collapsed` field — tile groups are always visible (spec FR-010).

| Field | Type | Config key | Validation |
|-------|------|------------|------------|
| `name` | `str` | `tile_groups[].name` | Required, non-empty. |
| `icon` | `str | None` | `tile_groups[].icon` | Optional. Rendered beside the group name as an `<img>` if `http(s)`, else monogram fallback. |
| `tiles` | `list[Tile]` | `tile_groups[].tiles` | Required list. Each entry validated by `_parse_tile`. Empty list is valid (group renders but has no tiles). |

**Relationship to existing model**:
- A `TileGroup` contains zero or more `Tile` objects (composition).
- `Tile` objects inside a `TileGroup` are independent of any flat `Tile` in the `tiles`
  list — the same tile name may appear in multiple groups or both flat and grouped
  without deduplication (spec Edge Cases).

### DashboardConfig (extended + renamed field)

The top-level config gains a `tile_groups` field and renames `services`→`tiles`.

| Field | Type | Meaning |
|-------|------|---------|
| `title` | `str` | Page title (unchanged). |
| `tiles` | `list[Tile]` | **Flat/un-grouped tiles.** (renamed from `services`). Always honored. |
| `tile_groups` | `list[TileGroup]` | **Named tile groups.** Optional. Rendered as labeled sections of tiles. |
| `bookmark_groups` | `list[BookmarkGroup]` | Bookmark groups (unchanged). |

**Rendering rule** (per research R2):
- Flat `tiles` always render first (unlabeled).
- Each `tile_groups` entry renders as a labeled section (header + tile grid), in declared
  order, always visible.
- If `tile_groups` is empty or absent, only flat `tiles` render (same as today, minus the
  rename).

### Config File on Disk (renamed keys)

The YAML config file is the single source of truth. The `services` key becomes `tiles`;
an optional `tile_groups` key is added. The legacy `services`/`service_groups` keys are
NOT recognized as tiles (breaking change; migration documented in quickstart/README).

## State Transitions

There is no stateful interaction for tile groups — no collapse/expand, no saved user
choice. The rendering is fully derived from the config at each page load:

```
Config load / page render
    │
    ├─ tiles (flat) present?  ─► render flat tiles section (no header)
    │
    ├─ tile_groups present?   ─► for each group:
    │                              render <h3 class="group-title"> group.name
    │                              render group.icon (if present)
    │                              render tile grid for group.tiles
    │
    └─ bookmark_groups present? ─► render <h3 class="group-title"> "Bookmarks" (if groups exist)
                                      render bookmark accordion (unchanged)
                                      "No bookmarks configured yet." (if empty)
```

## Relationship to Existing Model

- `Tile` is the renamed `Service` — same fields, same validation, same rendering.
- `TileGroup` is added as a parallel to `BookmarkGroup` (without `collapsed`), following
  the same validation pattern (required `name`, optional `icon`, list of child objects).
- `parse_dashboard` renames `_parse_service`→`_parse_tile`, reads the flat key `tiles`,
  adds `_parse_tile_group` (mirrors `_parse_group`), and reads `tile_groups`.
- `DashboardConfig` renames the field `services`→`tiles` and gains `tile_groups`; the view
  passes `tiles` and `tile_groups` to the template.
- The template renders tile groups using the same grid structure used for flat tiles,
  wrapped in a per-group header block; all class names rename `service-*`→`tile-*`.
- No new dependencies, no database, no server-side persistence — purely config + template
  + rename sweep.

## Rebrand Scope (renames applied)

This is a **breaking** rename across every applicable facet (spec FR-001/FR-012):

| Facet | Before | After |
|-------|--------|-------|
| Config keys | `services`, `service_groups` | `tiles`, `tile_groups` |
| Model types | `Service`, `ServiceGroup` | `Tile`, `TileGroup` |
| Model field | `DashboardConfig.services` | `DashboardConfig.tiles`, `+ tile_groups` |
| Parser funcs | `_parse_service`, `_parse_service_group` | `_parse_tile`, `_parse_tile_group` |
| Parser vars | `services`, `raw_services` | `tiles`, `raw_tiles` |
| Template vars/loops | `service` loop var | `tile` loop var |
| CSS classes | `.service-icon`, `.service-icon img`, `.service-monogram`, `.service-name`, `.service-tile` | `.tile-icon`, `.tile-icon img`, `.tile-monogram`, `.tile-name`, `.tile` |
| Template label | `aria-label="Services"` | `aria-label="Tiles"` |
| Meta/comment | "Services" / "local services" | "Tiles" / "local tiles" |
| Test files | `test_views_services.py`, `test_homepage_services.py` | `test_views_tiles.py`, `test_homepage_tiles.py` |
| Docs/README/config comments | "services" | "tiles" |

**Retained intentionally** (not part of the rename): unrelated "services" text such as a
bookmark label "National Benefits Services", and anything in git history. No back-compat
aliases for the legacy keys.

## Validation Rules (new/renamed — related to spec FR-007)

1. `tiles` must be a list if present (rejects a legacy/non-list `services` silently
   ignored; the legacy `services`/`service_groups` keys are not used as tile sources).
2. `tile_groups` must be a list if present.
3. Each `tile_groups` entry must be a mapping with a non-empty `name`.
4. Each entry's `tiles` must be a list (defaults to empty if absent).
5. Each tile within a group must pass the same validation as a flat `Tile`.
6. Any violation raises a clear `ConfigValidationError` (with the `tile_groups[i]` path);
   nothing is partially applied.
