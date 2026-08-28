# HTTP Interface Contract

**Date**: 2026-08-28
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

The dashboard exposes a minimal HTTP interface for browsers (and an optional health
check for container orchestration). There is no JSON API and no authentication.
The contract from feature 001 is unchanged; the only difference is the frontend
assets served (Bootstrap instead of UIkit).

## Routes

### `GET /` — Homepage

- **Status**: `200 OK`
- **Body**: The rendered HTML page (services + grouped bookmarks) using the **Bootstrap 5**
  frontend. Layout: bookmarks in a right-hand column on desktop (`lg`+); below the apps on
  mobile. Content is freshly derived from the current config snapshot; on config file
  change the page reflects it on the next request.
- **On config error** (malformed/invalid YAML or validation failure): returns a readable
  error page, never a blank/crash (FR-010).

### `GET /health` — Health check (optional)

- **Status**: `200 OK`
- **Body**: a small plain-text ack (`OK`).
- Does not require reading the config.

### Static assets

- `GET /static/<path>` — serves vendored **Bootstrap** CSS/JS (`/static/bootstrap/...`)
  and app assets (Flask default). No remote/CDN asset references (offline-capable).

## Behavior & Security

- All dynamic content is HTML-escaped server-side before rendering.
- No authentication, sessions, or cookies required (out of scope per user).
- External/service/bookmark URLs are never followed by the server; they are rendered as
  client-side links opened in a new tab.
