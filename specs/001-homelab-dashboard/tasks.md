---
description: "Task list for homelab-dashboard homepage feature implementation"
---

# Tasks: Homelab Dashboard Homepage

**Input**: Design documents from `/specs/001-homelab-dashboard/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included because project governance (Constitution Principle IV — Test-First, NON-NEGOTIABLE) requires tests written before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `config/`, `tests/` at repository root (per plan.md)
- Python 3.14 project managed with `uv` (no pip). Run tests with `uv run pytest`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize uv project: create `pyproject.toml`, add dependencies `flask`, `pyyaml`, `pytest`, generate `uv.lock` via `uv add flask pyyaml` and `uv add --dev pytest`
- [x] T002 [P] Create directory structure: `app/`, `app/templates/`, `app/static/uikit/`, `config/`, `tests/contract/`, `tests/integration/`, `tests/unit/`
- [x] T003 [P] Vendor UIkit assets (CSS/JS, no jQuery) into `app/static/uikit/` from the official build
- [x] T004 [P] Create starter config at `config/example.yaml` (a few services + 2 bookmark groups) per `contracts/config-contract.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Flask app factory in `app/__init__.py` (creates app, registers routes, wires CONFIG_PATH from env with default `config/example.yaml`)
- [x] T006 Create entry point in `app/server.py` that starts the Flask dev server
- [x] T007 Create security helper in `app/security.py` that validates URLs (http/https only) and HTML-escapes all renderable strings (name/label/url)
- [x] T008 [P] Create error page template for invalid config in `app/templates/error.html` (renders a clear, readable error message per FR-010)

