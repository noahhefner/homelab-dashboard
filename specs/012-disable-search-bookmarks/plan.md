# Implementation Plan: Disable Search and Bookmarks

**Branch**: `012-disable-search-bookmarks` | **Date**: 2026-09-06 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/012-disable-search-bookmarks/spec.md`

## Summary

Add two top-level YAML config flags — `show_search` and `show_bookmarks` — that let the dashboard owner hide the navbar search bar and/or the bookmarks section. Both default to enabled (`true`), so existing configs render exactly as before. When disabled, the feature is omitted from the rendered page (occupies zero space) and the remaining layout rebalances: the search bar's navbar space is reclaimed by the flex layout, and the tiles column expands to full width in place of the bookmarks column. The flags are parsed into `DashboardConfig` via `parse_dashboard` and consumed by the Jinja2 templates, following the same config → model → view → template data flow as `search_engine` (feature-011). The `config/example.yaml` file is updated to document both flags.

## Technical Context

**Language/Version**: Python 3.14 (project `requires-python = ">=3.14"`)

**Primary Dependencies**: Flask (web framework), PyYAML (config parsing), Bootstrap 5 + Bootstrap Icons (vendored, via Vite build)

**Storage**: YAML config file on disk (live-reloaded via `ConfigLoader`)

**Testing**: pytest (unit, integration, contract tests already established); sed-style assertions via BeautifulSoup helpers in `tests/soup_utils.py`

**Target Platform**: Linux server (self-hosted homelab), browsers on desktop and mobile

**Project Type**: Web application (Flask + Jinja2 templates + static Bootstrap)

**Performance Goals**: No measurable performance impact; flags are static booleans evaluated at render time, with no server-side processing at request time

**Constraints**: Must use Bootstrap utility classes and components per Principle VI (Framework-First Frontend). Hiding is plain Jinja `{% if %}` conditional rendering plus existing Bootstrap flex/grid utilities — no custom CSS or JavaScript. Invalid flag values must fall back to the default (enabled) without a config load error (spec FR-009).

**Scale/Scope**: Single-user homelab dashboard; 2 templates affected (index.html, config.html), 3 Python modules (model.py, schema.py, views.py), 1 config example file, plus tests.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Developer Experience First | PASS | Config change is live-reloaded; no restart needed; defaults preserve current behavior |
| II. Readability Over Cleverness | PASS | Two simple boolean flags with clear names (`show_search`, `show_bookmarks`); plain `{% if %}` gating in templates |
| III. Extensibility & Modularity | PASS | Config is a self-contained extension of the existing parse pipeline; no coupling to other modules |
| IV. Testability | PASS | Test-First: unit + contract tests for parsing, integration tests for rendered output (Test-First NON-NEGOTIABLE) |
| V. YAGNI & Simplicity | PASS | No abstractions beyond a tiny boolean-parse helper; no new dependencies |
| VI. Framework-First Frontend | PASS | Hiding uses conditional template rendering; layout rebalance reuses existing Bootstrap flex/grid utilities (`me-auto`/`ms-auto`, `col-*`); no custom CSS/JS needed |
| Security Requirements | PASS | No secrets; no new user-controlled content rendered; flags are strict booleans with safe defaults |

## Project Structure

### Documentation (this feature)

```text
specs/012-disable-search-bookmarks/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
app/
├── model.py             # Add show_search and show_bookmarks fields to DashboardConfig
├── schema.py            # Add _parse_bool_flag; parse show_search/show_bookmarks in parse_dashboard
├── views.py             # Pass show_search and show_bookmarks to templates
├── templates/
│   ├── index.html       # Gate search form on show_search; gate bookmarks <aside> on show_bookmarks;
│   │                    #   expand tiles to full width when bookmarks hidden
│   └── config.html      # Gate search form on show_search
config/
│   └── example.yaml     # Add show_search: true and show_bookmarks: true with comments
tests/
├── unit/
│   └── test_schema.py   # Add show_search/show_bookmarks parsing tests (default, true/false, invalid)
├── integration/
│   └── test_visibility_toggles.py  # NEW: search/bookmarks hiding + layout rebalance tests
└── contract/
    └── test_config_schema.py  # Add new keys to recognized-key contract; flag contract tests
```

**Structure Decision**: Flat module structure matches existing project conventions (see feature-011's plan). No new modules or directories — additions go in existing files plus one new integration test file.

## Complexity Tracking

> No Constitution Check violations. No complexity justifications needed.