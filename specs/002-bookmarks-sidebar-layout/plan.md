# Implementation Plan: Bookmarks Sidebar Layout

**Branch**: `002-bookmarks-sidebar-layout` | **Date**: 2026-08-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-bookmarks-sidebar-layout/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Update the dashboard frontend so that bookmarks render in a right-hand column on desktop (reserving the main/left area for the homelab apps) and move to below the apps on mobile/narrow viewports. In support of the responsive layout, replace the currently vendored UIkit CSS/JS with Bootstrap CSS/JS, vendored locally so the page works without internet connectivity. This is a presentation-only change: the backend, YAML data model, and bookmark/organization behavior are unchanged.

## Technical Context

**Language/Version**: Python 3.14 (backend, unchanged). Frontend markup in Jinja2 templates with plain CSS/JS.

**Primary Dependencies**:
- Backend web framework: Flask 3.x (unchanged).
- YAML: PyYAML (unchanged).
- Frontend UI framework: **Bootstrap 5** (CSS + JS) **replacing** the currently vendored UIKit assets. Bootstrap assets are **vendored locally** under `app/static/bootstrap/` so the UI works offline.
- No new Python dependencies; Bootstrap is a static asset only.

**Storage**: None (no database). Content remains driven by the mounted YAML config file. Unchanged from feature 001.

**Testing**: pytest (backend unit + integration, run via `uv run pytest`). Frontend behavior verified through rendered-HTML assertions in integration tests (grid/layout classes, breakpoint classes, vendored-asset references, collapsed-group state).

**Target Platform**: Linux server (Docker host); clients are any modern desktop/mobile browser (Bootstrap 5 supports current+1 browsers).

**Project Type**: web application (backend + frontend); this feature is frontend-only.

**Performance Goals**: Homepage interactive in under 2 seconds on a homelab network (per SC-004); must handle 150+ bookmarks gracefully (per SC-003), now within a side column on desktop.

**Constraints**: Must work offline (Bootstrap vendored, no CDN). Single Docker container. No database. In-place YAML reload unchanged. Mobile-first responsive behavior preserved. No new runtime dependencies.

**Scale/Scope**: Personal homelab, single user. Two coupled UI changes: (1) UIKit → Bootstrap migration, (2) bookmark column placement. Backend and config schema untouched.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gate 1 — Extensibility & Modularity**: Keep the small, bounded module split. Boostrap is imported as a vendored dependency and referenced via templates/static, not forked or edited. The layout change is confined to the template/CSS/JS layer. ✅

**Gate 2 — Testability (Test-First, NON-NEGOTIABLE)**: Update existing integration tests that assert UIKit classes, and add assertions for the new Bootstrap grid classes, the right-side bookmark container, the mobile breakpoint behavior, and offline asset references. Tests written alongside the change and must pass in a clean run. ✅

**Gate 3 — YAGNI & Simplicity**: Use Bootstrap's standard grid (CSS) and collapse (JS) components rather than building custom responsive layout machinery. No new abstraction layers. Offline vendoring is required by the user and is the simplest way to meet it. ✅

**Gate 4 — Security Requirements**: External bookmark/service URLs continue to be validated and rendered content escaped (unchanged). No new unsanitized content paths. ✅

**Gate 5 — DX First / Readability**: One-command run (`uv run flask --app app run` or the Docker flow) unchanged; vendored Bootstrap committed so offline/local dev works. Clear, readable template/CSS matching existing conventions. ✅

No violations; no Complexity Tracking table required.

## Project Structure

### Documentation (this feature)

```text
specs/002-bookmarks-sidebar-layout/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
app/
├── __init__.py          # App factory (unchanged form feature 001)
├── server.py            # Entry point (unchanged)
├── config.py            # YAML config loader + live-reload (unchanged)
├── model.py             # Data model: Service, Bookmark, BookmarkGroup, DashboardConfig (unchanged)
├── schema.py            # Config validation/parsing (unchanged)
├── views.py             # Route handlers (unchanged logic; passes same context)
├── templates/
│   ├── index.html       # UPDATED: Bootstrap layout, bookmark right column on desktop, below on mobile
│   └── error.html       # UPDATED: switch UIKit classes to Bootstrap
└── static/
    ├── bootstrap/       # NEW: vendored Bootstrap CSS+JS (replaces app/static/uikit/)
    ├── app.css          # UPDATED: Bootstrap-based layout/column/group styles
    └── app.js           # UPDATED: group collapse using Bootstrap collapse API / data attributes

# REMOVED: app/static/uikit/

config/
└── example.yaml         # Unchanged (may be updated only to showcase layout; no schema change)

tests/
├── contract/            # YAML schema contract tests (unchanged)
├── integration/         # UPDATED: home page, bookmark groups, mobile/layout, invalid config, reload
└── unit/                # UPDATED: view rendering asserts for new classes

Dockerfile               # Unchanged (serves static assets; Bootstrap is vendored locally)
docker-compose.yml       # Unchanged
Dockerfile
pyproject.toml           # Unchanged (no new Python deps)
```

**Structure Decision**: Keep the single-project web app structure from feature 001. Only the frontend layer changes: swap the vendored UIkit directory for a vendored Bootstrap directory, replace UIKit utility/component classes in the templates and CSS, and rework the template grid so bookmarks occupy a right column at `lg`+ breakpoints and stack below the apps on smaller screens. The Python backend and data-contract layers remain completely untouched.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No Constitution Check violations; this table is intentionally empty.
