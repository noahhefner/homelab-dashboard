# Data Model: Download Config & Icon Links

**Feature**: [spec.md](spec.md) · **Phase 1** · **Date**: 2026-08-31

## Overview

This feature is **read-only and presentational**. It adds no database, no new persisted
entity, and no write path. It exposes the existing config file's raw bytes as a downloadable
attachment and renders static icon-source links on the existing `/config` page. The only
"data" involved is the already-loaded config file plus two fixed, static link URLs.

## Entities

### Config File (existing, now downloadable)

The single dashboard config the running app already loads (`CONFIG_PATH`). No new
attributes are stored; the download reads its current bytes.

| Field | Type | Meaning |
|-------|------|---------|
| `path` | string | Absolute config path (existing `ConfigLoader.path`). |
| `raw` | string | The current file bytes (text) as read from disk. |
| `readable` | bool | Whether the file exists and can be read (drives the download error path). |
| `basename` | string | `os.path.basename(path)`; used as the download filename (FR-003). |

**Operations (new)**: serve the raw bytes as an attachment download via `read_raw`; this is
the same read already performed by `view_config`, with no mutation.

**Validation rules**:
1. The download reads only the fixed, resolved `CONFIG_PATH` — never a client-supplied path.
2. The download filename is always `basename(path)`, derived server-side; it is never taken
   from request input (Security Requirements).
3. If `read_raw` cannot read the file, no partial/empty download is produced; a clear error
   is returned instead (FR-005).

### Icon Source Links (new, static)

Two fixed, trusted URLs rendered as links on the editor page (FR-006).

| Field | Type | Meaning |
|-------|------|---------|
| `dashboardicons_url` | string | `https://dashboardicons.com` |
| `homarr_dashboard_icons_url` | string | `https://github.com/homarr-labs/dashboard-icons` |

**Rules**:
- Both are static `https` destinations; no user input, no lookup.
- Rendered with `target="_blank" rel="noopener noreferrer"` (FR-007).
- Present in both editing and read-only modes (FR-008).

## State Transitions

No persistent state transitions. The download route depends on the file's current read
state at request time:

```
GET /config/download
    │  read_raw(path)
    ├─ success ─► 200 attachment; filename = basename(path); body = exact bytes
    └─ ConfigEditorError ─► error response (no empty/partial download)
```

## Relationship to Existing Model

- Reuses `ConfigLoader.path` and `read_raw` from `app/editor.py` (no schema or storage
  duplication).
- Reuses the existing `view_config` rendering pipeline and `config.html` template.
- The download adds no schema changes: `parse_dashboard` / `DashboardConfig` are untouched.
- The icon links are purely presentational template content; no backend data model change.
