---

description: "Task list for Header Search Bar feature implementation"
---

# Tasks: Header Search Bar

**Input**: Design documents from `/specs/011-header-search-bar/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests ARE included. The project constitution (Principle IV - Testability, NON-NEGOTIABLE) mandates test-first development, contract tests for module boundaries, and integration tests for cross-module behavior.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Spec contains a single user story (US1).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `tests/` at repository root (Flask web app)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

No setup tasks required — the Flask project already exists with established structure, dependencies (Flask, PyYAML), Bootstrap vendored assets, and pytest test suite. This feature adds to existing files only.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before the user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T001 Create `_parse_search_engine` and `_parse_search_engine_icon` helper functions in app/schema.py that validate the new config keys (search engine must be a string containing `{query}`; icon must be a valid http/https URL via `validate_url`)
- [X] T002 Add `search_engine` field to `DashboardConfig` dataclass in app/model.py (type `str | None`, default `None`)
- [X] T003 Add `search_engine_icon` field to `DashboardConfig` dataclass in app/model.py (type `str | None`, default `None`)
- [X] T004 Update `parse_dashboard` in app/schema.py to populate `search_engine` and `search_engine_icon` from YAML config using the helpers from T001

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Search the Web from the Dashboard Header (Priority: P1) 🎯 MVP

**Goal**: Add a search bar to the dashboard navbar that submits queries to a configurable search engine in a new tab, with a configurable search engine icon to the left of the input. Hidden on mobile.

**Independent Test**: Load the homepage (or config page) in a desktop browser, type a query, and submit — a new tab opens with results from the configured engine. On a mobile viewport (<768px), the search bar and icon are completely hidden (zero space). With an icon configured, the icon loads to the left of the input; with none/broken, the default magnifying-glass icon shows.

### Tests for User Story 1 (write FIRST, ensure they FAIL before implementation) ⚠️

- [X] T005 [P] [US1] Contract test for `search_engine` parsing (default fallback, missing `{query}`, non-string) in tests/contract/test_config_schema.py
- [X] T006 [P] [US1] Contract test for `search_engine_icon` parsing (valid URL, invalid URL, absent → fallback) in tests/contract/test_config_schema.py
- [X] T007 [P] [US1] Unit test for `parse_dashboard` returning `search_engine` and `search_engine_icon` values in tests/unit/test_schema.py
- [X] T008 [P] [US1] Integration test that homepage navbar contains the search form with `target="_blank"`, `method="GET"`, input name `q`, and `rel="noopener"` in tests/integration/test_navbar.py
- [X] T009 [P] [US1] Integration test that config page navbar contains the search form in tests/integration/test_navbar.py
- [X] T010 [P] [US1] Integration test that default `bi-search` icon renders when no `search_engine_icon` is configured in tests/integration/test_navbar.py
- [X] T011 [P] [US1] Integration test that configured `search_engine_icon` image URL renders with `onerror` fallback markup in tests/integration/test_navbar.py
- [X] T012 [P] [US1] Integration test that search form and icon use `d-none d-md-flex` (hidden on mobile, zero space) in tests/integration/test_mobile_layout.py
- [X] T013 [P] [US1] Integration test for custom `search_engine` taking effect in form `action` on next load in tests/integration/test_navbar.py

### Implementation for User Story 1

- [X] T014 [US1] Add `search_engine` and `search_engine_icon` to the `render_template` call in the `home()` view in app/views.py
- [X] T015 [US1] Add `search_engine` and `search_engine_icon` to the `render_template` call in the `view_config()` view in app/views.py
- [X] T016 [P] [US1] Add search bar form (with configurable icon to the left of the input, default `bi-search` fallback, `d-none d-md-flex`, `target="_blank"`, `rel="noopener"`, input name `q`) to the navbar in app/templates/index.html
- [X] T017 [P] [US1] Add the same search bar form to the navbar in app/templates/config.html
- [X] T018 [US1] Add minimal `.search-engine-icon` sizing CSS (if beyond Bootstrap utilities) to app/static/app.css
- [X] T019 [US1] Add `search_engine` and `search_engine_icon` example key/value pairs to config/example.yaml

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect the feature holistically

- [X] T020 [P] Update README/quickstart documentation if developer workflow or config schema documentation changes (Principle I)
- [X] T021 Run `pytest` from repo root and confirm the full suite passes
- [X] T022 [P] Run `quickstart.md` validation scenarios (desktop search, mobile hide, custom icon, broken icon fallback)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Not needed (existing project)
- **Foundational (Phase 2)**: No external dependencies - BLOCKS user story
- **User Story (Phase 3)**: Depends on Foundational phase completion
- **Polish (Final Phase)**: Depends on User Story completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - sole user story

### Within User Story 1

- Tests (T005–T013) MUST be written and FAIL before implementation (constitution Principle IV, red-green-refactor)
- Data model/schema (T001–T004) before views (T014–T015)
- View data passing before templates
- Implementation before final example.yaml update

### Parallel Opportunities

- All Foundational tasks (T001, T002, T003, T004) can be parallel, but T002/T003 (model fields) must precede T004 (parse) logically; T001 helper precedes T004
- All test tasks (T005–T013) can run in parallel
- Template tasks T016 and T017 (index.html and config.html) can run in parallel
- View tasks T014 and T015 (home and view_config) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all test tasks together (write failing tests first):
Task: "Contract test for search_engine parsing in tests/contract/test_config_schema.py"
Task: "Contract test for search_engine_icon parsing in tests/contract/test_config_schema.py"
Task: "Unit test for parse_dashboard search fields in tests/unit/test_schema.py"
Task: "Integration test for navbar search form in tests/integration/test_navbar.py"
Task: "Integration test for config page search form in tests/integration/test_navbar.py"
Task: "Integration test for default bi-search icon in tests/integration/test_navbar.py"
Task: "Integration test for configured icon onerror markup in tests/integration/test_navbar.py"
Task: "Integration test for d-none d-md-flex mobile hiding in tests/integration/test_mobile_layout.py"
Task: "Integration test for custom search_engine in form action in tests/integration/test_navbar.py"

# Launch the two template tasks together:
Task: "Add search bar form to app/templates/index.html"
Task: "Add search bar form to app/templates/config.html"

# Launch the two view tasks together:
Task: "Add search fields to home() render_template in app/views.py"
Task: "Add search fields to view_config() render_template in app/views.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (schema/model)
2. Write failing tests (T005–T013)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run tests + quickstart scenarios
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. This feature is a single user story (US1) — the full feature is the MVP

---

## Notes

- [P] tasks = different files, no dependencies
- [US1] label maps task to the user story for traceability
- The user story should be independently completable and testable
- Verify tests fail before implementing (constitution Principle IV)
- Commit after each task or logical group
- Stop at the checkpoint to validate the story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
