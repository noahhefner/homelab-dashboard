# Data Model: pnpm Bootstrap Assets

**Phase 1 output for `/specs/003-pnpm-bootstrap-assets/plan.md`**

This feature is a **developer/build tooling change**. It introduces no application
data entities and does not alter the dashboard's runtime data model (which is
unchanged from feature 001/002: `DashboardConfig`, `Service`, `BookmarkGroup`,
`Bookmark`). Instead, the "state" involved is the dependency/provisioning model
described below.

## Dependency & Provisioning Model

### Dependency Manifest (`package.json`, committed)

Declares the frontend assets the dashboard depends on.

| Attribute | Type | Notes |
|-----------|------|-------|
| `name` | string | Project name (`homelab-dashboard`). |
| `version` | string | Manifest version (independent of the app). |
| `private` | boolean | `true` — not published as a package. |
| `dependencies.bootstrap` | string | Pinned version, e.g. `"5.3.3"`. |
| `scripts.provision` | string | Command that copies Bootstrap assets into `app/static/bootstrap/` (e.g. `scripts/provision-bootstrap.sh`). |
| `scripts.setup` | string | Convenience command: install + provision (`pnpm install && pnpm provision`). |

### Lockfile (`pnpm-lock.yaml`, committed)

A deterministic record of the resolved dependency tree, including the exact
`bootstrap` version and its transitive packages. Ensures `pnpm install
--frozen-lockfile` reproduces the same files on any machine and in the container
build (reproducibility).

### Provisioning Script (`scripts/provision-bootstrap.sh`, committed)

Copies the compiled distribution from the installed `bootstrap` package to the
served static directory.

| Source (from `node_modules/bootstrap/dist/`) | Destination (`app/static/bootstrap/`) |
|------------------------------------------------|----------------------------------------|
| `css/bootstrap.min.css`                         | `css/bootstrap.min.css`                |
| `js/bootstrap.bundle.min.js`                    | `js/bootstrap.bundle.min.js`           |

### Static Assets (`app/static/bootstrap/`, NOT committed)

The materialized files served by Flask at `/static/bootstrap/...`. These are
**gitignored**; they exist locally only after provisioning (developer) or are
produced during the container build.

## State Transitions

1. **Fresh checkout**: `app/static/bootstrap/` absent (gitignored). Dashboard would
   render unstyled until provisioned.
2. **Provision** (`pnpm install && pnpm provision`): `node_modules` populated from the
   locked deps; Bootstrap dist files copied to `app/static/bootstrap/`. Page styled.
3. **Version bump**: edit `package.json` (or `pnpm add bootstrap@X.Y.Z`) then
   re-provision; `pnpm-lock.yaml` updates; assets replaced with the new version.
4. **Container build**: the Node stage provisions assets, which are copied into the
   Python image — the deployed dashboard is styled with no manual step.

## Validation Rules (provisioning correctness)

- Provisioned `css/bootstrap.min.css` and `js/bootstrap.bundle.min.js` MUST exist in
  `app/static/bootstrap/` after provisioning.
- Version in `package.json` and the files in `app/static/bootstrap/` MUST agree (re-run
  provisioning reconciles any drift).
- `app/static/bootstrap/` MUST not appear as tracked/untracked in version control after
  provisioning.

## Non-Changes

- Runtime data model and validation (feature 001/002) are identical.
- No new Python dependencies, no application code changes, no template/markup changes.
