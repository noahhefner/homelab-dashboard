# Research: Disable Search and Bookmarks

**Feature**: 012-disable-search-bookmarks
**Date**: 2026-09-06

## R1: Config key naming and semantics

**Decision**: Use two top-level boolean keys **`show_search`** and **`show_bookmarks`**, both defaulting to `true` (feature shown).

**Rationale**: The feature description frames the toggles as "disable" options, but positive "show" flags with a default of enabled match the existing config's semantics best (e.g., `collapsed: false` is "expanded by default") and read naturally in YAML: `show_search: true`. Naming them as "show" avoids double-negatives like `hide_bookmarks: false`. Defaulting to enabled means existing configs without the keys render identically to today, satisfying the spec's "enabled by default" requirement and the backward-compatibility success criteria (SC-004, SC-006).

**Alternatives considered**:
- `enable_search` / `enable_bookmarks`: equivalent, but "show" maps more directly to the visible UI that is being toggled.
- `hide_search` / `hide_bookmarks` (default `false`): rejected — negative semantics are less readable in a config and invert the spec's "default enabled" framing.

## R2: Where the flags live — parsed model vs. raw YAML read

**Decision**: Add `show_search` and `show_bookmarks` as fields on `DashboardConfig`, parsed in `parse_dashboard()` via a small `_parse_bool_flag(value, default)` helper, and consumed by views/templates from the parsed config.

**Rationale**: This follows the exact pattern established for feature-011 (`search_engine`/`search_engine_icon`): config key → dataclass field → `parse_dashboard` → `render_template`. These flags are ordinary dashboard data, not security/authorization switches, so they do not need the raw-YAML special-casing that `editor_enabled()` uses (which exists only because `editor` is a default-deny flag intentionally kept out of the model). Keeping them in the model keeps parsing testable at the unit level and consistent with how every other visible feature is configured.

**Alternatives considered**:
- Reading raw YAML in a view helper like `editor_enabled()`: rejected — duplicates config access logic and bypasses live-reload caching, and these are not default-deny security flags.
- Storing in `app.config`: rejected — would bypass the `ConfigLoader` live-reload mechanism.

## R3: Invalid value handling

**Decision**: A non-boolean value for either flag falls back to the default (`true`, shown) and never raises or blocks config load.

**Rationale**: Spec FR-009 requires that invalid values fall back to "shown" and never crash or fail to load. This mirrors the existing lenient default-on behavior of `_parse_search_engine` (invalid → default) and keeps a typo from taking down the dashboard (Constitution: "errors MUST surface the cause... rather than a bare failure" and DX Principle I). Only genuine `bool` values (`true`/`false`) set the flag; strings like `"false"` or integers do not.

**Alternatives considered**:
- Raising `ConfigValidationError` for invalid values (like `collapsed` does): rejected — that would fail config loading, the opposite of the spec's explicit requirement (FR-009, SC-006).
- Coercing strings (`str(value).lower() in {"true", ...}`): rejected per Principle V/II — implicit coercion adds hidden behavior; a strict boolean check with a safe default is simpler and testable.

## R4: How hiding is implemented in templates

**Decision**: Wrap the search `<form>` in `{% if show_search %}` in both `index.html` and `config.html`, and wrap the bookmarks `<aside>` in `{% if show_bookmarks %}` in `index.html`. When bookmarks are hidden, drop the `col-lg-9` constraint on the tiles `<section>` so it expands to full width.

**Rationale**: Conditional template rendering is the simplest hiding mechanism — nothing is emitted to the browser, so the hidden feature occupies zero space (spec FR-002, FR-005) with zero CSS. The tiles section currently uses `col-12 col-lg-9` because the bookmarks `<aside>` occupies the `col-lg-3`; removing the constraint lets the tiles use the freed space (spec FR-006). The navbar's other flex elements already carry `me-auto`/`ms-auto`, so once the middle search form is removed the brand and right-side controls rebalance automatically with no CSS changes.

**Alternatives considered**:
- CSS `display:none` via a Bootstrap utility (`d-none`) driven by a template class: rejected — the element would still be sent over the wire and clutter the DOM; a plain conditional is more direct (Principle V).
- Custom CSS / a `body` class: rejected per Principle VI — Bootstrap utilities and the existing grid already express everything needed.

## R5: Example config update

**Decision**: Add `show_search: true` and `show_bookmarks: true` to `config/example.yaml` near the existing top-level `title`/`editor` keys, each with a short comment explaining the default and how to hide the feature.

**Rationale**: The user explicitly requested that the example config document the new values. Comments follow the existing example-file style (every top-level and per-group key has an explanatory comment). Placing the flags at the top, like `editor`, groups the simple dashboard-level switches together.

**Alternatives considered**:
- Only documenting in the README/spec: rejected — the user asked for the example config to carry the values, and the file is the canonical onboarding artifact.
- Touching `local.yaml` or the `.backup.yaml` files: rejected — those are user-owned/backup files, not documentation.

## R6: Which templates/pages are affected

**Decision**: The search bar gate applies to both `index.html` and `config.html`; the bookmarks gate applies only to `index.html` (the config editor page never renders bookmarks).

**Rationale**: Both page templates have a navbar search form (duplicated markup, per the existing convention noted in feature-011), so the search toggle must gate both (spec FR-002, US1 acceptance #3). Bookmarks render only on the homepage `<aside>`, so only `index.html` needs the bookmarks gate (spec FR-005). No other templates render either feature.

**Alternatives considered**:
- Extracting the search form into a partial (`_search.html`) to avoid double-maintenance: rejected for this feature per Principle V — the duplication pre-dates this change and extracting it is out of scope; both edits are small and gated identically.

## R7: Security implications

**Decision**: No new security surface. Both flags are strict booleans; the full search-bar/icon URL handling (validator, `rel="noopener"`, `onerror` fallback) is unchanged and only rendered when the search bar is shown. Hiding or showing features does not expose data or require access control in a single-owner dashboard.

**Alternatives considered**: none — security check is a verification, not a design choice.