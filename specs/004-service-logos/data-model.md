# Data Model: Service Logos

**Phase 1 output for `/specs/004-service-logos/plan.md`**

This feature evolves the meaning of the existing **Service icon** attribute so it
reliably carries a remote logo URL. It introduces **no new entity** and no new
runtime data model beyond what feature 001 defined.

## Entity: Service (unchanged shape, clarified `icon` semantics)

| Attribute | Type | Location | Notes |
|-----------|------|----------|-------|
| `name` | string | `services[].name` | Required, non-empty. |
| `url` | string | `services[].url` | Required, must be a valid absolute `http(s)` URL. |
| `icon` | string \| null | `services[].icon` | **Logo value.** Optional. When set to a valid absolute `http(s)` URL, it is rendered as the service logo image; otherwise (null, empty, or a non-URL) the tile shows a monogram fallback (first letter of `name`). |

### `icon` as a logo — interpretation rules

1. If `icon` is a valid absolute `http(s)` URL (via `validate_url`):
   - Rendered as an `<img>` logo on the service tile, with `loading="lazy"` and an
     `onerror` fallback to the monogram if the image fails to load.
2. Otherwise (null / empty / non-URL string):
   - Rendered as a monogram (first letter of `name`), consistent with feature 001.

These rules preserve backward compatibility: existing configs that use a plain-word
`icon` still render a monogram; configs using a URL already render an image.

## Related entities (unchanged from feature 001)

- **Bookmark**: label, URL, optional `icon`. Not the focus of this feature, but it
  shares the same URL-vs-monogram `icon` semantics; untouched except where tests
  confirm consistency.
- **BookmarkGroup**: name, optional `icon`. Unchanged.
- **DashboardConfig**: title, services, bookmark_groups. Unchanged.

## Validation rules

- A service `icon`/logo is NOT validated as strongly as `url`: it may be any string or
  absent (feature 001 allows the monogram path). Only when it is used as an `<img>` src
  must the value pass `validate_url` (http/https + netloc) to avoid rendering
  javascript:/data: or malformed sources.
- Rendered logo `src` and service `name` MUST be HTML-escaped to prevent injection
  (Constitution Security Requirements).

## State transitions

1. **No logo configured** (`icon` absent or non-URL): tile shows monogram.
2. **Logo configured as a valid remote URL**: tile shows the `<img>` logo; on image
   load failure, `onerror` swaps to the monogram for the remainder of the visit.
3. **Logo changed/removed in config**: on reload the tile re-renders to the new value
   or the monogram — no restart or rebuild needed (config is re-read per request).

## Non-changes

- No new database, storage, or file assets. Logos are remote URLs only.
- No change to Bookmark/BookmarkGroup rendering beyond shared `icon` semantics.
- No bundled logo library; dashboardicons.com is a documented recommendation only.
