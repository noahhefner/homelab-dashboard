# Data Model: Bookmark Link Icons

**Phase 1 output for `/specs/007-bookmark-link-icons/plan.md`**

This feature introduces no new entity or field. It renders the existing **Bookmark** `icon`
field, which is already parsed from the YAML config. The only model-relevant change is a
documented (and enforced-by-cleanup) meaning for that field.

## Entity: Bookmark (existing, semantics clarified)

| Attribute | Type | Location | Notes |
|-----------|------|----------|-------|
| `label` | string | `bookmarks[].label` | Required, non-empty (unchanged) — also the text fallback when no icon renders. |
| `url` | string (`http(s)`) | `bookmarks[].url` | Required, valid `http`/`https` URL (unchanged). |
| `icon` | string \| null | `bookmarks[].icon` | **Semantics now enforced.** Optional. A full remote image URL when present; rendered as an `<img>`. |

### `icon` semantics (new contract)

1. A full `http(s)` image URL → rendered as an `<img>` beside the bookmark label.
2. Absent / `null` → no image; the text label is shown.
3. Any other value (short word, malformed, non-`http(s)`) → **unsupported**; no `<img>` is
   emitted and the text label is shown. Such values MUST NOT remain in the repository.

## Validation rules

- The schema already parses `icon` as a string and validates nothing further (it is
  optional). The rendering layer MUST guard the value: only a valid `http(s)` URL is
  emitted as an `<img src>` (using the existing `is url`/URL validator test), mirroring the
  service-icon behavior. This is validated by tests, not by a new schema rule, to keep the
  change minimal and consistent.
- No new config keys, no new required fields, no schema change.

## Rendering / state

1. **Bookmark with a URL icon** → renders `<img src="<url>">` (lazy-loaded, with an
   `onerror` fallback to the label) next to the label.
2. **Bookmark with no icon / non-URL icon** → renders the label only (no image).
3. Each bookmark renders independently (spec FR-004).

## Related entities (unchanged)

- **BookmarkGroup**: name, icon (group-level, may also be a clean URL), collapse state,
  bookmarks. Unchanged. (Group *names/colors* are unrelated to per-bookmark link icons;
  the group `icon` is a separate, existing value.)
- **Service**: name, url, icon. Unchanged — the reference pattern for this feature.
- **DashboardConfig**: title, services, bookmark_groups. Unchanged.

## Non-changes

- No database or new server-side persistence.
- No new entity, field, config key, or dependency.
- The `BookmarkModel`/`schema` layers are unchanged; only the template, CSS, example
  config, README, and tests change.
