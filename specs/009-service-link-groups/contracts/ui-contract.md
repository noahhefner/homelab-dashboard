# UI Contract: Tile Link Groups

**Feature**: [spec.md](../spec.md) · **Phase 1** · **Date**: 2026-08-31

## Overview

The UI contract defines how the dashboard homepage renders tile groups (renamed from
"services"/"service groups"), the hardcoded "Bookmarks" heading, and the rebranded
terminology. This builds on the existing Bootstrap 5 grid layout (feature 002) and the
icon/monogram rendering (features 001/004/007), with all `service-*` classes renamed to
`tile-*`.

## Homepage Layout (same grid, renamed classes, added group sections)

- The main content section (tiles) uses the existing grid classes `col-12 col-lg-9`
  (full width on mobile, left ~75% on desktop). **Unchanged**, but `aria-label` becomes
  `"Tiles"`.
- The bookmark section uses `col-12 col-lg-3` (below apps on mobile, right column on
  desktop). **Unchanged**.
- A new "Bookmarks" heading is inserted at the top of the bookmark column, above the
  accordion.

### Tile Rendering (renamed classes)

The tile link uses the `app-tile tile` (formerly `app-tile service-tile`) anchor with
`tile-icon`, `tile-monogram`, and `tile-name` (formerly `service-*`) classes. All links
open in a new tab (`target="_blank"` + `rel="noopener noreferrer"`), for both internal
and external targets (spec FR-013).

### Tile Group Rendering (new)

Within the main tiles section:

1. **Flat `tiles`** render first, in the existing unlabeled grid.
2. **Each `tile_groups` entry** renders as a labeled block, in declared order:

```html
<div class="tile-group">
  <h3 class="group-title">
    <img .../>  <!-- optional group icon, lazy-loaded with monogram fallback -->
    Media       <!-- group name (escaped) -->
  </h3>
  <div class="row g-3">
    <!-- tile grid, same structure as flat tiles -->
  </div>
</div>
```

**Contract rules**:
- The group header is a **plain heading** (`<h3 class="group-title">`) with the group
  name; it is NOT a collapsible Bootstrap accordion button (spec FR-010).
- There is **no collapse/expand control** and no `data-bs-toggle` on tile groups. The only
  collapsible element on the page is the bookmark accordion.
- The group name and icon are HTML-escaped on render (Security Requirements; group name
  is validated as a non-empty string).
- A group's tiles use the same `col-6 col-sm-4 col-md-3 col-xl-2` grid and
  `app-tile tile` classes as flat tiles, so sizing/behavior is uniform.

---

## "Bookmarks" Heading (new, hardcoded)

- A heading reading **"Bookmarks"** is rendered directly above the bookmark accordion
  whenever `bookmark_groups` is non-empty (spec FR-011).
- The text is **hardcoded** and NOT configurable.
- When `bookmark_groups` is empty, the heading is omitted (the existing
  "No bookmarks configured yet." message is shown instead).

```html
<aside aria-label="Bookmarks" class="col-12 col-lg-3">
  <h3 class="group-title">Bookmarks</h3>
  <div class="accordion bookmark-accordion" id="bookmark-accordion">
    <!-- existing bookmark groups (collapsible) -->
  </div>
</aside>
```

---

## Rebrand (renames applied)

The former "services" terminology is renamed to "tiles" across the UI and docs:

| Surface | Before | After |
|---------|--------|-------|
| Main section `aria-label` | `Services` | `Tiles` |
| `<meta name="description">` | "...links to local services and bookmark groups." | "...links to local tiles and bookmark groups." |
| HTML comment above main section | `<!-- Services: main area ... -->` | `<!-- Tiles: main area ... -->` |
| README feature bullet | `**Services**: ...` | `**Tiles**: ...` |
| README config comment | `# Put links to your homelab services here.` | `# Put links to your homelab tiles here.` |
| `config/example.yaml` comment | `# ...services...` | `# ...tiles...` |

Unlike the pre-clarification (backward-compat) design, this rebrand **also** renames the
internal identifiers and CSS classes (`service-*` → `tile-*`, `Service`→`Tile`, etc.) —
per spec FR-001/FR-012 (Clarification Q1 → A).

---

## Accessibility

- The tiles `<section aria-label="Tiles">` and bookmark `<aside aria-label="Bookmarks">`
  use explicit accessible labels.
- Group headings (`<h3 class="group-title">`) provide a clear document outline.
- The "Bookmarks" heading is a real heading element, not a styled `<div>`, so it is
  available to assistive tech.
- No interaction is required to reveal tile groups (always visible), matching FR-010.
