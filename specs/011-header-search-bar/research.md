# Research: Header Search Bar

**Feature**: 011-header-search-bar
**Date**: 2026-09-03

## R1: How to pass config values to Jinja2 templates

**Decision**: Add `search_engine` as a field on `DashboardConfig` and pass it to templates via `render_template()` in `views.py`.

**Rationale**: The existing pattern already passes `config.title`, `config.tile_groups`, etc. to templates. Adding `search_engine` to the dataclass keeps the data flow consistent and avoids special-casing like `editor_enabled()` (which reads raw YAML because `parse_dashboard` intentionally ignores unknown keys).

**Alternatives considered**:
- Reading raw YAML in the view (like `editor_enabled()`): rejected because it duplicates config access logic and the search engine URL is a parsed, validated value, not a boolean flag.
- Storing it in `app.config`: rejected because it would bypass the live-reload mechanism.

## R2: Configurable search engine URL pattern

**Decision**: Use a `{query}` placeholder in the URL template string (e.g., `https://duckduckgo.com/?q={query}`). Validate that the placeholder is present.

**Rationale**: This is the most common pattern for configurable search engines. All major search engines (Google, DuckDuckGo, Bing, Brave Search) accept a query parameter in their URL. The `{query}` placeholder is simple, well-understood, and easy to validate.

**Alternatives considered**:
- Using a separate `search_engine_name` + built-in URL map: rejected per YAGNI (Principle V) — a URL template is more flexible and avoids maintaining a list of engines.
- Using `{{query}}` (Jinja2 syntax): rejected because it would conflict with template rendering; `{query}` is template-agnostic.

## R3: Mobile hiding approach

**Decision**: Use Bootstrap's responsive display utilities: `d-none d-md-flex` (or `d-none d-md-block`) on the search bar container. This hides the element below the `md` breakpoint (768px) and shows it at `md` and above.

**Rationale**: Per Principle VI (Framework-First Frontend), Bootstrap's built-in responsive utilities are the preferred approach. `d-none d-md-flex` is the standard Bootstrap pattern for hiding on mobile and showing on medium+ viewports. No custom CSS is needed.

**Alternatives considered**:
- Custom `@media` query in `app.css`: rejected per Principle VI — Bootstrap already provides this functionality.
- JavaScript-based viewport detection: rejected per Principle V — unnecessary complexity for a CSS-only problem.

## R4: Search form HTML structure

**Decision**: Use a plain `<form>` element with `method="GET"`, `target="_blank"`, `rel="noopener"`, and an `<input type="search">`. The form's `action` attribute is set to the search engine URL with `{query}` replaced. A submit button with a search icon (Bootstrap Icons) provides a visible click target.

**Rationale**: A plain HTML form requires no JavaScript for the core search-and-open behavior. `target="_blank"` opens results in a new tab. `rel="noopener"` prevents the new tab from accessing `window.opener`. `type="search"` provides built-in browser behaviors (clear button, Enter-to-submit).

**Alternatives considered**:
- JavaScript-based `window.open()`: rejected per Principle V — a plain form achieves the same result with zero JS.
- Using Bootstrap's input group component: considered but a standalone form element is simpler and avoids visual complexity in the navbar.

## R5: Default search engine

**Decision**: Default to Google (`https://www.google.com/search?q={query}`) when `search_engine` is absent or invalid.

**Rationale**: Google is the most widely known search engine and a reasonable default for a personal tool. The spec explicitly requests this default.

**Alternatives considered**:
- DuckDuckGo: a reasonable privacy-focused alternative, but Google is more universally recognized as a default.
- No default (hide search bar when unconfigured): rejected because the spec requires a fallback.

## R6: Search engine icon format and storage

**Decision**: Add a `search_engine_icon` field on `DashboardConfig` storing an external image URL (same format as existing tile/bookmark icons). Pass it to templates via `render_template()`.

**Rationale**: This is consistent with how tiles and bookmarks already handle icons in this project (external URL strings in YAML, validated with `validate_url`). The existing `validate_url` infrastructure in `app/security.py` can be reused directly, and the same `<img>` + `onerror` fallback pattern already used for tile/bookmark icons can be applied.

**Alternatives considered**:
- Bootstrap Icons class name (e.g., `bi bi-google`): rejected per the user's clarification — they explicitly chose external image URL format.
- Both (URL + class): rejected per Principle V (YAGNI) — a single external URL format is sufficient.

## R7: Search engine icon fallback on broken image

**Decision**: Use the existing `onerror` pattern already present in the project (used for tile and bookmark icons) to hide a broken `<img>` and reveal a default `bi-search` Bootstrap icon fallback.

**Rationale**: The project already uses this exact pattern for tile icons in `index.html` (`onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"`). Reusing it keeps the codebase consistent (Principle II) and requires no new JavaScript (Principle V).

**Alternatives considered**:
- Server-side image validation/proxy: rejected per Principle V — unnecessary complexity; the frontend `onerror` pattern suffices.
- Custom JS to swap icons: rejected because the project already has a well-established HTML `onerror` pattern.

## R8: Search engine icon positioning

**Decision**: Place the icon before (left of) the search input field, inside the search form's flex container.

**Rationale**: This is the standard pattern for search interfaces (Google, GitHub, etc.) and reads naturally as "search for [query]". It follows the user's explicit clarification.

**Alternatives considered**:
- After the input / before submit button: rejected per user clarification.
- As the submit button itself: rejected per user clarification.
