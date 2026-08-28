# Phase 0 Research: Homelab Dashboard Homepage

**Date**: 2026-08-28
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

This file records the research and design decisions that resolve the technical
details of the implementation plan. It consolidates Phase 0 (Outline & Research)
outputs following the workflow in `.specify/templates/plan-template.md`.

## Research Topics

### R1: Backend framework for serving a single-page UIkit homepage

- **Decision**: Flask (Python 3.14) as the web framework, serving a single rendered
  HTML template plus static UIkit assets.
- **Rationale**: Flask is lightweight, single-process, trivial to run in one Docker
  container, and has first-class static-file serving and Jinja template rendering —
  exactly matching the scope (a small landing page with no database or auth). It
  requires no extra runtime beyond Python.
- **Alternatives considered**:
  - FastAPI: heavier (async, Pydantic) and begs for a JSON API we don't need; YAGNI violation.
  - Django: far too heavy for a single-page dashboard; YAGNI violation.
  - Node/Express, static-site generator: rejected because the user explicitly required a Python backend.

### R2: Live YAML configuration reload without restarting the backend or container

- **Decision**: **Reload-on-request with modification-time checking.** The application
  caches the parsed config keyed by file modification time/size; on every page request
  it re-checks the mounted YAML file's mtime and re-parses only when it changed. Editing
  the mounted YAML and hitting refresh picks up the change with zero backend or container
  restarts and zero extra moving parts.
- **Rationale**: This is the simplest deterministic approach that satisfies the hard
  requirement ("update yaml and reload on the fly without restarting"). Because the
  homepage is a low-traffic personal dashboard, re-checking mtime on each request is
  trivial (one `stat()` call) and always correct. It is fully unit-testable and requires
  no background threads, locks, or debouncing.
- **Alternatives considered**:
  - `watchdog`/inotify file-watcher with a background thread: adds thread-safety
    concerns, debounce edge cases, and a dependency — unnecessary complexity for a
    low-traffic page (YAGNI). Rejected.
  - Config via an additional `/reload` HTTP endpoint: requires manual external action
    and doesn't auto-reflect file edits; rejected (worse DX, more moving parts).
  - SIGHUP-triggered reload (production pattern): works but is Linux/Docker-signal
    specific and manual; the mtime check is simpler and automatic. File-watcher
    research confirmed mtime/polling approaches are standard and sufficient here.

### R3: UIkit integration

- **Decision**: Vendor the pre-built UIkit assets (CSS + JS from the official download)
  into `app/static/uikit/` and reference them from the single Jinja template. No npm
  build pipeline.
- **Rationale**: UIkit is distributed as prebuilt CSS/JS that can be dropped into a
  static directory and served directly by Flask. This keeps the frontend simple,
  avoids a Node toolchain in the Python/Docker stack, and matches the "UIkit for the
  user interfaces" requirement exactly. It provides the responsive grid, card/tile
  components, accordion/collapsible groups, and mobile behavior used to meet the
  responsive and bookmark-scale requirements. UIkit has no jQuery dependency.
- **Alternatives considered**:
  - npm/webpack bundling of UIkit: adds a Node build step to a pure-Python container;
    violates YAGNI and the single-container simplicity goal. Rejected.
  - CDN-hosted UIkit: requires internet at view time and is unsuitable for a self-hosted
    homelab that should work offline/local. Rejected in favor of vendoring.

### R4: Single-container Docker packaging with mounted config volume

- **Decision**: One container from a `python:3.14-slim` base image, with the Python
  project and dependencies installed/managed via `uv` (not pip). The YAML config is
  mounted via a Docker volume at a known path (e.g. `/app/config.yaml`), passed to the
  app through an environment variable. Flask's built-in server (or a single Gunicorn
  worker) runs the app; no database, no sidecar containers, no auth.
- **Rationale**: Matches the user's explicit constraints ("run as one Docker container",
  "no database", "mount the config file via a docker volume"). A volume-mounted config
  is edited on the host and picked up automatically by the R2 reload mechanism.
- **Alternatives considered**:
  - Multi-container (app + DB + reverse proxy): explicitly rejected by the user's
    "one container, no database" requirement.
  - Baking the config into the image: would defeat the purpose of volume-mounting and
    editing on the host; rejected.

### R5: Security handling of external content

- **Decision**: All service/bookmark URLs and labels derived from user-edited YAML must
  be validated and HTML-escaped when rendered. Jinja auto-escaping is enabled for
  labels; destination URLs are attribute-escaped and opened in a new tab with
  `rel="noopener noreferrer"`. Because this is a single-user homelab config, the 
  "threat model" is defensive escaping/injection-avoidance rather than full SSRF
  protection — but output escaping is mandatory per the Constitution's Security
  Requirements.
- **Rationale**: The Constitution requires escaping any third-party/user-controlled
  rendered content and validating external URLs. This keeps the dashboard safe-by-default
  even if the YAML comes from an untrusted source.
- **Alternatives considered**: None reasonable; escaping is non-negotiable.

## Consolidated Decisions Summary

| Topic | Decision | Key principle |
|-------|----------|---------------|
| Backend | Python 3.14 + Flask | YAGNI, DX |
| Frontend | UIkit (vendored static assets) | No Node build, matches requirement |
| Config source | Single mounted YAML, no DB | User requirement, YAGNI |
| Live reload | mtime-checked re-parse on each request | Extensibility, DX, testability |
| Packaging | Single slim Docker container + volume mount | User requirement |
| Security | Validate + escape all rendered URLs/labels | Security Requirements guarantee |

All NEEDS CLARIFICATION items from Technical Context are resolved above. No open
clarifications remain.
