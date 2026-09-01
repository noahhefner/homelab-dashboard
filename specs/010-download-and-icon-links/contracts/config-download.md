# Contract: Download Config & Icon Links (UI + Download Endpoint)

**Feature**: [spec.md](../spec.md) · **Phase 1** · **Date**: 2026-08-31

This defines the browser-facing contract for downloading the config YAML from the editor
page and for the icon-source links shown on the same page. The download is a read-only
server route; the browser is never trusted for filenames or paths.

---

## 1. Download route

**`GET /config/download`**

**Purpose**: Return the current config YAML file as a downloadable attachment (spec FR-001).

**Behavior**:
- Reads the exact on-disk bytes via `read_raw`.
- Responds with `Content-Disposition: attachment; filename="<basename.of.config.path>"`
  (e.g., `config/example.yaml` → `example.yaml`) — FR-003, derived server-side.
- Returns the raw bytes unchanged (FR-002) with an appropriate YAML mimetype
  (`application/x-yaml` or `text/yaml`).
- Works whether or not the `editor` flag is enabled (FR-004).

**Success response** — `200`:

```
HTTP/1.1 200 OK
Content-Disposition: attachment; filename="example.yaml"
Content-Type: text/yaml; charset=utf-8

<exact on-disk YAML bytes>
```

**Failure responses** (FR-005 — never an empty/partial download):

| Status | Behavior | When |
|--------|----------|------|
| `404` | Clear error message | Config file does not exist |
| `500` | Clear error message | Config file unreadable / read error |

---

## 2. Editor page UI contract

**`GET /config`**

**Purpose**: Show the current config, plus the download button and icon-source links, in
both editing and read-only modes.

**Download button** (FR-001, FR-004, FR-008):
- A clearly visible control labeled "Download config" linking to `GET /config/download`;
  present in both editing and read-only modes.
- Suggested markup: an `<a href="{{ url_for('dashboard.download_config') }}">` styled as a
  Bootstrap button with a download icon (`bi-download`).

**Icon sources section** (FR-006, FR-007, FR-008):
- A small section labeled e.g. "Icon sources" with links to:
  - `https://dashboardicons.com`
  - `https://github.com/homarr-labs/dashboard-icons`
- Each link uses `target="_blank" rel="noopener noreferrer"` so it opens in a new tab
  without navigating away, and does not leak `window.opener`.
- Both links are visible in editing and read-only modes.

**Error state**: When the config is unreadable, `view_config` keeps its existing "Unable to
load the configuration" alert; no download button or icon-free rendering is required in that
error branch (the download/icon controls appear on the normal page render).

---

## 3. Contract tests to enforce (spec FR-001/002/003/004/006/007/008/009)

1. `GET /config/download` returns `200` with `Content-Disposition: attachment; filename="<basename>"` and a body exactly equal to the on-disk config bytes.
2. `GET /config/download` works with editing **disabled** (no `editor` flag) — returns the same bytes (FR-004).
3. `GET /config/download` with a missing/unreadable config file returns a clear error and does **not** return an empty/partial body (FR-005).
4. `GET /config` renders the download button and the two icon-source links in both editing and read-only modes (FR-001/006/008).
5. Each icon-source link has `target="_blank"` and `rel="noopener noreferrer"` (FR-007).
6. The download filename is derived from the config path basename, never from client input (FR-003; Security).
