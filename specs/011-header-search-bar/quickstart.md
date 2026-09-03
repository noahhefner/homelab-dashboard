# Quickstart Validation: Header Search Bar

**Feature**: 011-header-search-bar
**Date**: 2026-09-03

## Prerequisites

- Python 3.11+ installed
- Project dependencies installed (`pip install -e .` or equivalent)
- A valid config file (e.g., `config/example.yaml`)

## Validation Scenarios

### 1. Search bar visible on homepage (desktop)

```bash
# Start the dev server
python -m app.server

# In a desktop browser, open http://localhost:5000
# Expected: Search bar is visible in the navbar between the title and icon buttons
```

### 2. Search bar visible on config page (desktop)

```bash
# Open http://localhost:5000/config
# Expected: Search bar is visible in the navbar
```

### 3. Search bar hidden on mobile

```bash
# Open browser dev tools, toggle device toolbar, select a mobile viewport (< 768px)
# Navigate to http://localhost:5000
# Expected: Search bar is completely hidden; no space reserved for it in the navbar
```

### 4. Search submission opens new tab

```bash
# On desktop, type "hello world" in the search bar and press Enter
# Expected: New tab opens with Google search results for "hello world"
```

### 5. Custom search engine

```yaml
# Add to config.yaml:
search_engine: "https://duckduckgo.com/?q={query}"
```

```bash
# Reload the page, type a query, submit
# Expected: New tab opens with DuckDuckGo results
```

### 6. Invalid search engine falls back to default

```yaml
# Set in config.yaml:
search_engine: "https://example.com/"
```

```bash
# Reload the page, type a query, submit
# Expected: New tab opens with Google results (fallback)
```

### 7. Empty query does not open tab

```bash
# Clear the search bar, press Enter
# Expected: No new tab opens; search bar retains focus
```

### 8. Search bar in navbar order

```bash
# View page source on http://localhost:5000
# Expected: <form> appears after navbar-brand and before the right-side icon div
```

### 9. Custom search engine icon

```yaml
# Add to config.yaml:
search_engine_icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/duckduckgo.svg"
```

```bash
# Reload the page
# Expected: Custom icon appears to the left of the search input
```

### 10. No icon configured shows default magnifying glass

```bash
# Remove search_engine_icon from config.yaml, reload the page
# Expected: Default bi-search magnifying-glass icon appears to the left of the search input
```

### 11. Broken icon URL shows default magnifying glass

```yaml
# Set in config.yaml:
search_engine_icon: "https://example.com/broken.png"
```

```bash
# Reload the page
# Expected: No broken image placeholder; default bi-search icon is displayed instead
```

### 12. Icon hidden on mobile

```bash
# Open browser dev tools, toggle device toolbar, select a mobile viewport (< 768px)
# Navigate to http://localhost:5000
# Expected: Both the search bar AND its icon are completely hidden
```

## Automated Test Validation

```bash
# Run all tests
pytest

# Run search-bar-specific tests
pytest tests/integration/test_navbar.py -v
pytest tests/integration/test_mobile_layout.py -v
pytest tests/unit/test_schema.py -v -k search
pytest tests/contract/test_config_schema.py -v -k search
```

Expected: All tests pass.
