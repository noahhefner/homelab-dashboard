# Implementation Plan: pnpm Bootstrap Assets

**Branch**: `003-pnpm-bootstrap-assets` | **Date**: 2026-08-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-pnpm-bootstrap-assets/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Replace the current approach of committing Bootstrap CSS/JS under `app/static/bootstrap/` with a pnpm-based mechanism: declare the Bootstrap version in `package.json` (tracked in source control) and provision the compiled assets into `app/static/bootstrap/` by copying them from the installable `bootstrap` package. The downloaded assets are excluded from version control (gitignored), giving easy version tracking/updating and keeping the repo lean. The Flask app continues to serve `app/static/bootstrap/` exactly as before, so the rendered page is unchanged. The container build provisions assets so deployed dashboards are always styled.

## Technical Context

**Language/Version**: 
- Backend: Python 3.14 (unchanged).
- Frontend asset management: **Node.js + pnpm** (developer tooling only — NOT a build/bundling system).

**Primary Dependencies**:
- Backend web framework: Flask 3.x (unchanged).
- Frontend UI framework: **Bootstrap 5** (same version as feature 002, 5.3.3, now managed via the `bootstrap` npm package instead of committed files).
- Package manager: **pnpm** (tracks `bootstrap` package version; provides the provisioning mechanism via `pnpm` lifecycle/scripts).
- No new Python runtime dependencies.

**Storage**: None (no database). Unchanged. pnpm uses a store + `node_modules`/`pnpm-lock.yaml` for version tracking only.

**Testing**: pytest (backend unit + integration, `uv run pytest`) — unchanged. Existing tests assert the rendered page references `/static/bootstrap/...`; these must still pass once assets are provisioned rather than committed.

**Target Platform**: Linux server (Docker host); developer machines run `node`/`pnpm` for provisioning.

**Project Type**: web application (backend + frontend), with a developer-tooling change for asset provisioning.

**Performance Goals**: Single-command provisioning on a fresh checkout; container build provisions assets with no manual step (preserve feature 001's one-command DX).

**Constraints**: 
- Must work offline at runtime (assets present in the image after provisioning).
- pnpm used ONLY for version tracking + asset copying — no bundling, transpiling, or build pipeline (user's explicit intent).
- Bootstrap asset files under `app/static/bootstrap/` must NOT be committed to source control.
- The dependency manifest (`package.json`) and `pnpm-lock.yaml` ARE committed (tracked).
- Docker build must work without committing assets (provision during image build).

**Scale/Scope**: Developer-tooling + container-build change. Affects repository layout, `.gitignore`, the Docker build, and provisioning docs; does not change the Flask app code or rendered markup.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gate 1 — Extensibility & Modularity**: pnpm is added as a bounded dependency-tracking/provisioning layer, not embedded in app modules. Version info lives in one manifest; provisioning is a dedicated, documented script. ✅

**Gate 2 — Testability (Test-First, NON-NEGOTIABLE)**: Existing integration tests verify the rendered page uses `/static/bootstrap/...`; these become the contract proving provisioning produces a working page. A provisioning check (assets present after running the provisioning command) is added. ✅

**Gate 3 — YAGNI & Simplicity**: The user explicitly wants pnpm ONLY for version tracking + asset provisioning (no build tooling). This is the minimal mechanism that meets "track versions, easy updates, don't commit assets." ✅

**Gate 4 — Security Requirements**: No new secret handling; Bootstrap assets are trusted third-party files copied into static assets (no user-supplied content). No new network exposure at runtime (provisioning happens at build/development time). ✅

**Gate 5 — DX First / Readability**: Single-command provisioning for developers; container build is self-contained (provisions its own assets); docs/quickstart updated. No friction added to the common dev loop. ✅

No violations; no Complexity Tracking table required.

## Project Structure

### Documentation (this feature)

```text
specs/003-pnpm-bootstrap-assets/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# NEW: pnpm/npm manifest + lockfile (committed; track Bootstrap version)
package.json               # NEW: declares "bootstrap": "5.3.3" + provisioning script
pnpm-lock.yaml             # NEW: generated lockfile (committed)
pnpm-workspace.yaml        # OPTIONAL: only if a workspace is needed (likely not needed)

# NEW: provisioning script that copies Bootstrap dist assets from node_modules into static
scripts/provision-bootstrap.sh   # NEW: copies node_modules/bootstrap/dist/{css,js} -> app/static/bootstrap/

app/
├── static/
│   ├── bootstrap/         # EXISTING dir, now gitignored + populated by provisioning (NOT committed)
│   ├── app.css / app.js   # unchanged
└── templates/index.html        # unchanged (already references /static/bootstrap/...)
config/example.yaml             # unchanged

# MODIFIED: ignore committed Bootstrap assets
.gitignore               # ADD: app/static/bootstrap/ (and node_modules/)

# MODIFIED: Docker build provisions assets so image is styled without committing them
Dockerfile               # MODIFIED: install node+pnpm, run provisioning during build
docker-compose.yml       # unchanged

tests/
├── integration/test_mobile_layout.py   # unchanged (asserts /static/bootstrap/ refs)
└── (new) test_asset_provisioning.py    # NEW: asserts assets present after provisioning (if requested)
```

**Structure Decision**: Keep the single-project layout. Add a minimal Node/pnpm layer at the repository root solely for version-tracking Bootstrap and provisioning its compiled assets. The provisioning script is a tiny, well-documented copy step (no build tooling). `app/static/bootstrap/` becomes gitignored and is populated by the provisioning command (or the container build). This preserves the existing Flask static-serving path while moving asset custody from version control to the package registry.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No Constitution Check violations; this table is intentionally empty.
