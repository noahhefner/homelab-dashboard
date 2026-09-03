# Data Model: Header Search Bar

**Feature**: 011-header-search-bar
**Date**: 2026-09-03

## Entities

### DashboardConfig (extended)

| Field | Type | Default | Validation | Notes |
|-------|------|---------|------------|-------|
| `title` | `str` | `"Homelab"` | Non-empty string | Existing field, unchanged |
| `tile_groups` | `list[TileGroup]` | `[]` | List of valid TileGroup | Existing field, unchanged |
| `bookmark_groups` | `list[BookmarkGroup]` | `[]` | List of valid BookmarkGroup | Existing field, unchanged |
| `search_engine` | `str \| None` | `None` | If present: must be a string containing `{query}` placeholder | **New field** |
| `search_engine_icon` | `str \| None` | `None` | If present: must be a valid http/https URL (via `validate_url`) | **New field** |

### Config YAML (extended)

```yaml
# Existing keys (unchanged)
title: "Home Lab"
editor: true
tile_groups: [...]
bookmark_groups: [...]

# New keys (optional)
search_engine: "https://duckduckgo.com/?q={query}"
search_engine_icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/duckduckgo.svg"
```

### Validation Rules

1. `search_engine` is **optional** — if absent, the default (`https://www.google.com/search?q={query}`) is used at render time.
2. If present, `search_engine` MUST be a string.
3. If present, `search_engine` MUST contain the substring `{query}`. If missing, fall back to the default.
4. No URL validation is performed on the search engine URL beyond checking for the `{query}` placeholder (the URL is used as a form `action`, not fetched server-side).
5. The `{query}` placeholder is replaced with the URL-encoded search terms at render time in the template.
6. `search_engine_icon` is **optional** — if absent, the default `bi-search` Bootstrap icon is used at render time.
7. If present, `search_engine_icon` MUST be a valid http/https URL (via `validate_url`, same as tile/bookmark icons). If invalid, fall back to the default `bi-search` icon.
8. If the configured icon URL fails to load (broken image), the HTML `onerror` fallback pattern hides the broken `<img>` and reveals the default `bi-search` icon.

### State Transitions

None. The search engine URL and icon are static configuration values that are live-reloaded like all other config values.
