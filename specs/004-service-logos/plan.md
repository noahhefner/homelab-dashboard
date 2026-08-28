# Implementation Plan: Service Logos

**Branch**: `004-service-logos` | **Date**: 2026-08-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/004-service-logos/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Add support for recognizable service logos on the dashboard homepage by ensuring **any valid remote image URL** can be used as a service logo (provided through the existing `icon` field), with a robust monogram/default fallback when a logo is absent or fails to load. Logo URLs are validated/sanitized to prevent injection, and loading stays fast. The user is **encouraged** (not required) to source logos from dashboardicons.com, which is documented in the example config, README, and quickstart. Because the underlying `icon`-as-remote-URL behavior largely already exists (feature 001), this feature mainly formalizes, hardens, validates with tests, and documents the behavior — it is intentionally lightweight (YAGNI).

## Technical Context

**Language/Version**: Python 3.14 (backend, unchanged). No Node/JS build tooling changes.

**Primary Dependencies**: Flask 3.x (unchanged). Bootstrap 5.3.3 (unchanged, feature 003). No new Python runtime dependencies. Logos are remote images loaded in the browser; the recommended (optional) source is dashboardicons.com (direct icon URLs via the jsDelivr CDN pattern `https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/{svg|png}/<name>.<ext>`).

**Storage**: None (no database). Logos are remote URLs; no local asset files are stored or committed (repository stays lean, per feature 003).

**Testing**: pytest (`uv run pytest`) — unit + integration. Existing tests already assert URL-icon and monogram rendering; new tests will lock in "any valid remote URL renders as a logo" and the fallback/safety behavior.

**Target Platform**: Linux server (Docker host) serving the dashboard; browsers load remote logos.

**Project Type**: web application (backend + frontend), with a small, focused enhancement to existing service-icon rendering/behavior plus documentation.

**Performance Goals**: Preserve existing target — homepage loads and becomes interactive in under 2 seconds on a typical home network and standard device even with logos on all configured services.

**Constraints**: 
- Any valid `http(s)` remote image URL must be accepted as a logo URL.
- Logos must not break the page: a fallback (monogram/default) MUST render when a logo is absent or fails to load.
- Rendered logo URLs MUST be validated/escaped to prevent injection (Constitution Security Requirements).
- dashboardicons.com is a recommended convenience source, NOT a hard dependency; the dashboard must work if that site is unreachable.
- No new binary assets committed; pnpm-managed assets and lean repo behavior (feature 003) are preserved.

**Scale/Scope**: Single-project enhancement. Touches config example + docs + tests, with minimal application changes. Affects how the `icon` (logo) value on services is interpreted and validated, and how it is documented.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gate 1 — Extensibility & Modularity**: Logo handling stays within the existing config/schema/rendering boundaries; no new modules or entangled concerns. The `icon`→logo interpretation is a small, bounded extension of the existing `Service` entity. ✅

**Gate 2 — Testability (Test-First, NON-NEGOTIABLE)**: New tests (written first) verify: any valid remote URL renders as a logo `<img>`; a non-URL value falls back to monogram; the existing rendering contract holds; and rendered logo URLs are safe. These are deterministic (no external network needed — rendering is static markup). ✅

**Gate 3 — YAGNI & Simplicity**: No bundled logo library, no local logo storage, no new framework or dependency. Reuses the existing `icon`/URL mechanism and adds docs + tests. dashboardicons.com is optional and only referenced in docs/example. The simplest design that satisfies the spec. ✅

**Gate 4 — Security Requirements**: Logo URLs are validated with the existing `validate_url` (absolute http/https with netloc) and HTML-escaped when rendered, preventing injection. No new secrets or network exposure at runtime. Remote content loads only in the browser (client-side image), matching existing `icon` behavior. ✅

**Gate 5 — DX First / Readability**: Documentation (README/quickstart/example config) makes assigning a logo and finding a dashboardicons.com source easy. No added friction to the common dev loop. ✅

No violations; no Complexity Tracking table required until post-design re-check (see bottom).

## Project Structure

### Documentation (this feature)

```text
specs/004-service-logos/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (icon/logo contract)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# MODIFIED: demonstrate and encourage dashboardicons.com logo URLs for services
config/example.yaml            # MODIFIED: service `icon` values -> dashboardicons.com (jsDelivr) URLs

# MODIFIED: logo behavior/docs for services
README.md                      # MODIFIED: document assigning remote-URL logos + dashboardicons.com

# Tests covering the logo (icon-as-URL) contract
tests/
├── unit/test_views_services.py    # MODIFIED: assert any remote URL renders as logo <img>
├── unit/test_security.py          # MODIFIED (as needed): logo URL validation/sanitization
└── (tests that already assert monogram fallback remain)
```

**Application code note**: the template already renders a URL-`icon` as an `<img>` with an inline `onerror` fallback to the monogram (see `app/templates/index.html`), and `app/security.py::validate_url` + the `is url` Jinja test already gate that. If the implementation confirms this is sufficient, **no application code change is required** — the feature is delivered through tests, example config, and docs. Any necessary template/schema hardening is decided during implementation and covered by the new tests.

**Structure Decision**: Keep the single-project layout. Logo support is a thin, deliberate enhancement layered over the existing per-service `icon` field: validate, render remote URLs as logos, fall back to monogram, and document dashboardicons.com as the recommended source. No structural reorganization.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No Constitution Check violations; this table is intentionally empty. (Re-checked after Phase 1 — no violations.)
