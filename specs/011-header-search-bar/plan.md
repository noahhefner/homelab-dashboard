# Implementation Plan: Header Search Bar

**Branch**: `011-header-search-bar` | **Date**: 2026-09-03 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/011-header-search-bar/spec.md`

## Summary

Add a search bar to the dashboard navbar that submits queries to a configurable search engine and opens results in a new tab. The search engine URL template is stored in the YAML config as a top-level `search_engine` key with a `{query}` placeholder. A configurable icon (`search_engine_icon` key, external image URL) sits to the left of the search input to indicate the configured engine, falling back to a default magnifying-glass icon. The search bar and its icon are completely hidden on mobile viewports.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Flask (web framework), PyYAML (config parsing), Bootstrap 5 (CSS/JS framework, vendored locally)

**Storage**: YAML config file on disk (live-reloaded via `ConfigLoader`)

**Testing**: pytest (unit, integration, contract tests already established)

**Target Platform**: Linux server (self-hosted homelab), browsers on desktop and mobile

**Project Type**: Web application (Flask + Jinja2 templates + static Bootstrap)

**Performance Goals**: No measurable performance impact; search bar is static HTML with no server-side processing at query time

**Constraints**: Must use Bootstrap utility classes and components per Principle VI (Framework-First Frontend). No JavaScript required for core search-and-open behavior (HTML form with `target="_blank"`).

**Scale/Scope**: Single-user homelab dashboard; 2 templates affected (index.html, config.html)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Developer Experience First | PASS | Config change is live-reloaded; no restart needed |
| II. Readability Over Cleverness | PASS | Simple HTML form, clear config key name |
| III. Extensibility & Modularity | PASS | Config key is self-contained; no coupling to existing modules |
| IV. Testability | PASS | Tests follow existing patterns (pytest, Flask test client) |
| V. YAGNI & Simplicity | PASS | No abstractions beyond what's needed; plain HTML form |
| VI. Framework-First Frontend | PASS | Uses Bootstrap `d-none d-md-flex` for mobile hiding, Bootstrap form classes, `bi-search` default icon |
| Security Requirements | PASS | No secrets; `rel="noopener"` on new tab; icon is user-configured external image URL (validated); onerror fallback prevents broken-image behavior |

## Project Structure

### Documentation (this feature)

```text
specs/011-header-search-bar/
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
├── model.py             # Add search_engine and search_engine_icon fields to DashboardConfig
├── schema.py            # Parse and validate search_engine and search_engine_icon from YAML
├── views.py             # Pass search_engine_url and search_engine_icon to templates
├── templates/
│   ├── index.html       # Add search bar (with icon) to navbar
│   └── config.html      # Add search bar (with icon) to navbar
├── static/
│   └── app.css          # Minimal custom CSS for search bar (if needed beyond Bootstrap)
config/
│   └── example.yaml     # Add search_engine and search_engine_icon examples
tests/
├── unit/
│   └── test_schema.py   # Add search_engine and search_engine_icon parsing tests
├── integration/
│   ├── test_navbar.py   # Add search bar presence + icon tests
│   └── test_mobile_layout.py  # Add mobile hiding tests (incl. icon)
└── contract/
    └── test_config_schema.py  # Add search_engine and search_engine_icon contract tests
```

**Structure Decision**: Flat module structure matches existing project conventions. No new directories or files beyond additions to existing locations.

## Complexity Tracking

> No Constitution Check violations. No complexity justifications needed.
