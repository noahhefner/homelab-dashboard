# Dependency Manifest Contract

**Date**: 2026-08-28
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

Contract for the root `package.json` / `pnpm-lock.yaml` that track the frontend asset
dependencies.

## Requirements

- `package.json` MUST declare a pinned `bootstrap` dependency (e.g. `"5.3.3"`), with
  no version range that would silently float.
- `package.json` MUST expose:
  - `provision`: copies Bootstrap assets into `app/static/bootstrap/`.
  - `setup`: install + provision (`pnpm install && pnpm provision`).
- `package.json` MUST set `"private": true` (not published).
- `pnpm-lock.yaml` MUST be committed so `pnpm install --frozen-lockfile` is
  reproducible on any machine and in the container build.

## Exclusion Contract

- `package.json` and `pnpm-lock.yaml` are **tracked** (committed).
- `node_modules/` and the materialized `app/static/bootstrap/` are **not** committed.

## Updating the Bootstrap Version

1. Change the version: `pnpm add bootstrap@X.Y.Z` (updates `package.json` +
   `pnpm-lock.yaml`), or edit `package.json` then `pnpm install`.
2. Re-provision: `pnpm provision` (or `pnpm setup`).
3. The files in `app/static/bootstrap/` now reflect `X.Y.Z`.
