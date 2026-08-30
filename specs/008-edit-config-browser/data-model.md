# Data Model: Edit Config From Browser

**Feature**: [spec.md](spec.md) · **Phase 1** · **Date**: 2026-08-30

## Overview

The feature introduces an opt-in write path for a single YAML config file plus a
bounded backup, and one new config flag that controls whether editing is exposed. It
adds no database and no new persisted entity beyond the config file itself and the
backup copy.

## Entities

### Config File (existing, now also writable)

The single dashboard config the running app already loads (`CONFIG_PATH`).

| Field | Type | Meaning |
|-------|------|---------|
| `path` | string | Absolute config path (existing `ConfigLoader.path`). |
| `raw` | string | The current file bytes (text) as read from disk. |
| `readable` | bool | Whether the file exists and can be read. |
| `writable_supported` | bool | Whether the parent directory allows atomic write (informational, surfaced in the UI). |

**Operations** (new): read current raw content; atomically replace content with validated
input; (implied) the dashboard re-parses on next request via the existing mtime/size stat.

**Validation rules** (before any write):
1. Must parse with `yaml.safe_load` (syntax).
2. Must pass the existing `parse_dashboard` (dashboard config format: top-level mapping,
   `title`, `services[]`, `bookmark_groups[]` with required fields/types).
3. Empty/invalid/interpretation-failure → **reject**, no write, preserve previous bytes.

### Editor-Enable Flag (new config option)

A boolean in the config that gates the edit capability (spec FR-010 / Q1 → Option B).

| Key | Type | Default | Meaning |
|-----|------|---------|---------|
| `editor` (or `edit_config`) | boolean | `false` | When `true`, the save route and the editor UI (edit controls) are exposed. When `false`/absent, editing is disabled and only viewing is available. |

**Validation rules**:
- Must be a boolean if present.
- Its default is `false` (opt-in); absence must not enable editing.
- Because it is part of the same validated config, an invalid value is caught by
  `parse_dashboard` and surfaced rather than silently enabling/disabling editing.
- The flag is read by the backend to decide whether to expose save; it is never used to
  gate the (read-only) config view.

### Last-Known-Good Backup (new)

A bounded copy of the most recent valid config, retained to support recovery (FR-006).

| Field | Type | Meaning |
|-------|------|---------|
| `path` | string | Backup path derived from config path (e.g., `<config>.backup.yaml`). |
| `content` | string | The last valid config content before a subsequent overwrite. |

**Rules**:
- Written only when a newly validated config is about to replace the current one.
- Holds the previous valid content so a later bad edit can be reverted to it.
- Bounded (single recent copy by default), per spec Assumptions.

## State Transitions

`GET /config` → returns current raw + enabled flag + writability info (read-only).

```
Disable (default)
    │  GET /config → view raw         (edit controls hidden)
    ▼
[editor flag = true]  ───────────►  Edit enabled
    │  POST /config/save
    ▼
 ┌ Validate (safe_load + parse_dashboard)
 │   ├─ fail ─► 400 { error } ; on-disk config UNCHANGED
 │   └─ pass ─► backup old → atomic os.replace(new)
 │                  ▼
 │           dashboard re-parses on next request (hot reload)
 └─ done
```

## Relationship to Existing Model

- Reuses `DashboardConfig` / `Service` / `BookmarkGroup` / `Bookmark` parsing via
  `parse_dashboard` (no schema duplication).
- Reuses `ConfigLoader`: the write path replaces the file; the loader's existing
  mtime/size stat picks the change up with no restart.
- Reuses `escape_html` / `validate_url` for any value rendered back into the page
  (Security Requirements, FR-009).
