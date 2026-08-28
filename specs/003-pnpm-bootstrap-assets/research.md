# Research: pnpm Bootstrap Assets

**Phase 0 output for `/specs/003-pnpm-bootstrap-assets/plan.md`**

Purpose: resolve the technical unknowns raised during planning and record decisions
for pnpm-based Bootstrap asset provisioning. Every decision below works against the
constraint that pnpm is used **only** for version tracking + asset provisioning — no
build/bundling tooling (user's explicit intent and constitution Principle V).

## 1. Managing the Bootstrap Version

- **Decision**: Declare Bootstrap as a `dependency` in a root `package.json`
  (`"bootstrap": "5.3.3"`, pinned), and commit `package.json` + `pnpm-lock.yaml`.
  pnpm installs the `bootstrap` package into `node_modules`, from which we copy its
  compiled distribution assets.
- **Rationale**: A committed `package.json` + compatible lockfile is the standard,
  minimal way to declaratively pin a third-party package version and make updates
  repeatable (`pnpm add bootstrap@<new>`, re-provision). This is exactly "track
  versions, easy updates" without introducing a build pipeline. The `bootstrap` npm
  package ships precompiled `dist/css/bootstrap.min.css` and
  `dist/js/bootstrap.bundle.min.js`, so no compilation is needed.
- **Alternatives considered**:
  - Keep committing assets (current 002 behavior): rejected — user explicitly wants to
    avoid committing assets.
  - Use a script that downloads from a CDN: rejected — brittle, not version-tracked,
    and duplicates pnpm's job.

## 2. Provisioning the Assets (the copy step)

- **Decision**: Add a small, dedicated shell script `scripts/provision-bootstrap.sh`
  that copies the needed files from `node_modules/bootstrap/dist/` into
  `app/static/bootstrap/`:
  - `dist/css/bootstrap.min.css` → `app/static/bootstrap/css/bootstrap.min.css`
  - `dist/js/bootstrap.bundle.min.js` → `app/static/bootstrap/js/bootstrap.bundle.min.js`
  Expose it as an npm script: `"provision": "scripts/provision-bootstrap.sh"`, run via
  `pnpm provision`.
- **Rationale**: A plain copy preserves the exact files feature 002 served, so the
  Flask app and templates are unchanged. Keeping the copy logic in one obvious script
  makes the mechanism transparent and auditable (readability, principle II). Using an
  npm script name (`pnpm provision`) gives an easy, discoverable command.
- **Alternatives considered**:
  - `postinstall` hook that auto-provisions: convenient, but a hidden side effect that
    is harder to reason about; a named `provision` script is more explicit and still
    one command. (Decision: named script; may note `postinstall` as optional.)
  - pnpm `package.json` `files`/`sideEffects` etc.: N/A — we are not publishing a package.

## 3. Keeping Assets Out of Source Control

- **Decision**: Add `app/static/bootstrap/` and `node_modules/` to `.gitignore`, then
  remove the currently committed Bootstrap files from tracking (`git rm -r
  --cached app/static/bootstrap`). `package.json` and `pnpm-lock.yaml` remain tracked.
- **Rationale**: Gitignoring the provisioned/compiled assets while tracking the
  manifest keeps the package registry as the single source of truth (spec FR-003,
  US3). `git rm --cached` (not the worktree) stops tracking the existing files without
  deleting the local copy until reprovisioned.
- **Security note**: gitignore patterns are broad-path-based; ensure the ignore rule
  targets exactly `app/static/bootstrap/` so app source and other static assets stay
  tracked.

## 4. Container Build Provisions Its Own Assets

- **Decision**: Adopt a **two-stage Docker build**:
  - Stage 1 (Node): `FROM node:22-slim`, set up pnpm (via `corepack enable`),
    copy `package.json` + `pnpm-lock.yaml`, run `pnpm install --frozen-lockfile` and
    the provisioning script into a build dir, and copy the result out.
  - Stage 2 (Python): keep the existing `python:3.14-slim` stage, copy the provisioned
    Bootstrap assets from stage 1 into `app/static/bootstrap/`, then copy the app and
    config as today.
- **Rationale**: This keeps the production image slim (no Node runtime at runtime), is
  reproducible (frozen lockfile), and ensures the deployed dashboard is always styled
  from a fresh checkout/CI with **no separate provisioning step** (spec FR-007, SC-004).
  It preserves the existing single `docker build` / `docker compose up` DX.
- **Alternatives considered**:
  - Install Node+pnpm into the Python image: larger runtime image; rejected (keeps
    runtime lean).
  - Commit assets and skip provisioning in Docker: rejected (defeats the feature goal).
  - Multi-stage via `COPY --from` of just the produced assets: chosen — minimal and clean.

## 5. Impact on the Flask App and Tests

- **Decision**: No change to Flask wiring or `app/templates/index.html` (it already
  references `/static/bootstrap/...`). Existing tests asserting those references
  continue to define the "styled page" contract; a new check confirms assets exist
  after provisioning.
- **Rationale**: The app is identical; only asset custody changes (committed → pnpm).
  Backend/config/template/testing for rendering are untouched.
- **Alternative considered**: none — changing the app is out of scope (spec Assumptions).

## 6. Developer Prerequisites

- **Decision**: Document that provisioning requires `node` (≥18) and `pnpm` installed.
  The quickstart lists installing pnpm (e.g., `npm i -g pnpm` or `corepack enable`).
- **Rationale**: Expo qualitative: a fresh checkout must run one command (`pnpm
  install` + `pnpm provision`, or a combined `pnpm setup` script) to get assets (spec
  US1). Combined convenience script: `"setup": "pnpm install && pnpm provision"`.
