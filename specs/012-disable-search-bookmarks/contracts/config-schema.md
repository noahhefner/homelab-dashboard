# Contracts: Disable Search and Bookmarks

**Feature**: 012-disable-search-bookmarks
**Date**: 2026-09-06

## Config Schema Contract

The YAML config file accepts two optional top-level boolean keys that control whether the search bar and the bookmarks section are rendered:

```yaml
show_search: true
show_bookmarks: true
```

### Contract Rules: `show_search`

| Rule | Description |
|------|-------------|
| Key | `show_search` (top-level, optional) |
| Type | Boolean |
| Default | `true` (search bar shown) |
| Invalid value | Non-boolean value (string, number, null) falls back to `true`; config load does NOT fail |
| Effect when `false` | Search form and search icon are not rendered on any page with a navbar (desktop and mobile); they occupy zero layout space |
| Other config | `search_engine` / `search_engine_icon` remain valid keys but are ignored while the search bar is hidden |

### Contract Rules: `show_bookmarks`

| Rule | Description |
|------|-------------|
| Key | `show_bookmarks` (top-level, optional) |
| Type | Boolean |
| Default | `true` (bookmarks shown) |
| Invalid value | Non-boolean value (string, number, null) falls back to `true`; config load does NOT fail |
| Effect when `false` | No bookmark group renders and no space is reserved for the bookmarks section; the tiles use the freed space |
| Other config | `bookmark_groups` remains a valid key but is ignored while bookmarks are hidden |

### Independence

`show_search` and `show_bookmarks` are independent: either, both, or neither may be set without affecting the other.

### Valid Examples

```yaml
show_search: true
show_bookmarks: true

# Hide just the search bar
show_search: false

# Hide just the bookmarks
show_bookmarks: false

# Hide both for a minimal dashboard
show_search: false
show_bookmarks: false
```

### Invalid Examples (fall back to enabled)

```yaml
# Not a boolean - search bar stays shown
show_search: "yes"
# Not a boolean - bookmarks stay shown
show_bookmarks: 0
# Null - treated as absent
show_search: null
```

## HTML Contract

### Search bar (navbar, both pages)

Rendered only when `show_search` is `true`. The `<form>` is wrapped in `{% if show_search %}` in `index.html` and `config.html`:

```html
{% if show_search %}
<form class="d-none d-md-block mx-auto"
      action="{{ search_action }}"
      method="get"
      target="_blank"
      rel="noopener">
  <!-- search input group, unchanged from feature-011 -->
</form>
{% endif %}
```

| Rule | Description |
|------|-------------|
| Rendered when | `show_search` is `true` (default) |
| Omitted when | `show_search` is `false` — the `<form>` is not present in the served HTML at all; zero space |
| Navbar rebalance | Brand `me-auto` + controls `ms-auto` push to opposite edges automatically once the centered form is removed (no CSS change) |

### Bookmarks section (`index.html` only)

Rendered only when `show_bookmarks` is `true`:

```html
{% if show_bookmarks %}
<aside aria-label="Bookmarks" class="col-12 col-lg-3">
  <!-- bookmark accordion, unchanged -->
</aside>
{% endif %}
```

Tiles section when bookmarks are hidden (tiles expand to full width):

```html
<section aria-label="Tiles" class="col-12 {{ 'col-lg-9' if show_bookmarks }}">
```

| Rule | Description |
|------|-------------|
| Rendered when | `show_bookmarks` is `true` (default) |
| Omitted when | `show_bookmarks` is `false` — the `<aside>` is not present in the served HTML at all; zero space, zero reserved column |
| Tiles width | `col-12` full width when bookmarks hidden; `col-12 col-lg-9` (with bookmarks `col-lg-3`) when shown |

## Contract Tests (backing the schema contract)

Covered by `tests/contract/test_config_schema.py` additions: the recognized top-level keys list includes `show_search` and `show_bookmarks`; absent → `True`; explicit `false` → `False`; non-boolean → fallback `True` with no load error.