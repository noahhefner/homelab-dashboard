# Config Contract: Tile Link Groups

**Feature**: [spec.md](../spec.md) · **Phase 1** · **Date**: 2026-08-31

## Overview

The config contract defines the YAML structure the dashboard accepts. This feature
renames the flat `services` key to `tiles`, adds a `tile_groups` top-level key, and
removes the legacy `services`/`service_groups` keys from the accepted tile vocabulary
(breaking change, Clarification Q1 → A).

## Top-Level Keys (complete enumeration)

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| `title` | string | No | Default "Homelab". |
| `tiles` | list of `{name, url, icon?}` | No | Flat/un-grouped tiles. Must be a list. (renamed from `services`) |
| `tile_groups` | list of `{name, icon?, tiles}` | No | Named tile groups. Must be a list. (renamed from `service_groups`) |
| `bookmark_groups` | list of `{name, collapsed?, icon?, bookmarks}` | No | Unchanged. |
| `editor` / `edit_config` | boolean | No | Opt-in editor flag. Unchanged. |

**Allowed keys rule**: Any key not in the above table is silently ignored by
`parse_dashboard` (existing behavior preserved) — **except** that the legacy
`services`/`service_groups` keys are NOT used as tile sources and must be migrated to
`tiles`/`tile_groups` (spec FR-001, US1 AS3). A config that only provides `services`
yields an empty `tiles` list (no tiles).

---

## `tiles[]` Entry (flat; renamed from `services[]`)

```yaml
tiles:
  - name: Plex            # required, non-empty string
    url: "https://..."    # required, valid http(s) URL (internal OR external)
    icon: "https://..."   # optional, any string (rendered as <img> if http(s) URL, else monogram fallback)
```

**Validation rules** (unchanged from current, applied to `Tile`):
- `name`: required, non-empty string.
- `url`: required, valid absolute `http(s)` URL. May point to an internal homelab service
  or an external service (spec FR-013).
- `icon`: optional. Any string or absent. If present and a valid `http(s)` URL, rendered
  as `<img>` with lazy loading and `onerror` monogram fallback. If absent or non-URL,
  monogram fallback.

---

## `tile_groups[]` Entry (new; renamed from `service_groups[]`)

```yaml
tile_groups:
  - name: Media            # required, non-empty string
    icon: "https://..."   # optional, same semantics as tiles[].icon
    tiles:                # required, list of tile entries
      - name: Plex
        url: "https://..."
        icon: "..."
      - name: Emby
        url: "https://..."
```

**Validation rules**:
- `name`: required, non-empty string. Failure → `ConfigValidationError`.
- `icon`: optional. Same rendering/validation semantics as `tiles[].icon`.
- `tiles`: required, must be a list. Each entry validated by `_parse_tile` (same rules as
  flat `tiles[]`). Empty list is valid (group renders with no tiles).
- An invalid or missing `name` in a group → **rejected** (spec FR-007).
- A `tile_groups` entry with no `tiles` key → defaults to empty list (no error).
- `TileGroup` has **no** `collapsed` field; an unknown `collapsed` key is ignored.

---

## `tiles` + `tile_groups` Coexistence

When both keys are present in the same config, both are honored:
- `tiles` render first (unlabeled, flat).
- Each `tile_groups` entry renders after, in declared order, always visible.
- A tile name may appear in both `tiles` and one or more `tile_groups` — no deduplication
  (spec Edge Cases).
- This is valid and must pass schema validation without error.

---

## Interaction with Config Editor (feature 008)

A config saved through the in-browser editor may contain `tiles` and `tile_groups`. The
editor does not need to change; it writes raw YAML text, and `parse_dashboard` validates
it on the next reload. If a saved config includes malformed `tile_groups` (e.g., missing
name, non-list `tiles`), the validation is rejected with a clear error and the last valid
config is preserved (feature 008 existing behavior).

---

## Migration Note (breaking change)

Configs authored against the former `services`/`service_groups` keys MUST rename them to
`tiles`/`tile_groups` and change any `service_groups[].services` internal lists to
`tile_groups[].tiles`. Textual, mechanical change; no transformation is performed
automatically.
