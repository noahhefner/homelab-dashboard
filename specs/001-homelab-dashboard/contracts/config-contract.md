# Config Contract: `config.yaml`

**Date**: 2026-08-28
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

This contract defines the single YAML configuration file that drives the entire
dashboard. Users edit this file (typically mounted into the container via a Docker
volume) to add, remove, or reorder services and bookmarks.

## Top-level Structure

```yaml
title: "Home Lab"          # optional; page title/heading (default "Home Lab")

services:                  # optional ordered list of service tiles
  - name: Plex
    url: "https://plex.lan:32400"
    icon: plex             # optional: bundled icon key or image URL

bookmark_groups:           # optional ordered list of named groups
  - name: Finances
    icon: bank             # optional
    bookmarks:
      - label: Banking App
        url: "https://bank.example.com"
        icon: bank         # optional
```

## Fields

### `title` (optional)

- Type: string
- Page/tab title and main heading. Default: `"Home Lab"`.

### `services` (optional)

- Type: list of `Service` objects
- Ordered; rendered top-to-bottom in the services section.

A `Service`:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | yes | Display name; also used for fallback monogram. |
| `url` | string | yes | Must be a valid `http`/`https` URL. |
| `icon` | string | no | Bundled icon key or image URL. Absent/unknown → fallback monogram. |

### `bookmark_groups` (optional)

- Type: list of `BookmarkGroup` objects
- Ordered; rendered top-to-bottom.

A `BookmarkGroup`:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | yes | Group heading. |
| `icon` | string | no | Optional group icon. |
| `bookmarks` | list of `Bookmark` | no | Ordered bookmarks within the group. |

A `Bookmark`:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `label` | string | yes | Display text. |
| `url` | string | yes | Must be a valid `http`/`https` URL. |
| `icon` | string | no | Optional icon. |

## Validation Rules

1. Root MUST be a YAML mapping. Empty file → `{}` → empty dashboard (no crash).
2. `url` values MUST be valid absolute `http`/`https` URLs.
3. `name` / `label` MUST be non-empty strings.
4. Unknown top-level keys are ignored (forward-compatible).
5. Malformed structure or invalid required fields yield a **clear, readable error page**
   rather than a blank/broken page (spec FR-010).

## Rendering & Security Behavior

- All labels, names, and URLs are HTML-escaped on output.
- External URLs open in a new tab with `rel="noopener noreferrer"`.
- An absent/unreachable icon gracefully falls back to a monogram or default tile.
