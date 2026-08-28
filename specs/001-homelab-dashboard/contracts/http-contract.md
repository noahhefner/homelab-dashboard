# HTTP Interface Contract

**Date**: 2026-08-28
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

The dashboard exposes a minimal HTTP interface for browsers (and an optional health
check for container orchestration). There is no JSON API and no authentication.

## Routes

### `GET /` — Homepage

- **Status**: `200 OK`
- **Body**: The rendered HTML page (services + grouped bookmarks) using the UIkit
  frontend. Content is freshly derived from the current config snapshot; on config
  file change the page reflects it on the next request.
- **On config error** (malformed/invalid YAML or validation failure): returns
  `200 OK` with the error page, or appropriate error status as determined at
  implementation — always a readable message, never a blank/crash (FR-010).

### `GET /health` — Health check (optional)

- **Status**: `200 OK`
- **Body**: a small plain-text/JSON acknowledgement (`OK`).
- Used by container/Docker healthcheck; confirms the process is up. Does not require
  reading the config.

### Static assets

- `GET /static/<path>` — serves vendored UIkit CSS/JS and app assets (Flask default).
- Referenced from the homepage template.

## Behavior & Security

- All dynamic content is HTML-escaped server-side before rendering.
- No authentication, sessions, or cookies required (out of scope per user).
- External/service/bookmark URLs are never followed by the server; they are rendered as
  client-side links opened in a new tab.
