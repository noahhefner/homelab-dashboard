# Research: Bookmark Link Icons

**Phase 0 output for `/specs/007-bookmark-link-icons/plan.md`**

Purpose: resolve the technical decisions needed to render bookmark link icons just like
the homelab service icons, within the existing Flask/Bootstrap dashboard and the
Constitution's principles.

## 1. What a Bookmark Icon Is

- **Decision**: A bookmark icon is a full remote image URL (`http(s)`), rendered as an
  `<img>` beside the bookmark's text label — exactly the treatment already applied to
  homelab service icons. Short-word icon values (e.g., `youtube`, `bank`, `play`) are NOT
  a supported icon form anywhere in this project; any non-URL icon value falls back to the
  plain text label (spec FR-007).
- **Rationale**: The user explicitly asked for icons "just like the icons on the homelab
  links," which are remote image URLs (feature 004). The `Bookmark` model already carries
  an `icon` string field and the schema already parses it, so no new config shape is
  needed. Keeping a single, URL-only form avoids a second (unsupported) icon vocabulary
  and matches the "one way to do it" readability principle (Principle II).
- **Alternatives considered**:
  - Map short words to dashboard-icons URLs: rejected — the user explicitly said short
    words are unsupported everywhere and should be replaced with full URLs.
  - Bootstrap icon-class names (`bi-*`): rejected — a second icon style that deviates from
    the homelab image approach and adds a font-class mechanism with no request backing it.
  - A dual representation (URL or class): rejected (YAGNI; violates the single-form
    decision above).

## 2. How to Render the Icon in the Template

- **Decision**: In `app/templates/index.html`, inside each bookmark `<a>`, conditionally
  emit an `<img>` when `bookmark.icon` is a valid URL, otherwise emit only the
  existing text label. Reuse the existing `is url` Jinja test already registered on the
  app factory, and the lazy-loading + inline `onerror` fallback pattern used for service
  icons.
- **Rationale**: The template already knows whether an icon is a valid image URL via
  `service.icon and service.icon is url`; applying the same test to `bookmark.icon` is the
  smallest, most consistent change. Because the bookmark's text label is always present,
  no separate monogram element is needed — when the image is absent or fails, the label
  itself is the fallback (spec FR-002).
- **Alternatives considered**: a server-side lookup/transform of the icon — rejected
  (unnecessary; the URL renders directly); adding a monogram for failures — rejected
  (redundant since the label is right there, and it would clutter the list).

## 3. Removing Unsupported Short-Word Icons From the Repo

- **Decision**: Replace every short-word icon value found in `config/example.yaml` (both
  the `bookmark_groups[].icon` and `bookmarks[].icon` entries) with a full remote image
  URL (e.g., dashboard-icons) where a suitable icon exists, and remove the `icon` value
  where none exists. Apply the same cleanup to any documentation (README) that shows
  short-word icons.
- **Rationale**: The clarified scope (spec FR-008) requires the repo to contain no
  short-word icons. The example config currently uses values like `icon: play`,
  `icon: youtube`, `icon: bank`, etc., which are not rendered and are now explicitly
  unsupported. Correcting the example keeps it a valid, runnable illustration of the
  supported behavior (Principle I).
- **Alternatives considered**: leaving short words in place — rejected (they are
  unsupported yet appear to be valid examples, which would mislead users); documenting
  them as "ignored" — rejected (the user wants them removed, and keeping dead example
  values is contrary to YAGNI/clarity).

## 4. Validation and Safety of the Icon Value

- **Decision**: Only render the icon as an `<img src>` when it passes the existing `url`
  validator (an absolute `http`/`https` URL). Unsafe values (e.g., `javascript:`) and
  non-URL values are never emitted as an image source; the bookmark falls back to its text
  label. Output is HTML-escaped by Jinja.
- **Rationale**: This mirrors the proven service-icon behavior already covered by
  `test_views_services.py` (`test_non_url_icon_renders_monogram_not_img`,
  `test_unsafe_icon_value_not_rendered_as_img_src`). Applying the same guard to bookmarks
  satisfies the Security Requirements without new machinery (spec FR-005).
- **Alternatives considered**: rendering any string as `src` regardless — rejected
  (injection/`javascript:` risk and broken images); adding a new sanitizer — rejected
  (YAGNI; the existing validator + `is url` test is sufficient and consistent).

## 5. Deliverable Scope

- **Decision**: Concrete outputs: (a) tests (written first) for bookmark icon rendering
  (URL → `<img>`, non-URL/short-word → label fallback, no icon → label, unsafe value never
  `src`, example config free of short words); (b) template + CSS changes; (c) example
  config + README cleanup. No model/schema change, no new endpoints, database, or server
  state, no new dependency.
- **Rationale**: Test-first (Principle IV) and accurate developer docs (Principle I),
  keeping the implementation small, consistent with the existing service-icon path, and
  free of speculative complexity.
- **Alternatives considered**: a separate config field or icon-management subsystem —
  rejected (YAGNI; the existing `Bookmark.icon` field is sufficient and already parsed).

## 6. Notes on Rendering Details

- The `Bookmark.icon` field and its parsing already exist (`app/model.py` line 15,
  `app/schema.py` `_parse_bookmark`); no data-layer change is needed, which is why the
  plan lists only template + CSS + example config + README + tests as modified files.
- The `is url` Jinja test is already registered in `app/__init__.py`
  (`app.jinja_env.tests["url"] = validate_url`), so the template can reuse it directly.
