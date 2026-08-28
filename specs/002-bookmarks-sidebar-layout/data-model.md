# Data Model: Bookmarks Sidebar Layout

**Phase 1 output for `/specs/002-bookmarks-sidebar-layout/plan.md`**

This feature is **presentation-only**. There are **no changes** to the application
data model, configuration schema, or validation rules. The entities below are
unchanged from feature 001 and are documented here for completeness so downstream
consumers (quickstart, tests) understand what the template renders.

## Entities (unchanged from feature 001)

### DashboardConfig

The top-level validated configuration produced from the single YAML file.

| Attribute | Type | Notes |
|-----------|------|-------|
| `title` | `str` | Page `<title>`/heading. Default `"Home Lab"`. |
| `services` | `list[Service]` | Apps shown in the main left area. |
| `bookmark_groups` | `list[BookmarkGroup]` | Bookmark groups shown in the sidebar (desktop) / below (mobile). |

### Service

A running homelab service rendered as a clickable tile.

| Attribute | Type | Notes |
|-----------|------|-------|
| `name` | `str` | Display name (non-empty). |
| `url` | `str` | Validated http/https URL. |
| `icon` | `str \| None` | Optional icon/image reference. |

### BookmarkGroup

A named category containing bookmarks.

| Attribute | Type | Notes |
|-----------|------|-------|
| `name` | `str` | Non-empty group name. |
| `bookmarks` | `list[Bookmark]` | Bookmarks in this group. |
| `icon` | `str \| None` | Optional icon reference. |

### Bookmark

A frequently used external site inside a group.

| Attribute | Type | Notes |
|-----------|------|-------|
| `label` | `str` | Non-empty display label. |
| `url` | `str` | Validated http/https URL. |
| `icon` | `str \| None` | Optional icon reference. |

## Validation Rules (unchanged from feature 001)

- `title` optional; defaults to `"Home Lab"`.
- `services` and `bookmark_groups` optional lists; default to empty.
- `name`: required non-empty string.
- `url`: required, must pass `app.security.validate_url` (valid http/https URL).
- `icon`: optional string when present.

## State Transitions (frontend-only, unchanged from feature 001)

- **Bookmark group collapse state**: each group's open/closed state is
  persisted to `localStorage` under key `homelab:group:collapsed:<group-name>`
  and re-applied on load. This behavior is preserved by the new Bootstrap Collapse
  implementation.

## Deliberate Non-Changes

- No new entities, fields, or relationships are introduced.
- The YAML schema/contract (see `contracts/`) is identical to feature 001.
- Backend modules (`config.py`, `model.py`, `schema.py`, `views.py`) are untouched.
