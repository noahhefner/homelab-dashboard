# Implementation Plan: Navbar & Dark Mode

**Branch**: `005-navbar-darkmode` | **Date**: 2026-08-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/005-navbar-darkmode/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Refactor the dashboard top area into a persistent Bootstrap **navbar** (using the
`navbar` component and the `navbar-brand` class) that hosts a configurable title on the
left and a dark-mode theme toggle on the right. The configurable title replaces the
current fixed "HOME LAB" header and defaults to **"Homelab"** (one word) when not
provided. Dark mode is implemented with Bootstrap 5.3's `data-bs-theme` mechanism plus
CSS custom-property overrides for the dashboard-specific colors, with the user's choice
persisted in `localStorage` and a system-preference default. Finally, the dropdown
"carat" symbol is replaced with a Bootstrap icon (from the Bootstrap Icons icon set,
provisioned consistently with the existing pnpm-based asset flow from feature 003).

## Technical Context

**Language/Version**: Python 3.14 backend (unchanged, Flask 3.x app). Frontend is
server-rendered Jinja2 templates with Bootstrap 5.3.8.

**Primary Dependencies**: Flask 3.x (unchanged). Bootstrap 5.3.8 (unchanged, feature
003). **New**: Bootstrap Icons (the `bootstrap-icons` npm package) for the icon used in
place of the dropdown carat. Dark mode and the navbar use Bootstrap's built-in CSS/JS —
no new frameworks.

**Storage**: None (no database). Two client-side settings persist via `localStorage`
already (bookmark collapse state) — the theme preference follows the same pattern.

**Testing**: pytest (`uv run pytest`). Unit tests cover the configurable-title/default
behavior in schema/model; integration tests assert the navbar markup, title placement
(left) and toggle placement (right), and that the dropdown uses a Bootstrap icon instead
of the carat. Provisioning tests (feature 003 pattern) extend to cover the new Bootstrap
Icons assets.

**Target Platform**: Linux server (Docker host) serving the dashboard; modern browsers.

**Project Type**: web application (backend + frontend), a focused UI/UX enhancement plus
a small asset-provisioning addition.

**Performance Goals**: Preserve existing target — homepage loads and becomes interactive
in under 2 seconds on a typical home network and standard device. Swapping theme must be
instant (client-side only, no reload).

**Constraints**:
- The title MUST be configurable from the YAML config; when absent or empty, the default
  is "Homelab" (one word).
- The title MAY be any string; it MUST be HTML-escaped when rendered (Constitution
  Security) and must not break the navbar layout when long.
- The navbar MUST use the Bootstrap navbar component with the brand class.
- The theme toggle MUST live on the right side of the navbar.
- The user's theme choice MUST persist across reloads; a sensible default (system
  preference, falling back to light) applies when no choice is made.
- Dropdown indicators MUST use Bootstrap Icons rather than the carat character.
- Bootstrap Icons assets are provisioned (not committed), following the feature 003
  pnpm→static copy pattern; no new binaries committed.

**Scale/Scope**: Single-project enhancement. Touches config parsing (title default),
the homepage template (navbar + dropdown icon), app JS (theme toggle), app CSS (dark
theme + navbar), asset provisioning, plus tests, example config, and docs. Small and
bounded.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gate 1 — Extensibility & Modularity**: The change stays within the existing config →
schema → template boundaries. The title default lives in the model/schema; navbar and
dark mode are template + CSS + small JS within the existing single view; icon assets
follow the established provisioning module. No new entangled modules. ✅

**Gate 2 — Testability (Test-First, NON-NEGOTIABLE)**: New tests (written first)
verify: the configurable-title default ("Homelab" when absent/empty, custom value when
set); the navbar renders with the brand class, title on the left and toggle on the
right; and dropdown carets are replaced by Bootstrap icons. These are deterministic
static-markup assertions plus schema/model unit tests — no network needed. Theme
persistence JS is covered by a lightweight client-side check or by markup/attribute
assertions. ✅

**Gate 3 — YAGNI & Simplicity**: No new framework; dark mode reuses Bootstrap 5.3's
built-in `data-bs-theme`; the icon change reuses the existing Bootstrap Icons set via
the same pnpm-provision flow already established for Bootstrap. No speculative
settings screens, no per-account theming, no build system changes. ✅

**Gate 4 — Security Requirements**: The configurable title is HTML-escaped when
rendered (Jinja autoescape) — no injection. The theme preference is a client-side
localStorage value; none of it is server state or secrets. No new network exposure.
✅

**Gate 5 — DX First / Readability**: Provisioning one extra icon asset stays one
command (`pnpm setup`). The optional toggle requires no server-side work. Code follows
existing template/CSS/JS conventions. ✅

No violations; no Complexity Tracking table required until post-design re-check (see
bottom).

## Project Structure

### Documentation (this feature)

```text
specs/005-navbar-darkmode/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (title default + theme/icon contract)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# MODIFIED: title/theme/icon behavior + docs
app/
├── model.py                      # MODIFIED: DashboardConfig.title default -> "Homelab"
├── schema.py                     # MODIFIED: normalize empty/whitespace title to default
├── templates/index.html          # MODIFIED: navbar (navbar-brand) + theme toggle + icon dropdown
├── static/app.css                # MODIFIED: navbar styles, dark-theme custom props, icon styling
├── static/app.js                 # MODIFIED: theme toggle + persistence (mirrors collapse pattern)
└── static/bootstrap-icons/       # NEW: provisioned Bootstrap Icons assets (gitignored)
    ├── css/bootstrap-icons.min.css
    └── fonts/bootstrap-icons.woff2 (.woff)

scripts/provision-bootstrap.sh    # MODIFIED: also provision Bootstrap Icons css + fonts

# MODIFIED: dependency manifest + config/docs/tests
package.json                      # MODIFIED: add bootstrap-icons dependency
pnpm-lock.yaml                    # MODIFIED (generated by pnpm)
config/example.yaml               # MODIFIED (as needed): document/default title behavior
.gitignore                        # MODIFIED: ignore app/static/bootstrap-icons/
README.md                         # MODIFIED: document navbar, dark mode, configurable title, icons

tests/
├── unit/test_schema.py           # MODIFIED: default-title assertions ("Homelab")
├── unit/test_model.py            # NEW (or MODIFIED): title default
├── integration/test_navbar.py    # NEW: navbar/brand/title-left/toggle-right markup
├── integration/test_dark_mode.py # NEW: data-bs-theme attribute + default
├── integration/test_dropdown_icons.py   # NEW: icon replaces carat (e.g., bi-chevron)
└── integration/test_asset_provisioning.py  # MODIFIED: also assert bootstrap-icons assets

contracts/                        # NEW: title + theme + icon contract (in specs/005/contracts/)
```

**Structure Decision**: Keep the single-project layout. The change is a thin, deliberate
UI/UX layer over the existing Flask/Bootstrap app: it re-uses the existing config-title
key, swaps the header for a Bootstrap navbar, adds a client-side theme toggle on the
right (Bootstrap `data-bs-theme`), and re-provisions the bootstrap-icons font the same
way feature 003 provisions Bootstrap. No structural reorganization.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No Constitution Check violations; this table is intentionally empty. (Re-checked after
Phase 1 — no violations.)
