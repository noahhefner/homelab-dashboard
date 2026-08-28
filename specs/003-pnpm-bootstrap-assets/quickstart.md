# Quickstart / Validation Guide: pnpm Bootstrap Assets

**Date**: 2026-08-28
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

This guide lets you validate the pnpm-based Bootstrap provisioning end-to-end. It is a
validation/run guide — implementation belongs in `tasks.md`. Manifest details live in
[contracts/dependency-manifest.md](contracts/dependency-manifest.md) and provisioning
in [contracts/provisioning.md](contracts/provisioning.md).

## Prerequisites

- **Node.js** (≥18) and **pnpm**. Install pnpm globally once if missing:
  `npm install -g pnpm`, or use Corepack: `corepack enable`.
- The dashboard source; Python 3.14 + `uv` (for running tests / the app).

## 1. Provision Bootstrap Assets (Developer)

```bash
pnpm install      # installs the pinned bootstrap package from the lockfile
pnpm provision    # copies dist/css + dist/js into app/static/bootstrap/
```

Or the combined shortcut:

```bash
pnpm setup
```

After this, `app/static/bootstrap/css/bootstrap.min.css` and
`app/static/bootstrap/js/bootstrap.bundle.min.js` exist.

## 2. Run the Dashboard

```bash
CONFIG_PATH=config/example.yaml uv run python -m app.server
```

Open <http://localhost:5000> — the page is styled with Bootstrap via
`/static/bootstrap/...`.

## 3. Build & Run the Container (Production)

```bash
docker build -t homelab-dashboard .
docker run --rm -p 5000:5000 homelab-dashboard
```

The build provisions Bootstrap itself — the deployed page is styled with no manual
step.

## Validation Scenarios

(**Spec**: FR-*, **Scenario**: US*)

### V1 — Fresh checkout provisions cleanly (US1)

- On a fresh clone (Bootstrap assets absent from version control), run `pnpm setup`.
- Confirm both files exist in `app/static/bootstrap/`.
- Confirm the page renders styled.

### V2 — Assets stay out of version control (US3)

- After `pnpm setup`, run `git status`.
- Confirm no `app/static/bootstrap/` files appear as untracked or modified.
- Confirm `package.json` + `pnpm-lock.yaml` are tracked.

### V3 — Version is visible and updatable (US2)

- Read the `bootstrap` version in `package.json`.
- Bump it (e.g. `pnpm add bootstrap@<new>`), run `pnpm provision`.
- Confirm `app/static/bootstrap/` files now come from the newer version and the page
  still renders.

### V4 — Idempotent re-provisioning (FR-004)

- Run `pnpm provision` twice; the second run produces identical, consistent output and
  leaves no partial state.

### V5 — Container build styled without manual step (FR-007, SC-004)

- `docker build` then `docker run`; the homepage is fully styled with no
  post-build provisioning.

### V6 — Existing rendering tests still pass

- `uv run pytest` passes, including the integration test asserting the homepage
  references `/static/bootstrap/...`.

## Automated Tests

```bash
uv run pytest
```
