# Contracts: Header Search Bar

**Feature**: 011-header-search-bar
**Date**: 2026-09-03

## Config Schema Contract

The YAML config file accepts optional top-level `search_engine` and `search_engine_icon` keys:

```yaml
search_engine: "https://example.com/search?q={query}"
search_engine_icon: "https://example.com/icon.png"
```

### Contract Rules: `search_engine`

| Rule | Description |
|------|-------------|
| Key | `search_engine` (top-level, optional) |
| Type | String |
| Placeholder | Must contain `{query}` substring |
| Default | When absent or invalid: `https://www.google.com/search?q={query}` |
| Encoding | The `{query}` placeholder is replaced with URL-encoded search terms |

### Contract Rules: `search_engine_icon`

| Rule | Description |
|------|-------------|
| Key | `search_engine_icon` (top-level, optional) |
| Type | String |
| Validation | Must be a valid http/https URL (via `validate_url`, same as tile/bookmark icons) |
| Default | When absent or invalid: Bootstrap `bi-search` icon (magnifying glass) |
| Broken image | HTML `onerror` fallback hides broken `<img>` and shows `bi-search` icon |
| Mobile | Hidden along with the search bar (`d-none d-md-flex`) |

### Valid Examples

```yaml
search_engine: "https://www.google.com/search?q={query}"
search_engine: "https://duckduckgo.com/?q={query}"
search_engine: "https://www.bing.com/search?q={query}"
search_engine: "https://search.brave.com/search?q={query}"
search_engine_icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/duckduckgo.svg"
search_engine_icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/google.svg"
```

### Invalid Examples (fall back to default)

```yaml
# Missing placeholder
search_engine: "https://duckduckgo.com/"
# Not a string
search_engine: 123
# Empty string
search_engine: ""
# Invalid URL (not http/https)
search_engine_icon: "not-a-url"
# Empty string
search_engine_icon: ""
```

## HTML Contract

The search bar renders as a `<form>` in the navbar:

```html
<form class="d-none d-md-flex align-items-center gap-2 me-3"
      action="{search_engine_url}"
      method="GET"
      target="_blank"
      rel="noopener">
    {% if search_engine_icon %}
        <img src="{{ search_engine_icon }}"
             alt="{{ search_engine_name }}"
             class="search-engine-icon"
             onerror="this.style.display='none'; this.nextElementSibling.style.display='inline-flex';">
        <span class="search-engine-icon-fallback" style="display:none;">
            <i class="bi bi-search" aria-hidden="true"></i>
        </span>
    {% else %}
        <span class="search-engine-icon">
            <i class="bi bi-search" aria-hidden="true"></i>
        </span>
    {% endif %}
    <input type="search"
           class="form-control form-control-sm"
           name="q"
           placeholder="Search…"
           aria-label="Search the web"
           required>
    <button type="submit"
            class="btn btn-link nav-link p-1"
            aria-label="Search">
        <i class="bi bi-search" aria-hidden="true"></i>
    </button>
</form>
```

### HTML Contract Rules

| Rule | Description |
|------|-------------|
| `action` | The search engine URL with `{query}` replaced by the empty string (browser appends `?q=<encoded-query>`) |
| `method` | `GET` |
| `target` | `_blank` (new tab) |
| `rel` | `noopener` (security) |
| `name` | `q` (standard query parameter name) |
| `required` | Present on the input (prevents empty submission) |
| Icon position | To the left of (before) the search input field |
| Icon fallback | `onerror` hides broken `<img>`, reveals `bi-search` icon fallback |
| Mobile hiding | `d-none d-md-flex` hides below 768px, shows at 768px+ |
| Position | Between the brand and the right-side icon buttons in the navbar |
