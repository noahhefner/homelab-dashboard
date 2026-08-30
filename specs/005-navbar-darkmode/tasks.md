# Tasks: Navbar & Dark Mode

**Input**: Design documents from `/specs/005-navbar-darkmode/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/navbar-theme-icons.md, quickstart.md

**Tests**: Test tasks are included because the project Constitution (Testing, Principle IV) makes test-first non-negotiable: tests MUST be written before the code they validate and pass in a clean run. Tests are deterministic static-markup and schema/model unit assertions (no external network needed).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project web app**: `app/`, `tests/` at repository root (per plan.md Structure Decision)
- Vendor static assets under `app/static/` (Bootstrap + Bootstrap Icons), gitignored; provisioned via `pnpm provision`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Provision the Bootstrap Icons vendor assets required by the dropdown-icon change (US4) so the icon CSS is servable and loaded. Mirrors the feature 003 pnpm→static provisioning flow.

- [X] T001 Add pinned `bootstrap-icons` dependency to `package.json` and regenerate `pnpm-lock.yaml` (via `pnpm add bootstrap-icons`)
- [X] T002 [P] Extend `scripts/provision-bootstrap.sh` to copy the Bootstrap Icons CSS and font files from `node_modules/bootstrap-icons/font/` into `app/static/bootstrap-icons/css/` and `app/static/bootstrap-icons/fonts/`, using the existing atomic temp-dir copy pattern
- [X] T003 [P] Add `app/static/bootstrap-icons/` to `.gitignore` (alongside the existing `app/static/bootstrap/` entry)
- [X] T004 Load the provisioned Bootstrap Icons CSS link in `app/templates/index.html` `<head>` alongside the existing Bootstrap CSS

**Checkpoint**: Icons assets provision (`pnpm provision`) and are servable from `app/static/bootstrap-icons/`; manifest + lockfile track the pinned dependency.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The configurable-title default (US1) resolves in `app/model.py`/`app/schema.py` and is rendered by the view. No other user story depends on this logic, so this phase is intentionally minimal — US1 is the first story and is implemented here rather than held in a separate blocking stage.

No additional blocking infrastructure is required. Work can proceed directly into the user-story phases below (priority order).

---

## Phase 3: User Story 1 - Configurable Dashboard Title (Priority: P1) 🎯 MVP

**Goal**: Replace the fixed "HOME LAB" heading with text driven by the config `title`, defaulting to "Homelab" (one word) when absent/empty.

**Independent Test**: With a custom `title` set, the rendered homepage shows it; with `title` omitted, empty, or whitespace-only, it shows "Homelab" — verifiable via `parse_dashboard` (unit) and the rendered page (checkpoint of US2).

### Tests for User Story 1 ⚠️ (write first, ensure they FAIL)

- [X] T005 [P] [US1] Unit test: empty/absent/whitespace title yields default "Homelab" in `tests/unit/test_schema.py`
- [X] T006 [P] [US1] Unit test: custom title is preserved (non-empty string) in `tests/unit/test_schema.py`

### Implementation for User Story 1

- [X] T007 [US1] Update `DashboardConfig.title` default from `"Home Lab"` to `"Homelab"` in `app/model.py`
- [X] T008 [US1] Normalize title in `parse_dashboard` in `app/schema.py` so missing/`null`/empty/whitespace-only values resolve to the default `"Homelab"`, and strip surrounding whitespace from non-empty values
- [X] T009 [US1] Render the (HTML-escaped) `title` in the page so it appears where the old "HOME LAB" heading was; repurpose the existing `title` template call (Jinja autoescape keeps it safe)

**Checkpoint**: US1 is complete — `parse_dashboard` returns "Homelab" for no/empty title and the custom value otherwise. The title now displays (initially still in the existing header container; US2 restyles it into the navbar).

---

## Phase 4: User Story 2 - Persistent Navbar with Title (Priority: P1) 🎯 MVP

**Goal**: Replace the static header with a Bootstrap `navbar` component using the `navbar-brand` class; the configurable title appears on the left.

**Independent Test**: The rendered homepage contains a Bootstrap `navbar` whose `navbar-brand` contains the dashboard title, located on the left side.

### Tests for User Story 2 ⚠️ (write first, ensure they FAIL)

- [X] T010 [P] [US2] Integration test: page renders a Bootstrap `navbar` with the `navbar-brand` class and the title text in `tests/integration/test_navbar.py`
- [X] T011 [P] [US2] Integration test: the brand/title is rendered on the left of the navbar and there is a right-side area reserved for the theme toggle in `tests/integration/test_navbar.py`

### Implementation for User Story 2

- [X] T012 [US2] Replace the `<header>` block in `app/templates/index.html` with a full-width Bootstrap `navbar` using the `navbar` and `navbar-brand` classes; place the configurable title in the brand on the left
- [X] T013 [US2] Add the right-side toggle container area (e.g., `.ms-auto`-pushed control region) in the navbar in `app/templates/index.html` for the theme toggle to occupy in US3
- [X] T014 [P] [US2] Add navbar styling (background, border, spacing, brand sizing) to `app/static/app.css`

**Checkpoint**: US2 is complete — a persistent Bootstrap navbar spans the top, brand title on the left, right-side region reserved. US1's title is now the navbar brand.

---

## Phase 5: User Story 3 - Toggleable Dark Mode (Priority: P1)

**Goal**: Add light/dark themes with a toggle in the navbar's right side; persist the choice and default to the system preference (else light).

**Independent Test**: The page renders the current theme via `data-bs-theme`; clicking the toggle in the navbar right side switches the theme, and the choice survives a reload.

### Tests for User Story 3 ⚠️ (write first, ensure they FAIL)

- [X] T015 [P] [US3] Integration test: rendered page includes a default `data-bs-theme` (dark only when the app/server resolves a dark default; otherwise light) in `tests/integration/test_dark_mode.py`
- [X] T016 [P] [US3] Integration test: the navbar contains a theme-toggle control on the right side in `tests/integration/test_dark_mode.py`

### Implementation for User Story 3

- [X] T017 [US3] Set the `data-bs-theme` attribute on the root element in `app/templates/index.html` (initial value chosen by the JS default, defaulting to system preference/light)
- [X] T018 [US3] Implement the theme-toggle button (with sun/moon Bootstrap icon) in the right-side navbar region in `app/templates/index.html`
- [X] T019 [US3] Implement theme toggling + persistence in `app/static/app.js` (set/remove `data-bs-theme`, store `light`/`dark` in `localStorage` under a `homelab:theme` key, apply system `prefers-color-scheme` default when unset, guard storage unavailability as the existing collapse code does)
- [X] T020 [US3] Add dark-theme CSS custom-property overrides (tile/bookmark/`--text-muted`/monogram colors) scoped under `[data-bs-theme="dark"]` in `app/static/app.css`

**Checkpoint**: US3 is complete — the toggle in the navbar right switches themes, dark theme restyles the dashboard's custom tiles/bookmarks, and the choice persists.

---

## Phase 6: User Story 4 - Replace Dropdown Carats with Bootstrap Icons (Priority: P3)

**Goal**: Replace the literal caret character on bookmark-group toggles with a Bootstrap Icon that still conveys open/closed state.

**Independent Test**: The rendered bookmark-group toggle contains a Bootstrap icon (e.g., `bi-chevron-down`) and no literal carat character.

### Tests for User Story 4 ⚠️ (write first, ensure they FAIL)

- [X] T021 [P] [US4] Integration test: bookmark-group toggle uses a Bootstrap icon element and does NOT contain the literal carat (`▾`) in `tests/integration/test_dropdown_icons.py`

### Implementation for User Story 4

- [X] T022 [US4] Replace `<span class="group-caret">▾</span>` with a Bootstrap icon element (e.g., `<i class="bi bi-chevron-down group-caret">`) in `app/templates/index.html`, keeping the existing aria-hidden marker
- [X] T023 [US4] Confirm the icon's open/closed rotation styling in `app/static/app.css` (rotate -90deg when collapsed) targets the new icon element so the dropdown state is still visually conveyed

**Checkpoint**: US4 is complete — every dropdown indicator is a Bootstrap icon and all existing collapse behavior is preserved.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and asset-provisioning coverage that span multiple user stories.

- [X] T024 [P] Update `tests/integration/test_asset_provisioning.py` to also assert the Bootstrap Icons CSS + font assets exist and are gitignored, and that `package.json`/`pnpm-lock.yaml` still track the pinned `bootstrap-icons` dependency
- [X] T025 [P] Update `app/config.py` reference/`config/example.yaml` and `README.md` to document the configurable title (default "Homelab"), the navbar, dark mode toggle, and the Bootstrap-icons dropdown indicators
- [X] T026 [P] Validate the end-to-end behavior against `specs/005-navbar-darkmode/quickstart.md` (V1–V6) and confirm `uv run pytest` and `pnpm provision` pass cleanly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.
- **User Story 1 (Phase 3)**: Depends on nothing blocking (schema/model/template only).
- **User Story 2 (Phase 4)**: Depends on US1 (the title value shown in the brand) and on Setup's icon CSS load only for the icon toggle (US3/US4).
- **User Story 3 (Phase 5)**: Depends on US2 (navbar + right-side toggle region).
- **User Story 4 (Phase 6)**: Depends on Setup (Phase 1) for the provisioned Bootstrap Icons assets; independent of US1–US3.
- **Polish (Phase 7)**: Depends on the desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: No upstream story deps — first MVP slice.
- **US2 (P1)**: Depends on US1's title value; shares `app/templates/index.html` with US1.
- **US3 (P1)**: Depends on US2's navbar region; shares `app/templates/index.html` and `app/static/app.js`/`app.css`.
- **US4 (P3)**: Independent of US1–US3 (only needs Setup assets + the toggle's `group-caret` element); can be parallelized after Setup.

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Constitution test-first).
- Schema/model/unit changes before template changes within a story.

### Parallel Opportunities

- T001/T002/T003 (Setup) and T004 can partly run in parallel (T004 needs the provisioned assets to load correctly, so order T004 after a successful `pnpm provision`).
- US1 tests (T005/T006) and US2 tests (T010/T011) are [P] within their stories.
- Within-story implementation files are distinct where marked [P].
- US4 is fully parallelizable after Setup completes.

---

## Parallel Example: User Story 1 & User Story 4

```bash
# Launch US1 unit tests together:
Task: "Unit test: empty/absent/whitespace title yields default 'Homelab' in tests/unit/test_schema.py"
Task: "Unit test: custom title is preserved in tests/unit/test_schema.py"