### Tests for Foundational (Test-First) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T009 [P] Unit test for security helper URL validation + escaping in `tests/unit/test_security.py`
- [x] T010 [P] Unit test for app factory config-path wiring in `tests/unit/test_appfactory.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: Config & Data Layer (Foundational for US1)

**Purpose**: Model + schema + config loader with live reload. Required by US1-US4 (no story renders without config parsing).

- [x] T011 [P] Create data model classes (`Service`, `Bookmark`, `BookmarkGroup`, `DashboardConfig`) in `app/model.py` per `data-model.md`
- [x] T012 Create config parser + validator in `app/schema.py` that converts raw YAML dicts into model objects with validation rules from `contracts/config-contract.md`
- [x] T013 Create config loader with live reload in `app/config.py` that mtime-checks the mounted YAML and re-parses only on change (per research.md R2); exposes the current `DashboardConfig` snapshot
- [x] T014 [P] Create `config` unit tests for schema validation (valid config, missing required fields, invalid URL, unknown keys ignored) in `tests/unit/test_schema.py`
- [x] T015 [P] Create `config` contract test for the config file schema in `tests/contract/test_config_schema.py` (validate against `contracts/config-contract.md`)

**Checkpoint**: Config + data layer complete; all user stories can now build on it

---

## Phase 4: User Story 1 - View Services as a Landmark Homepage (Priority: P1) 🎯 MVP

**Goal**: Render every configured service as a clickable tile with an icon (or monogram fallback) that navigates to the service URL.

**Independent Test**: Configure a few services in `config/example.yaml`, load the homepage, and confirm every service appears as a tile with name + icon (or monogram fallback) and clicking it opens the destination URL.

### Tests for User Story 1 (Test-First) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T016 [P] [US1] Unit test for service-tile rendering/fallback logic in `tests/unit/test_views_services.py`
- [x] T017 [P] [US1] Integration test that a rendered page contains all configured service names/links in `tests/integration/test_homepage_services.py`

### Implementation for User Story 1

- [x] T018 [US1] Add homepage route in `app/views.py` that renders `app/templates/index.html` with the services list (depends on T011, T012, T013)
- [x] T019 [P] [US1] Create homepage template `app/templates/index.html` linking UIkit static assets and rendering service tiles
- [x] T020 [US1] Render service tiles with icon, plus monogram/fallback when icon missing or unreachable (per US1-3, FR-003), escaping via `app/security.py`
- [x] T021 [US1] Make each service tile an anchor that opens the service URL in a new tab with `rel="noopener noreferrer"` (per FR-002, HTTP contract)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 5: User Story 2 - Configure Everything via a Single YAML File (Priority: P1)

**Goal**: Editing the mounted YAML and refreshing the page reflects changes without restarting the backend or container.

**Independent Test**: With the app running, edit `config/example.yaml` (add a service, remove a bookmark), save, and refresh — the change appears with no restart (US2-1..3; FR-008).

### Tests for User Story 2 (Test-First) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T022 [P] [US2] Integration test for live reload: modify the config file, request the page, assert the new data is reflected in `tests/integration/test_config_reload.py`
- [x] T023 [P] [US2] Integration test for invalid-config error page in `tests/integration/test_invalid_config.py`
- [x] T024 [P] [US2] Unit test for the mtime-based change detector (config change vs stale) in `tests/unit/test_config_loader.py`

### Implementation for User Story 2

- [x] T025 [US2] Wire live-reload into the request path in `app/config.py`/`app/views.py` so each page request uses a fresh config when the file changed (per research.md R2, FR-008)
- [x] T026 [US2] Handle invalid/malformed YAML: render `app/templates/error.html` with a clear message instead of a blank/broken page (per FR-010, US2-3)
- [x] T027 [US2] Reflect config edits on refresh for both adding services and removing bookmarks in `app/views.py` (per US2-1, US2-2, FR-001)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 6: User Story 3 - Manage a Large Number of Bookmarks Gracefully (Priority: P2)

**Goal**: Display bookmarks in named, collapsible groups that stay usable at scale (150+ bookmarks, FR-005/FR-009).

**Independent Test**: Configure 100+ bookmarks across 5+ groups and confirm they render within groups, collapse/expand works with state persistence, and the page stays responsive with no layout breakage (US3-1..3; FR-006).

### Tests for User Story 3 (Test-First) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T028 [P] [US3] Integration test that bookmark groups render grouped bookmarks in `tests/integration/test_bookmark_groups.py`
- [x] T029 [P] [US3] Unit test for group collapse/expand state logic in `tests/unit/test_bookmark_group_state.py`

### Implementation for User Story 3

- [x] T030 [US3] Render bookmark groups with headings and grouped bookmarks in `app/templates/index.html` (per FR-005)
- [x] T031 [US3] Implement collapsible/expandable bookmark groups with state persisted across visits (per FR-006, US3-3) using UIkit accordion + `localStorage`
- [x] T032 [P] [US3] Add group-toggle JavaScript in `app/static/app.js`
- [x] T033 [US3] Ensure a large number of bookmarks renders without layout breakage in `app/templates/index.html` and within the SC-004 load target (per FR-009)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 4 - Use the Homepage on Mobile Devices (Priority: P2)

**Goal**: The homepage renders and functions correctly on small screens with tap-friendly tiles (FR-007).

**Independent Test**: Open the page at phone width (dev tools or real device) and confirm tiles/bookmark groups arrange into a usable single/two-column layout with no horizontal scroll, and tapping a tile works without hover (US4-1..3; FR-007).

### Tests for User Story 4 (Test-First) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T034 [P] [US4] Integration/smoke test asserting responsive classes + no-logic that breaks at narrow widths in `tests/integration/test_mobile_layout.py`

### Implementation for User Story 4

- [x] T035 [US4] Ensure homepage uses UIkit responsive/grid classes in `app/templates/index.html` so tiles and groups reflow to a no-horizontal-scroll layout on mobile (per FR-007, US4-1)
- [x] T036 [US4] Ensure tiles/links are tap-friendly with accessible touch target sizes in `app/templates/index.html` and open correctly on tap (per FR-007, US4-2)
- [x] T037 [US4] Add dashboard-specific responsive styling in `app/static/app.css` (per FR-007, US4-3)

**Checkpoint**: All user stories now functional; ready for polish

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T038 [P] Write `Dockerfile` (single container, python:3.14-slim, deps installed via `uv`, env `CONFIG_PATH`) per research.md R4
- [x] T039 [P] Write `docker-compose.yml` mounting `config/example.yaml` via a volume per quickstart.md
- [x] T040 Update `README.md` with setup, local run, Docker run, and config instructions
- [x] T041 Create `config/example.yaml` final seed with 100+ bookmarks across groups to demonstrate scale (if not already present)
- [x] T042 Run full test suite and quickstart.md validation scenarios (`uv run pytest`), confirm SC-001..SC-006 are satisfied
- [x] T043 [P] Security hardening review: confirm all rendered URLs/labels escaped and URLs validated across `app/security.py` and `app/templates/`, and no secrets committed in `config/` (per Constitution Security Requirements)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **Config & Data Layer (Phase 3)**: Depends on Foundational; BLOCKS all user stories (US1-US4 cannot render without config parsing)
- **User Stories (Phase 4+)**: All depend on Phases 1-3
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Phases 1-3 (config + data layer). No dependency on other stories.
- **User Story 2 (P1)**: Depends on Phases 1-3. Integrates with US1's page rendering but independently testable.
- **User Story 3 (P2)**: Depends on Phases 1-3. Builds on US1/2 page rendering; independently testable.
- **User Story 4 (P2)**: Depends on Phases 1-3. Styling on top of US1/2/3 output; independently testable.

### Within Each User Story

- Tests (included, per Constitution test-first) MUST be written and FAIL before implementation
- Config/data layer (Phase 3) before story implementation
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Foundational tasks marked [P] can run in parallel (within Phase 2)
- Phase 3 model/schema/loader tasks marked [P] can run in parallel (schema depends on model)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members after Phase 3

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for service-tile rendering/fallback in tests/unit/test_views_services.py"
Task: "Integration test homepage services in tests/integration/test_homepage_services.py"

# Launch all impl tasks for User Story 1:
Task: "Create homepage template app/templates/index.html"
Task: "Render service tiles with icon/fallback escaping"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: Config & Data Layer (CRITICAL - blocks rendering)
4. Complete Phase 4: User Story 1 (services render + navigate)
5. **STOP and VALIDATE**: Test User Story 1 independently (`uv run pytest`)
6. Deploy/demo if ready (even without bookmarks/mobile polish)

### Incremental Delivery

1. Complete Setup + Foundational + Data Layer → Foundation ready
2. Add User Story 1 (services homepage) → Test independently → MVP
3. Add User Story 2 (live config reload) → Test independently
4. Add User Story 3 (bookmark groups at scale) → Test independently
5. Add User Story 4 (mobile) → Test independently
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational + Data Layer together
2. Once Phase 3 is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests MUST be written first and verified failing before implementation (Constitution Principle IV)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Run tests with `uv run pytest`
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
