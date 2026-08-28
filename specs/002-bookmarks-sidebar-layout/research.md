# Research: Bookmarks Sidebar Layout (UIKit → Bootstrap)

**Phase 0 output for `/specs/002-bookmarks-sidebar-layout/plan.md`**

Purpose: resolve the technical unknowns raised during planning and record the
decisions, rationale, and alternatives considered. Every decision below is
technology-level and feeds the contracts/design in Phase 1.

## 1. Bootstrap Version

- **Decision**: Bootstrap **5** (CSS + the `bootstrap.bundle.min.js` build, which
  includes Popper and the collapse component).
- **Rationale**: Bootstrap 5 is the current stable major release, is maintained by
  the Bootstrap team, uses modern CSS (CSS custom properties, flexbox/grid), and
  its grid + collapse components cover the two things this feature needs
  (responsive columns and collapsible bookmark groups) without extra libraries.
  Bootstrap 5 does not require jQuery, so no extra dependency is introduced.
- **Alternatives considered**:
  - **Bootstrap 4**: older, requires jQuery; rejected (more baggage, older maintenance).
  - **Custom CSS only**: rejected because the user explicitly asked to adopt Bootstrap.
  - **Tailwind/PureCSS**: not requested and would add a build step; rejected for
    simplicity (Constitution Principle V).

## 2. Vendoring Bootstrap for Offline Use

- **Decision**: Vendor the **prebuilt distribution** assets directly into the repo
  under `app/static/bootstrap/`:
  - `css/bootstrap.min.css`
  - `js/bootstrap.bundle.min.js`
- **Rationale**: Vendoring the official prebuilt dist means no CDN, no build tooling,
  and no node_modules — everything still works offline, consistent with the
  existing approach used for UIKit (feature 001 vendored UIkit under
  `app/static/uikit/`). These are plain static files served by Flask, matching the
  project's no-build, single-container design (Constitution Principle V).
- **Implementation note**: Download the two files from the official Bootstrap 5.x
  release once and commit them. The template references them via
  `{{ url_for('static', filename='bootstrap/css/bootstrap.min.css') }}` and the
  matching `.js` path so Flask serves them locally. No network access is required
  at runtime.
- **Alternatives considered**:
  - **CDN link**: rejected — the user explicitly requires offline capability.
  - **Bootstrap via a package manager / build step (sass/rollup)**: rejected —
    introduces a compile step and dependency graph that is unnecessary for a single
    static stylesheet, violating YAGNI (Principle V).

## 3. Responsive Layout: Bookmarks on the Right (Desktop) / Below (Mobile)

- **Decision**: Use Bootstrap's **grid** to make the page a two-column layout at the
  `lg` breakpoint (≥992px) and a stacked single column below it:
  - A `.row` wraps two `.col` children:
    - **Services/apps column**: `col-12 col-lg-9` (full width on mobile; ~75% on desktop).
    - **Bookmarks sidebar column**: `col-12 col-lg-3` (full width below the apps on
      mobile; ~25% on the right on desktop).
- **Rationale**: Bootstrap's grid handles the responsive reflow declaratively with a
  single, fixed breakpoint (`lg`). This directly satisfies spec requirements
  FR-001..FR-005 (right side on desktop, below on mobile, single consistent
  breakpoint, automatic reflow). Using `col-12 col-lg-*` guarantees ordering:
  because the services column appears first in the DOM and wraps onto its own full row
  on mobile, bookmarks naturally fall below the apps with no CSS hacks and no
  horizontal scroll on small screens.
- **Ordering / DOM order**: On desktop both columns sit side by side (services left,
  bookmarks right) via `lg` columns; on mobile each `col-12` stacks vertically, with
  services first and bookmarks second. This matches spec FR-002/FR-003 exactly.
- **Alternatives considered**:
  - **CSS Grid custom layout (e.g., `grid-template-columns`)**: viable but would
    reimplement what Bootstrap grid already provides; rejected to keep the CSS small
    and consistent with Bootstrap's own conventions.
  - **Flexbox with `order` utilities**: possible but the Bootstrap grid col classes are
    more idiomatic and readable for this codebase.

## 4. Collapsible Bookmark Groups

- **Decision**: Use **Bootstrap's Collapse** component for bookmark group
  expand/collapse, replacing the current UIKit-native toggle behavior.
- **Rationale**: Bootstrap ships a stateful, accessible collapse component
  (`data-bs-toggle="collapse"` + `data-bs-target`/`href`, or the JS API). It preserves
  the existing UX (group headers that show/hide their bookmarks) with standard,
  fallback-safe markup, and removes the need for hand-rolled show/hide logic.
- **Group-state persistence**: The existing requirement to persist collapsed/expanded
  state across visits (feature 001 FR-006) is preserved. Since Bootstrap collapse is
  stateless by default, `app.js` will re-apply the persisted open/closed state from
  localStorage on load (mirroring the current `STORAGE_KEY` approach) and sync it on
  toggle events.
- **Alternatives considered**:
  - **Keep hand-rolled toggle in `app.js`**: possible, but adopting Bootstrap's
    component honors the user's UI-framework migration intent and reduces custom JS.
  - **`<details>`/`<summary>` native disclosure**: loses the ability to persist state
    as cleanly and is not part of Bootstrap; rejected for consistency.

## 5. Backend / Data-Contract Impact

- **Decision**: **No backend changes.** `views.py` already passes `services` and
  `bookmark_groups` to `index.html`; the template consumes the same context. The YAML
  schema, model, and validation rules are unchanged.
- **Rationale**: The feature is presentation-only (spec Assumptions and FR scope). Any
  template change is limited to markup/CSS/JS.
- **Alternative considered**: none — changing the backend would be out of scope and is
  explicitly avoided per the spec's scope boundary.

## 6. Existing Tests That Must Change

- **Decision**: Update integration/unit tests that assert UIKit-specific markup:
  - `tests/integration/test_mobile_layout.py`: replace `uk-child-width-*` class
    assertions with `col-12 col-lg-*` grid assertions; keep the viewport-meta and
    plain-anchor/tap-friendly assertions (they still apply).
  - `tests/integration/test_bookmark_groups.py`, `test_homepage_services.py`,
    `test_invalid_config.py`, `test_config_reload.py`: verify they still pass as-is
    (they assert rendered text/group names, which are unaffected); add/new assertions
    where a rendered-class check existed.
  - Unit view tests: update any class-string assertions.
- **Rationale**: Test-first requires the tests be updated in lockstep with the UI so
  a clean `uv run pytest` run passes (Constitution Principle IV).
