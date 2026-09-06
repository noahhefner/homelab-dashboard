# Quickstart Validation: Disable Search and Bookmarks

**Feature**: 012-disable-search-bookmarks
**Date**: 2026-09-06

## Prerequisites

- Python 3.14+ installed
- Project dependencies installed (`uv sync` or equivalent)
- A valid config file (e.g., `config/example.yaml`)

## Validation Scenarios

### 1. Defaults: search bar and bookmarks shown

```yaml
# config/example.yaml already ships with both flags enabled
show_search: true
show_bookmarks: true
```

```bash
python -m app.server
# Open http://localhost:5000
# Expected: search bar in navbar AND bookmarks column on the right both visible
# Open http://localhost:5000/config
# Expected: search bar in navbar visible
```

### 2. Hide the search bar

```yaml
show_search: false
```

```bash
# Reload http://localhost:5000 and http://localhost:5000/config
# Expected: no search form in either navbar; brand/theme-toggle still present;
# search bar occupies zero space
```

### 3. Hide the bookmarks

```yaml
show_bookmarks: false
```

```bash
# Reload http://localhost:5000
# Expected: no bookmarks section; tiles expand to full width below the navbar
```

### 4. Hide both

```yaml
show_search: false
show_bookmarks: false
```

```bash
# Reload http://localhost:5000
# Expected: clean page - navbar + tiles only, no errors
```

### 5. Independently toggled

```yaml
# Only the search bar hidden: bookmarks must still render
show_search: false

# Then, only the bookmarks hidden: search bar must still render
show_bookmarks: false
```

```bash
# Reload after each change
# Expected: the un-hidden feature is unaffected
```

### 6. Invalid value falls back to shown

```yaml
show_search: "yes"
```

```bash
# Reload http://localhost:5000
# Expected: dashboard loads WITHOUT an error page; search bar is shown (fallback)
```

### 7. Application live reload

```bash
# With the running server, edit config/example.yaml to set show_search: false and save
# Reload http://localhost:5000
# Expected: search bar disappears - no restart or redeploy needed
```

## Automated Test Validation

```bash
# Run all tests
pytest

# Feature-specific tests
pytest tests/integration/test_visibility_toggles.py -v
pytest tests/unit/test_schema.py -v -k "show"
pytest tests/contract/test_config_schema.py -v -k "show"
```

Expected: All tests pass.

## Reference

- Config contract and HTML gating rules: [contracts/config-schema.md](contracts/config-schema.md)
- Field/validation details: [data-model.md](data-model.md)