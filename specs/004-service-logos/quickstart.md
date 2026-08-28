# Quickstart / Validation Guide: Service Logos

**Date**: 2026-08-28
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

Validation/run guide for remote-URL service logos. Details of the config semantics live
in [contracts/service-logo.md](contracts/service-logo.md) and
[data-model.md](data-model.md); implementation belongs in `tasks.md`.

## Prerequisites

- The dashboard source; Python 3.14 + `uv` (for running tests / the app).
- No new runtime dependencies. Logos are remote images loaded by the browser.

## Running Tests / The App

```bash
uv run pytest
uv run -m app.server          # with CONFIG_PATH=config/example.yaml
```

## Assigning a Logo to a Service

Set the service's `icon` field to a remote image URL. Any valid `http(s)` image URL
works. For example, a dashboardicons.com logo:

```yaml
services:
  - name: Plex
    url: "https://plex.lan:32400"
    icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg"
```

If `icon` is omitted, empty, or not a valid URL, the tile shows a monogram (first letter
of the name) — this is the fallback and does not break the page.

## Validation Scenarios

(**Spec**: FR-*, **Scenario**: US*)

### V1 — Any remote logo URL renders (US1, FR-004)

- Configure a service with an arbitrary `http(s)` image URL for `icon`.
- Load the homepage and confirm the tile renders that URL in an `<img>` logo (not a
  monogram).

### V2 — Monogram fallback for missing/non-URL logo (US1, FR-002)

- Configure a service with no `icon`, and another with a non-URL `icon` (e.g., a plain
  word).
- Load the homepage and confirm both tiles render a monogram (first letter), with no
  broken/empty tile.

### V3 — Broken logo falls back without breaking the page (US1, FR-002)

- Configure a service with a valid-format but unreachable URL for `icon`.
- Load the homepage; the page must still render, and the tile must fall back to the
  monogram (browser `onerror`) rather than show a broken image or error.

### V4 — Logo changes take effect on reload (US2, FR-003)

- Change a service's `icon` URL (or remove it) in the YAML config.
- Reload the page and confirm the tile reflects the change (or the monogram fallback),
  with no code change or rebuild.

### V5 — Unsafe logo values are never rendered as an image source (FR-005)

- Configure a service `icon` that is not a valid absolute http(s) URL (e.g.,
  `javascript:...` or a relative path).
- Load the homepage and confirm the value is NOT emitted as an `<img src>` (it falls
  back to the monogram and is safely escaped).

### V6 — Example config encourages dashboardicons.com (FR-007)

- Open `config/example.yaml` and confirm service logos use dashboardicons.com URLs
  (jsDelivr pattern), demonstrating the recommended source.
- Confirm the dashboard renders without network access to dashboardicons.com (e.g., the
  page still loads; any tile whose logo can't load shows a monogram).

## Regression

- `uv run pytest` passes, including the existing rendering contract (mobile layout /
  `/static/bootstrap/...` references) and the new/updated logo tests.
