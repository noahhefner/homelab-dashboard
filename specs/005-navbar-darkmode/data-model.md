# Data Model: Navbar & Dark Mode

**Phase 1 output for `/specs/005-navbar-darkmode/plan.md`**

This feature changes the default value and empty-handling of the existing **Dashboard
title**, and introduces two **client-side (browser) settings** — the chosen theme and the
dropdown indicator (icon vs. carat). No new server-side entity or database is introduced.

## Entity: DashboardConfig (title semantics changed)

| Attribute | Type | Location | Notes |
|-----------|------|----------|-------|
| `title` | string | `title` (top-level YAML) | **Default changed to `"Homelab"`.** Rendered in the navbar `navbar-brand`. Must be a string once parsed; missing/`null`/empty/whitespace-only resolves to the default `"Homelab"`. HTML-escaped at render. |

### Title resolution rules

1. If `title` is present and a non-empty (after trimming) string → use it (unchanged
   custom-text behavior).
2. Otherwise (key absent, `null`, empty string, or whitespace-only string) → use the
   default `"Homelab"` (one word).

These rules preserve the existing ability to set a custom dashboard title while
introducing the required one-word default and cleaning up empty values that previously
could render as a blank heading.

## Client-side settings (no server entity)

- **Theme preference**: the user's light/dark choice. Values `light` / `dark`; persisted
  in `localStorage` (key e.g. `homelab:theme`). Persists across reloads; when absent, a
  system `prefers-color-scheme`/light default is applied. Not stored on the server.
- **Dropdown indicator**: static markup decision — the bookmark group toggle renders a
  Bootstrap Icon (e.g., `bi bi-chevron-down`) instead of the literal carat character. It
  is part of the template, not a data attribute.

## Validation rules

- `title` must be coercible to a string; trimming decides emptiness for the default.
- Rendered `title` MUST be HTML-escaped (Jinja autoescape) to prevent injection
  (Constitution Security Requirements).
- Theme values and the toggle are client-side only — no server-side validation surface;
  the JS writes only `light`/`dark` to `localStorage` and guards against storage
  unavailability (mirroring the existing collapse-state code).

## State transitions

1. **Title**: no title / empty → default "Homelab"; custom title set → that string;
   changing the config value is reflected on reload (config re-read per request).
2. **Theme**: light default (or system preference) → user toggles → switches
   `data-bs-theme` attribute and persists → reload preserves the chosen value → toggle
   again → back to the other theme.

## Non-changes

- No database, new config keys, or server-side state.
- `Service`, `Bookmark`, `BookmarkGroup` entities unchanged.
- The navbar is a rendering/structure change; it does not add a new entity.
