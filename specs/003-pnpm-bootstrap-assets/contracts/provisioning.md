# Provisioning Contract

**Date**: 2026-08-28
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

Contract for the provisioning mechanism that produces the served Bootstrap assets,
and for the container build that consumes it.

## Inputs

- `node_modules/bootstrap/dist/` (present after `pnpm install`).

## Outputs

After `pnpm provision`, the following files MUST exist:

| Output Path | Source |
|-------------|--------|
| `app/static/bootstrap/css/bootstrap.min.css` | `node_modules/bootstrap/dist/css/bootstrap.min.css` |
| `app/static/bootstrap/js/bootstrap.bundle.min.js` | `node_modules/bootstrap/dist/js/bootstrap.bundle.min.js` |

## Behavior

- Provisioning is idempotent: re-running it yields the same files as the current
  dependency version and reconciles any drift (spec FR-004).
- On failure (e.g., no network / missing package), provisioning MUST exit with a
  non-zero status and an actionable message, and MUST not leave a partially-updated
  directory. Recommend writing to a temp dir and atomically moving into place if
  strong atomicity is desired (implementation detail).
- After provisioning, version control status MUST show no tracked/untracked changes
  under `app/static/bootstrap/` (spec FR-003, SC-003).

## Container Build

- The Dockerfile MUST provision Bootstrap assets during the build so the resulting
  image contains a styled dashboard with no post-build manual step (spec FR-007,
  SC-004).
- Recommended: a Node build stage runs `pnpm install --frozen-lockfile` + the
  provisioning script, and the Python runtime stage copies only the produced assets
  (keeps the runtime image lean).

## Serving

- The Flask app continues to serve the same `/static/bootstrap/...` paths (unchanged).

## Verification

- `pnpm setup` (or `pnpm install && pnpm provision`) on a fresh checkout yields both
  output files and a styled homepage.
- `uv run pytest` still passes, including the integration test asserting the rendered
  page references `/static/bootstrap/...`.
