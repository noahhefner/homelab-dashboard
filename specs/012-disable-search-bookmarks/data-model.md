# Data Model: Disable Search and Bookmarks

**Feature**: 012-disable-search-bookmarks
**Date**: 2026-09-06

## Entities

### DashboardConfig (extended)

| Field | Type | Default | Validation | Notes |
|-------|------|---------|------------|-------|
| `title` | `str` | `"Homelab"` | Non-empty string | Existing field, unchanged |
| `tile_groups` | `list[TileGroup]` | `[]` | List of valid TileGroup | Existing field, unchanged |
| `bookmark_groups` | `list[BookmarkGroup]` | `[]` | List of valid BookmarkGroup | Existing field, unchanged |
| `search_engine` | `str \| None` | `None` | If present: string containing `{query}` placeholder | Existing field (feature-011), unchanged |
| `search_engine_icon` | `str \| None` | `None` | If present: valid http/https URL | Existing field (feature-011), unchanged |
| `show_search` | `bool` | `True` | If present: must be a boolean; non-boolean falls back to `True` | **New field** |
| `show_bookmarks` | `bool` | `True` | If present: must be a boolean; non-boolean falls back to `True` | **New field** |

### Config YAML (extended)

```yaml
# Existing keys (unchanged)
title: "Home Lab"
editor: true
tile_groups: [...]
bookmark_groups: [...]
search_engine: "https://duckduckgo.com/?q={query}"
search_engine_icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/duckduckgo.svg"

# New keys (optional, default enabled)
show_search: true
show_bookmarks: true
```

### Validation Rules

1. `show_search` and `show_bookmarks` are **optional** — when absent, both default to `True` (feature shown).
2. If present, each value MUST be a boolean. A valid boolean is used as-is.
3. If present but NOT a boolean (e.g., a string, number, or null), the flag falls back to its default `True` (feature shown) and the config loads without error (spec FR-009).
4. The two flags are entirely independent: setting one MUST NOT affect the other (spec FR-007).
5. `show_search` gates rendering of the navbar search form (and its icon) on all pages with a navbar. When `False`, the search form and icon are not rendered and occupy zero space.
6. `show_bookmarks` gates rendering of the bookmarks `<aside>` (all bookmark groups) on the homepage. When `False`, no bookmark group is rendered, no space is reserved, and the tiles use the freed space.
7. Hidden features' configuration (e.g., `search_engine`, `bookmark_groups`) remains valid in the config file and is parsed normally but ignored at render time (spec FR-003 / FR-005 edge cases).

### State Transitions

None. The flags are static configuration values that are live-reloaded like all other config values via `ConfigLoader`; a change takes effect on the next page load.