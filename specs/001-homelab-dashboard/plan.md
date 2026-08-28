# Implementation Plan: Homelab Dashboard Homepage

**Branch**: `001-homelab-dashboard` | **Date**: 2026-08-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-homelab-dashboard/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Build a self-hosted homelab landing page (Python web app) that renders services and grouped bookmarks defined in a single YAML file. The app ships as one Docker container, uses no database, serves a UIkit-based frontend, and reloads the YAML config on the fly (no backend or container restart). No authentication in this version.

## Technical Context

**Language/Version**: Python 3.14 (backend)

**Primary Dependencies**: 
- Package/environment manager: `uv` (project tooling; no pip).
- Backend web framework: Flask (lightweight, single-process, easy live reload). 
- Frontend: UIkit (CSS/JS UI framework) served as static assets.
- YAML parsing: PyYAML.
- Container: Docker (single container), official Python slim base image.

**Storage**: None (no database). All content driven entirely by the mounted YAML config file on the host via a Docker volume.

**Testing**: pytest (backend unit + integration, run via `uv run pytest`), plus a lightweight frontend smoke check.

**Target Platform**: Linux server (Docker host); clients are any modern desktop/mobile browser.

**Project Type**: web application (backend + frontend).

**Performance Goals**: Homepage interactive in under 2 seconds on a homelab network (per SC-004); must handle 150+ bookmarks gracefully (per SC-003).

**Constraints**: Single Docker container; no database; in-place YAML reload without restarting the process or container (per user requirement); mobile-first responsive UI; no authentication.

**Scale/Scope**: Personal homelab, single user. Content is small (tens of services, 150+ bookmarks).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gate 1 — Extensibility & Modularity**: The app must be split into small, bounded modules (config loading, model, rendering/router, frontend assets). Vendored UIkit must be imported as a dependency, not forked. ✅ (Design keeps a single bounded config-to-HTML pipeline with a clear contract between config schema and rendering.)

**Gate 2 — Testability (Test-First, NON-NEGOTIABLE)**: Tests written before/alongside code; contract tests for the YAML schema; integration tests for config reload. ✅ (Plan mandates pytest coverage and a deterministic config parer that is mockable/unit-testable.)

**Gate 3 — YAGNI & Simplicity**: No database, no auth, no framework beyond a minimal web server — matches user's explicit "no DB, no auth, single container" requirement. ✅ No added complexity beyond the problem.

**Gate 4 — Security Requirements**: External URLs must be validated and rendered content escaped to prevent injection; HTTPS/timeouts for any outbound contact. ✅ (Plan includes URL validation and HTML escaping of all user/third-party content.)

**Gate 5 — DX First / Readability**: Single-command local run, readable modules, a sensible example config. ✅ (Quickstart provides a one-command run; config schema is documented.)

No violations; no Complexity Tracking table required.

## Project Structure

### Documentation (this feature)

```text
specs/001-homelab-dashboard/
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
├── __init__.py          # App factory (Flask app creation, config path wiring)
├── server.py            # Entry point: starts the web server, serves the single page
├── config.py            # YAML config loader + live-reload (file watch / re-read on request)
├── model.py             # Data model: Service, Bookmark, BookmarkGroup, Dashboard config
├── schema.py            # Config validation/parsing (YAML -> model objects)
├── views.py             # Route handlers: render homepage HTML, health endpoint
├── templates/
│   └── index.html       # Single-page UIkit template
└── static/
    ├── uikit/           # Vendored UIkit assets (imported dependency)
    └── app.css, app.js  # Dashboard-specific styling + group toggle behavior

config/
└── example.yaml         # Example/starting configuration file

tests/
├── contract/            # YAML schema contract tests
├── integration/         # Config load + reload + render integration tests
└── unit/                # model / schema / config unit tests

Dockerfile               # Single container build
docker-compose.yml       # Optional: volume mount of config
pyproject.toml           # Python project config + deps (managed with uv)
uv.lock                  # Lockfile generated by uv
```

**Structure Decision**: A single-project web app with a small, clearly bounded Python module split (config → schema/model → views) plus a single-page UIkit frontend under templates/static. This satisfies Principle III (modularity) without introducing an unnecessary multi-project workspaces.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No Constitution Check violations; this table is intentionally empty.
