# Research: Navbar & Dark Mode

**Phase 0 output for `/specs/005-navbar-darkmode/plan.md`**

Purpose: resolve the technical decisions needed to add the Bootstrap navbar with a
configurable title, a toggleable dark mode, and Bootstrap-icon dropdown indicators,
working within the existing Flask/Bootstrap dashboard and the Constitution's principles.

## 1. Configurable Title and Default Semantics

- **Decision**: Keep the existing top-level `title` YAML key as the source of the
  customizable text. Change the default to **"Homelab"** (one word) per the explicit
  requirement. Treat a missing key, `null`, an empty string, or a whitespace-only string
  as "no title provided" and fall back to "Homelab". The rendered title is
  HTML-escaped (Jinja autoescape already active).
- **Rationale**: The config already has a `title` key (`config/example.yaml`), and
  `app/schema.py` currently defaults it to `"Home Lab"`. Reusing the key avoids adding a
  new config surface and keeps the change minimal (Principle V). The schema/model default
  is the single source of truth so empty/missing values normalize consistently before
  rendering. HTML escaping supplies the Security gate.
- **Alternatives considered**:
  - Introduce a new key (e.g., `dashboard_title`): rejected — redundant with the existing
    `title` field; confusing to maintain two names.
  - Keep default "Home Lab" and only change rendering casing: rejected — the requirement
    explicitly says default is "Homelab", one word.
  - Normalize in the template only: rejected — default belongs with the model/schema, and
    tests should exercise `parse_dashboard` directly (test-first).

## 2. Navbar: Structure and Placement

- **Decision**: Replace the current `<header>` block in `app/templates/index.html` with a
  Bootstrap `navbar` using the `navbar` component class and the `navbar-brand` class for
  the title, fixed at the top of the page (spanning full width). The `navbar-brand`
  element sits on the **left**; a theme-toggle control sits on the **right** (e.g., a
  button/icon pair inside a `.ms-auto`-spaced element or a navbar item pushed right).
- **Rationale**: The user explicitly asked for the "Bootstrap navbar component with the
  brand class". Bootstrap 5.3's navbar is the idiomatic component, fully supported by the
  provisioned bootstrap.bundle.min.js, and gives free responsiveness and spacing. Using
  `navbar-brand` is the brand/title element by definition.
- **Alternatives considered**: a custom header with flexbox — rejected (user asked for the
  Bootstrap navbar; reusing the component is simpler and consistent); putting the title
  outside the navbar — rejected (user asked for the title in the navbar on the left).

## 3. Dark Mode: Mechanism, Toggle, and Persistence

- **Decision**: Use Bootstrap 5.3's `data-bs-theme="dark"` attribute on the root
  (`<html>` or `<body>`) to switch the whole component palette. Provide a small set of
  CSS custom-property overrides (e.g., `--tile-bg`, `--tile-border`, `--text-muted`,
  `--monogram-bg`) under a `[data-bs-theme="dark"]` scope in `app.css` so the dashboard's
  custom tiles/bookmarks also switch. The toggle (a button containing a sun/moon Bootstrap
  icon) calls small JS that sets/removes the attribute and persists the choice in
  `localStorage` (key like `homelab:theme`). On load, apply the persisted value; if none,
  honor the user's `prefers-color-scheme` (system) preference, defaulting to light when no
  system preference is detected.
- **Rationale**: Bootstrap 5.3 has first-class dark mode via `data-bs-theme`; using it is
  the least-code, most-consistent approach (Principle V). Persisting via `localStorage`
  matches the existing bookmark-collapse pattern in `app.js` (Principle I, consistency).
  A system-preference default is the "sensible default" the spec's edge case calls for.
- **Alternatives considered**: maintain two separate stylesheets — rejected (fragile,
  duplicates styling); `prefers-color-scheme`-only (no manual toggle) — rejected (user
  explicitly wants a toggleable dark mode in the navbar); a theme cookie/server-state —
  rejected (no accounts/server persistence; client-side is simpler and sufficient).

## 4. Replacing the Dropdown Carat with Bootstrap Icons

- **Decision**: Replace the literal `▾` carat in the bookmark group toggle
  (`<span class="group-caret">▾</span>` in `app/templates/index.html`) with a Bootstrap
  icon element, e.g. `<i class="bi bi-chevron-down"></i>`, and keep the rotate-based
  open/closed affordance (rotate -90deg when collapsed) applied to the icon. Bootstrap
  Icons are NOT part of the `bootstrap` package, so add the `bootstrap-icons` npm package
  as a dependency and extend `scripts/provision-bootstrap.sh` to copy its CSS + font files
  into `app/static/bootstrap-icons/` (same pattern as feature 003). Load the icon CSS in
  `index.html`.
- **Rationale**: Bootstrap Icons is the standard icon set for Bootstrap components and
  satisfies "bootstrap icons" literally. Extending the existing pnpm→static provision flow
  is the established, minimal mechanism for shipping vendor assets without committing
  binaries (feature 003 / YAGNI). Using a chevron preserves the existing open↔closed
  rotation affordance so the icon also conveys state.
- **Alternatives considered**: hand-inline an SVG — rejected (user asked for "bootstrap
  icons"; the Bootstrap Icon set is the intended dependency and is version-pinned like
  Bootstrap); bundle a subset of icons — rejected (adds a custom build step; the full font
  is a small, gitignored provisioned artifact); use Bootstrap's bundled "bi" — not
  available, Bootstrap does not ship the icon font.

## 5. Bootstrap Icons Provisioning (feature 003 style)

- **Decision**: Add `bootstrap-icons` (pinned) to `package.json` and `pnpm-lock.yaml`.
  Extend `scripts/provision-bootstrap.sh` to copy from
  `node_modules/bootstrap-icons/font/` the `bootstrap-icons.min.css`, `bootstrap-icons.woff2`
  (and `.woff`) into `app/static/bootstrap-icons/css/` and `app/static/bootstrap-icons/fonts/`
  atomically via the existing temp-dir pattern. Add `app/static/bootstrap-icons/` to
  `.gitignore`. The icon CSS references the fonts via relative paths, matching the
  destination layout.
- **Rationale**: Mirrors the proven provisioning approach for Bootstrap itself (feature
  003): pinned dependency in the manifest, `pnpm provision` materializes gitignored static
  assets, tests assert the assets exist and are gitignored, and the manifest/lockfile stay
  tracked. Reproducible and one command (`pnpm setup`).
- **Alternatives considered**: committing the icon font/css — rejected (violates the
  lean-repository, gitignored-assets approach of feature 003); loading bootstrap-icons from
  a CDN — rejected (the project deliberately serves vendor assets locally, offline-capable;
  a CDN dependency would contradict feature 003 and make the dashboard depend on external
  reachability).

## 6. Deliverable Scope

- **Decision**: Concrete outputs: (a) tests (written first) for the title default, navbar
  structure/brand, toggle placement, dark-theme attribute, and icon-replaces-carat; (b)
  app changes (model/schema default, template navbar, CSS dark theme + navbar + icon, JS
  toggle); (c) asset provisioning for bootstrap-icons + gitignore + manifest; (d) example
  config + README/quickstart docs. No new endpoints, database, or server-side state.
- **Rationale**: Test-first (Principle IV) and accurate developer docs (Principle I) while
  keeping the implementation small and free of speculative complexity.
- **Alternatives considered**: a theme-management subsystem or per-user settings page —
  rejected (YAGNI; the toggle + local persistence fully satisfies the requirement).
