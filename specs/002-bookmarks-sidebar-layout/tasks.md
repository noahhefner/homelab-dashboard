# Tasks: Bookmarks Sidebar Layout

**Input**: Design documents from `/specs/002-bookmarks-sidebar-layout/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The constitution mandates test-first (Principle IV, non-negotiable) and this project has an existing test suite. Test tasks are therefore included: update existing tests that assert UIKit markup and add assertions for the new Bootstrap grid/layout/offline contract.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `tests/` at repository root (see `plan.md` Project Structure)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Vendor the Bootstrap assets that every frontend change depends on, replacing the current UIKit assets, so the UI works offline (user requirement).

- [X] T001 [P] Download and vendor Bootstrap 5 CSS into `app/static/bootstrap/css/bootstrap.min.css` (replaces `app/static/uikit/css/uikit.min.css`)
- [X] T002 [P] Download and vendor Bootstrap 5 bundle JS into `app/static/bootstrap/js/bootstrap.bundle.min.js` (replaces `app/static/uikit/js/*`)
- [X] T003 Delete the now-unused vendored UIKit directory `app/static/uikit/`

**Checkpoint**: Bootstrap assets are vendored locally under `app/static/bootstrap/` and UIKit is removed. No network connectivity is required at runtime.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update shared templates and app CSS/JS to Bootstrap before any user-story-specific layout work, so all stories build on a consistent frontend base.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Update `app/templates/index.html` to load the vendored Bootstrap CSS and JS via `{{ url_for('static', filename='bootstrap/css/bootstrap.min.css') }}` and `{{ url_for('static', filename='bootstrap/js/bootstrap.bundle.min.js') }}`, removing all UIKit class/script references
- [X] T005 [P] Replace UIKit utility/component classes in `app/templates/error.html` with Bootstrap equivalents (or confirm inline CSS is sufficient per its current markup) so the error page remains consistent
- [X] T006 [P] Update `app/static/app.css` to remove UIKit-specific rules and re-style the service tiles, bookmark links, monograms, and group headers using Bootstrap-compatible base styles (keep the existing `:root` design tokens and mobile touch-target refinement)

**Checkpoint**: Foundation ready — the page loads Bootstrap from local vendored assets, UIKit references are gone, and base styling is applied. User story implementation can now begin.

---

## Phase 3: User Story 1 - Bookmarks on the right on desktop (Priority: P1) 🎯 MVP

**Goal**: On desktop (≥992px), render the homelab apps in the main left area and the bookmarks in a right-hand column, visible without scrolling.

**Independent Test**: Open the dashboard in a wide (≥992px) viewport and confirm the bookmarks render in a right-side column beside the apps (not below), and clicking a bookmark still opens its destination. Covered automatically by updated integration tests asserting the grid classes.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T007 [P] [US1] Update `tests/integration/test_mobile_layout.py` to assert the Bootstrap right-column layout contract: services container has `col-12 col-lg-9`, bookmarks container has `col-12 col-lg-3`, both wrapped in a `row` (replacing the `uk-child-width-*` assertions)
- [X] T008 [P] [US1] Add an integration test asserting the rendered homepage references **local** `/static/bootstrap/...` assets and contains no remote/CDN CSS/JS URL (offline requirement) in `tests/integration/test_mobile_layout.py`

### Implementation for User Story 1

- [X] T009 [US1] Rework the layout in `app/templates/index.html`: wrap the services section and the bookmarks section in a single Bootstrap `.row`, giving the services section classes `col-12 col-lg-9` and the bookmarks section `col-12 col-lg-3` (order: services first, bookmarks second)
- [X] T010 [US1] Ensure the desktop side column handles many bookmarks gracefully: add scroll/overflow styling in `app/static/app.css` so a tall bookmarks column does not break the page layout (spec FR-009 / US3-2 intent)

**Checkpoint**: User Story 1 is fully functional on desktop and testable independently (apps left, bookmarks right, offline assets).

---

## Phase 4: User Story 2 - Bookmarks below the apps on mobile (Priority: P1)

**Goal**: On mobile/narrow viewports (<992px), render the bookmarks **below** the homelab apps with no horizontal scrolling, all content reachable via tap.

**Independent Test**: Open the dashboard at phone width and confirm bookmarks appear below the apps, with no horizontal scroll, and tapping a bookmark opens the destination without requiring hover.

### Tests for User Story 2 ⚠️

- [X] T011 [P] [US2] Update `tests/integration/test_mobile_layout.py` to assert the mobile stack contract: the services container uses `col-12`, the bookmarks container uses `col-12`, and the viewport meta tag remains present (no horizontal scroll intent)
- [X] T012 [P] [US2] Keep/extend the tap-friendly assertions (plain `<a href>`, `target="_blank"`, `noopener`) in `tests/integration/test_mobile_layout.py` for the mobile paths

### Implementation for User Story 2

- [X] T013 [US2] Confirm the `col-12` foundation in `app/templates/index.html` stacks the services above the bookmarks on mobile (the `col-lg-*` classes from US1 only take effect at `lg`), so bookmarks naturally fall below the apps with no CSS workarounds
- [X] T014 [US2] Verify/adjust mobile touch-target sizing in `app/static/app.css` under the existing `@media (max-width: ...)` refinement so service tiles and bookmark links remain comfortable tap targets (spec FR-007)

**Checkpoint**: User Stories 1 AND 2 both work independently (desktop right column, mobile below-apps stack).

---

## Phase 5: User Story 3 - Responsive reflow between breakpoints (Priority: P2)

**Goal**: As the window resizes between desktop and phone widths, bookmarks smoothly reflow from the right column to below the apps and back, with no clipped/overlapping/off-screen content.

**Independent Test**: Resize the browser continuously across the `lg` breakpoint and confirm the bookmarks reflow from right to below (and back) with no layout breakage at any width.

### Tests for User Story 3 ⚠️

- [X] T015 [P] [US3] Add an integration test in `tests/integration/test_mobile_layout.py` asserting a single, consistent `lg` breakpoint (no ambiguous intermediate classes) and that no fixed-width container causes overflow (reuse/extend existing no-horizontal-scroll checks)
- [X] T016 [US3] Update `tests/unit/test_bookmark_group_state.py` so the group toggle still works after switching to Bootstrap Collapse: keep `data-group-toggle`/`data-group-content` markers and localStorage persistence assertions, adjusted for the Bootstrap-based toggle wiring

### Implementation for User Story 3

- [X] T017 [US3] Rewrite the group collapse interaction in `app/static/app.js` to use **Bootstrap's Collapse component** while preserving the existing persisted state behavior: retain `data-group-toggle`/`data-group-content` attributes for state-keying and re-apply the saved open/closed state on load using the Bootstrap collapse API/events
- [X] T018 [US3] Ensure the group header + collapse markup in `app/templates/index.html` works in BOTH the desktop right column and the mobile stacked layout with correct Bootstrap Collapse markup (`data-bs-toggle="collapse"` + a target)

**Checkpoint**: All user stories are independently functional and reflow correctly; group collapse works in both placements.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation.

- [X] T019 [P] Update `config/example.yaml` (only if useful) to clearly demonstrate the bookmark sidebar layout; otherwise leave unchanged (no schema change permitted)
- [X] T020 Run the full suite `uv run pytest` and confirm all tests pass in a clean run (contract + unit + integration)
- [X] T021 Execute the `specs/002-bookmarks-sidebar-layout/quickstart.md` validation scenarios V1–V6 (desktop right, mobile below, reflow, collapse, offline/vendored Bootstrap, no-bookmark state) to confirm end-to-end behavior

**Checkpoint**: Feature complete and validated; no remaining UIKit references or remote asset URLs.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Bootstrap assets present) — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational completion
  - US1 (Phase 3) and US2 (Phase 4) can proceed in parallel, or sequentially (P1 → P1)
  - US3 (Phase 5) builds on the grid foundation and the app.js collapse rewrite — best after US1/US2
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependency on other stories
- **User Story 2 (P1)**: Can start after Foundational — shares `app/templates/index.html` and `app/static/app.css` with US1, so sequence or coordinate carefully (same files)
- **User Story 3 (P2)**: Depends on the Bootstrap grid (US1/US2) and the collapse/JS foundation — significantly overlaps `app/templates/index.html`, `app/static/app.js`

### Within Each User Story

- Tests written FIRST and confirmed to FAIL before implementation
- Template/markup before CSS/JS behavior
- Layout (grid classes) before interaction (collapse)

### Parallel Opportunities

- T001, T002, T003 (Phase 1 vendoring) are independent and can run in parallel
- T004/T005/T006 (Phase 2) touch different files and can run in parallel
- Within each story, the [P]-marked test tasks can run in parallel
- **Note**: US1/US2/US3 all touch `app/templates/index.html` and `app/static/app.css`/`app.js`. To avoid conflicts, implement the grid (US1), mobile stacking (US2), and collapse (US3) sequentially within the same files, or have a single implementer own the shared template/CSS/JS.

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (update/add layout + offline assertions):
Task: "Update tests/integration/test_mobile_layout.py for Bootstrap right-column layout"
Task: "Add offline /static/bootstrap/ reference test to tests/integration/test_mobile_layout.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (vendor Bootstrap, remove UIKit)
2. Complete Phase 2: Foundational (template loads Bootstrap, base CSS)
3. Complete Phase 3: User Story 1 (right-column grid on desktop)
4. **STOP and VALIDATE**: Test US1 independently (desktop right column + offline assets)
5. Deploy/demo if ready — even before mobile/reflow stories are done, the desktop layout + offline migration alone delivers the core user ask

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (Bootstrap, offline, no UIKit)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (mobile stack)
4. Add User Story 3 → Test independently → Deploy/Demo (reflow + collapse polish)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:
- Team completes Setup + Foundational together
- Once Foundational is done, bookmarks grid (US1) and the offline/asset work are separable; but because US1/US2/US3 share `index.html`, app.css, and app.js, prefer a **single owner** for those shared files, with tests owned in parallel by another developer

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (constitution Principle IV)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **Security (non-negotiable per constitution)**: do NOT introduce any remote/CDN asset URLs; all Bootstrap assets must remain vendored locally under `app/static/bootstrap/`; all rendered URL content remains validated/escaped per the existing `app/security.py` contract
