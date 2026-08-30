# Data Model: Bookmark Group Default State

**Phase 1 output for `/specs/006-bookmark-group-default-state/plan.md`**

This feature adds one optional attribute to the existing **BookmarkGroup** entity and
defines how it interacts with the existing client-side saved group state. No new entity or
database is introduced.

## Entity: BookmarkGroup (field added)

| Attribute | Type | Location | Notes |
|-----------|------|----------|-------|
| `name` | string | `bookmark_groups[].name` | Required, non-empty (unchanged). |
| `icon` | string \| null | `bookmark_groups[].icon` | Optional (unchanged). |
| `collapsed` | bool | `bookmark_groups[].collapsed` | **NEW.** Optional. Controls the group's initial state on page load. Default `false` (open). |
| `bookmarks` | list | `bookmark_groups[].bookmarks` | Nested bookmarks (unchanged). |

### `collapsed` semantics

1. `true` → the group starts **closed/collapsed** on page load.
2. `false` (or the field is absent / `null`) → the group starts **open/expanded**.

The value sets only the **initial** state; the group remains manually collapsible/
expandable by the user after load (unchanged from feature 002).

## Validation rules

- `collapsed` MUST be a boolean. A non-boolean value (e.g., a string) is invalid and raises
  the existing config validation error (consistent with the project's strict validation).
- Absent or `null` → treated as `false`.

## State transitions (per group, on page load and interaction)

1. **On load, no saved choice**: display the config-derived initial state (`collapsed` →
   closed; else open).
2. **On load, saved choice exists**: display the saved open/closed state (it takes
   precedence over the config default).
3. **On user toggle**: the group's state changes and that new choice is saved (feature 002
   behavior), so it becomes the saved choice on subsequent loads.
4. **On config change**: for groups with no saved choice, a reload reflects the new config
   default (the config is re-read per request — no rebuild/restart needed).

## Related entities (unchanged)

- **Bookmark**: label, URL, optional icon. Unchanged.
- **DashboardConfig**: title, services, bookmark_groups. Unchanged.
- **Saved group state**: a browser-side (localStorage) per-group open/closed value that
  takes precedence over the config default when present.

## Non-changes

- No database or new server-side persistence.
- No new config keys at the top level; the change is strictly per-group.
- Existing `Service`/`Bookmark` entities and all other behavior unchanged.
