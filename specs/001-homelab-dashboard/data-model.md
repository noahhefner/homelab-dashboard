# Data Model: Homelab Dashboard Homepage

**Date**: 2026-08-28
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

The dashboard's entire data model is derived from a single user-edited YAML file.
There is no database. This document defines the domain entities, their fields, and
validation rules (mirroring `contracts/config-contract.md`).

## Entities

### DashboardConfig (root)

The parsed representation of the whole YAML file.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | no | Page/tab title shown in the browser and as the heading. Default: "Home Lab". |
| `services` | `list[Service]` | no | Ordered list of service tiles shown at the top. |
| `bookmark_groups` | `list[BookmarkGroup]` | no | Ordered list of named bookmark groups. |

**Logical composition**: `DashboardConfig` has-many `Service` and has-many
`BookmarkGroup`. Each `BookmarkGroup` has-many `Bookmark`.

### Service

A running service in the home server, rendered as a clickable tile.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Display name of the service (e.g., "Plex"). |
| `url` | string | yes | Destination URL opened when the tile is clicked. |
| `icon` | string | no | Icon/logo reference: a bundled icon name or an image URL. Absent → fallback monogram (first letter of `name`). |

**Validation rules**:
- `name` non-empty.
- `url` is a valid http/https URL.
- `icon`, when present, is either a known icon key or a valid image URL.

### BookmarkGroup

A named category that groups bookmarks for orderly display, especially at scale.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Group title shown as a heading (e.g., "Finances"). |
| `icon` | string | no | Optional group icon reference. |
| `bookmarks` | `list[Bookmark]` | no | Bookmarks in this group. |

**Validation rules**:
- `name` non-empty.

### Bookmark

A frequently used external site (e.g., YouTube, banking app).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `label` | string | yes | Display text shown in the bookmark link. |
| `url` | string | yes | Destination URL. |
| `icon` | string | no | Optional icon reference. Absent → default. |

**Validation rules**:
- `label` non-empty.
- `url` is a valid http/https URL.

## Relationships

```
DashboardConfig
 ├── 1..* Service
 └── 1..* BookmarkGroup
             └── 1..* Bookmark
```

## Validation & Error Handling

- The YAML must parse as a mapping (dict). Failure to parse → FR-010: clear readable
  error page instead of a blank/crash.
- All rendered strings (labels, names, URLs) are HTML-escaped; URLs are attribute-escaped
  and validated for safe protocols (http/https).
- Unknown or missing entries do not crash rendering; malformed required fields surface
  an error message.

## State / Lifecycle

This model is **immutable-value-like**: each parse produces a fresh `DashboardConfig`.
The live-reload mechanism (see `research.md` R2) replaces the current config atomically
when the file's modification time changes, so views always read a consistent snapshot.
No in-place mutation, so there are no state-transition diagrams.