# Launch US4 icon test (does not depend on US1):
Task: "Integration test: bookmark-group toggle uses a Bootstrap icon in tests/integration/test_dropdown_icons.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Complete Phase 1: Setup (provision Bootstrap Icons).
2. Complete Phase 3: User Story 1 (title default) → validate via `uv run pytest`.
3. Complete Phase 4: User Story 2 (navbar) → validate the navbar + brand title render.
4. **STOP and VALIDATE**: Confirm `uv run pytest` is green and the homepage shows the brand title in the navbar.
5. Deploy/demo the MVP (customizable title in a Bootstrap navbar).

### Incremental Delivery

1. Setup → US1 (title default) → US2 (navbar) → validate (MVP).
2. Add US3 (dark mode toggle) → validate independently.
3. Add US4 (icons) → validate independently.
4. Polish + docs → full green run.

### Parallel Team Strategy

1. Team completes Setup together.
2. Developer A: US1 → US2 (navbar, sequential due to shared template).
3. Developer B: US3 (after US2's navbar region lands) or US4 (independent after Setup).
4. Stories integrate independently; each adds value without breaking prior stories.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps each task to its user story for traceability.
- US1 and US2 both edit `app/templates/index.html`, so they must run sequentially (not parallel) despite being separate stories.
- The Bootstrap Icons font/CSS are gitignored provisioned assets; never commit them.
- Verify tests fail before implementing, then pass in a clean run (Constitution Principle IV).
