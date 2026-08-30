# Bookmark Group Default State Contract

**Date**: 2026-08-30
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

Contract for the per-group configuration option that controls whether a bookmark group
starts open or closed on page load.

## Configuration

- An optional boolean `collapsed` field is supported on each `bookmark_groups[]` entry in
  the YAML config.
- Values:
  - `collapsed: true` → the group starts **closed/collapsed** on page load.
  - `collapsed: false`, `collapsed:` (null), or absent → the group starts **open**.
- `collapsed` MUST be a boolean; a non-boolean value is a config validation error.

## Validation & Safety

- Non-boolean `collapsed` values MUST be rejected via the existing config validation
  (consistent with strict parsing), never silently coerced.
- The rendered value (a boolean turned into a data attribute) is HTML-escaped; the group
  name handling is unchanged.

## Rendering / Behavior

- The group's initial state is governed by: saved user choice (if any) → else the config
  default. A saved user choice MUST take precedence over the config default (spec FR-004).
- Groups remain manually collapsible/expandable after load; the config only sets the
  initial state.
- The configured default MUST be passed to the client (e.g., as a data attribute on the
  group toggle) so the client can apply it when no saved choice exists.
- Each group's default is independent of other groups (spec FR-005).

## Example

```yaml
bookmark_groups:
  - name: Media
    collapsed: true      # starts closed
    bookmarks:
      - label: YouTube
        url: "https://www.youtube.com"
  - name: Finance        # no `collapsed` -> starts open
    bookmarks:
      - label: Bank
        url: "https://bank.example.com"
```

## Verification

- A group with `collapsed: true` and no saved choice renders collapsed on load.
- A group with `collapsed: false` (or no field) and no saved choice renders open.
- A group with a previously saved user choice keeps that choice on reload, regardless of
  its config default.
- A non-boolean `collapsed` value produces a config error.
- `uv run pytest` passes, including new/updated tests covering the above.
