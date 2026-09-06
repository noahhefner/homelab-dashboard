# Tasks: Disable Search and Bookmarks

**Input**: Design documents from `/specs/012-disable-search-bookmarks/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks ARE included. Per Constitution Principle IV (Test-First, NON-NEGOTIABLE), tests MUST be written first, verified to fail (RED), then made to pass (GREEN).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project: `app/` and `tests/` at repository root (see plan.md Project Structure)

## Tech Stack (from plan.md)

- Python 3.14, Flask, PyYAML, Jinja2 templates, Bootstrap 5 (vendored)
- Test: pytest + BeautifulSoup (`tests/soup_utils.py`, `tests/conftest.py`)
- Lint: ruff (Python), djlint (templates)
- Config: live-reloaded YAML via `ConfigLoader` (`app/config.py`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify the project baseline before any Test-First changes

**No new setup is required** — this feature builds directly on the existing Flask app. The only setup task establishes a green-test baseline (red-green discipline and Principle IV).

- [x] T001 Verify the current test suite passes as a baseline: run `pytest` and confirm all tests pass before any feature changes

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared parsing/comparison infrastructure that BOTH user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Add `_parse_bool_flag(value, default=True)` helper in `app/schema.py` that returns `value` only when it is a `bool`, otherwise returns `default` (per research R3 - invalid values fall back to shown)
- [x] T003 [P] Add `show_search` and `show_bookmarks` to the recognized top-level keys list assertion in `tests/contract/test_config_schema.py` (the list currently includes `search_engine`/`search_engine_icon` around lines 42-52)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Disable the Search Bar (Priority: P1) MVP

**Goal**: A top-level `show_search` flag that hides the navbar search bar (and its icon) on all pages with a navbar, occupying zero space, with "shown" as the default.

**Independent Test**: Load the homepage and the `/config` page with the default config (search bar present) and with `show_search: false` (no search `<form>` in the served HTML, zero space, brand/theme-toggle still present). No JS or other features required.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T004 [P] [US1] Unit tests for `show_search` parsing in `tests/unit/test_schema.py`: absent -> True, explicit `true`/`false` preserved, non-boolean (string/number/null) -> falls back to True with no error
- [x] T005 [P] [US1] Integration tests for search bar hiding in `tests/integration/test_visibility_toggles.py` (new file): default config renders the search form on `/` and `/config`; `show_search: false` renders no search form on either page; navbar brand and theme-toggle still render; `search_engine`/`search_engine_icon` values present while hidden cause no error
- [x] T006 [P] [US1] Contract tests for `show_search` rules in `tests/contract/test_config_schema.py`: absent -> True, valid `false` -> False, non-boolean falls back to True

### Implementation for User Story 1

- [x] T007 [US1] Add `show_search: bool = True` field to `DashboardConfig` in `app/model.py`
- [x] T008 [US1] Parse `show_search` in `parse_dashboard()` in `app/schema.py` using the `_parse_bool_flag` helper (depends on T002, T007)
- [x] T009 [US1] Pass `show_search=config.show_search` to both templates in `app/views.py` (`home()` and `view_config()`)
- [x] T010 [P] [US1] Gate the search `<form>` with `{% if show_search %}` in `app/templates/index.html` (wrap lines 33-66)
- [x] T011 [P] [US1] Gate the search `<form>` with `{% if show_search %}` in `app/templates/config.html` (wrap lines 35-68)
- [x] T012 [P] [US1] Document `show_search: true` with a short comment in `config/example.yaml` (top-level, near `editor`)

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Disable the Bookmarks (Priority: P1)

**Goal**: A top-level `show_bookmarks` flag that hides the entire bookmarks section on the homepage, removes the reserved column, and lets the tiles expand to full width, with "shown" as the default.

**Independent Test**: Load the homepage with the default config (bookmark groups shown, tiles `col-lg-9`) and with `show_bookmarks: false` (no bookmarks `<aside>`, no bookmark group rendered, tiles full width `col-12`). The search bar is unaffected.

**NOTE**: US1 and US2 share `app/model.py`, `app/schema.py`, `app/views.py`, and `config/example.yaml`. Implement US2 sequentially after US1 to avoid same-file conflicts (see Dependencies & Execution Order).

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T013 [P] [US2] Unit tests for `show_bookmarks` parsing in `tests/unit/test_schema.py`: absent -> True, explicit `true`/`false` preserved, non-boolean -> falls back to True with no error
- [x] T014 [P] [US2] Integration tests for bookmarks hiding in `tests/integration/test_visibility_toggles.py`: default config renders the bookmarks `<aside>`; `show_bookmarks: false` renders no bookmark group and tiles section uses full width (no `col-lg-9`)
- [x] T015 [P] [US2] Contract tests for `show_bookmarks` rules in `tests/contract/test_config_schema.py`: absent -> True, valid `false` -> False, non-boolean falls back to True

### Implementation for User Story 2

- [x] T016 [US2] Add `show_bookmarks: bool = True` field to `DashboardConfig` in `app/model.py`
- [x] T017 [US2] Parse `show_bookmarks` in `parse_dashboard()` in `app/schema.py` using the `_parse_bool_flag` helper (depends on T002, T016)
- [x] T018 [US2] Pass `show_bookmarks=config.show_bookmarks` to the homepage template in `app/views.py` (`home()`)
- [x] T019 [US2] Gate the bookmarks `<aside>` with `{% if show_bookmarks %}` in `app/templates/index.html` and make the tiles section class `col-12 {{ 'col-lg-9' if show_bookmarks }}` so tiles expand to full width when bookmarks are hidden
- [x] T020 [P] [US2] Document `show_bookmarks: true` with a short comment in `config/example.yaml` (top-level, next to `show_search`)

**Checkpoint**: At this point, User Story 2 is fully functional; the search bar toggle (US1) and bookmarks toggle (US2) both work independently.

---

## Phase 5: User Story 3 - Disable Both for a Minimal Dashboard (Priority: P2)

**Goal**: Combining `show_search: false` and `show_bookmarks: false` yields a clean, fully functional dashboard (navbar + tiles) with no errors.

**Independent Test**: Load the homepage and `/config` with both flags `false`; confirm the homepage renders the navbar and tiles only (no search form, no bookmarks), the config page renders normally, and no error page is served.

**NOTE**: FR-007 independence is guaranteed by the two separate flags implemented in US1/US2. This phase is a test + validation phase; no new code is expected beyond the test itself (YAGNI, Principle V).

### Tests for User Story 3

> **NOTE: Write this test FIRST, ensure it FAILS before implementation**

- [x] T021 [P] [US3] Integration test for the combined case in `tests/integration/test_visibility_toggles.py`: with `show_search: false` and `show_bookmarks: false`, the homepage serves `200`, contains the navbar brand, contains tile content, and contains no search `<form>` and no bookmarks `<aside>`; also assert independence by checking `show_search: false` with bookmarks default still renders the bookmark `<aside>` (and vice versa)

### Implementation for User Story 3

- [x] T022 [US3] Manual validation only: run the "Hide both" and "Independently toggled" scenarios from `specs/012-disable-search-bookmarks/quickstart.md` against a running server and confirm the behavior matches; no code change is expected

**Checkpoint**: All user stories are independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates and end-to-end validation across all stories

- [x] T023 [P] Run `ruff check app tests` and `djlint --lint app/templates` on changed files and fix any issues
- [x] T024 Run the full suite `pytest` and confirm all tests pass (existing + new)
- [x] T025 Execute all validation scenarios in `specs/012-disable-search-bookmarks/quickstart.md` against a running server and confirm expected outcomes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories (`_parse_bool_flag` is shared)
- **User Stories (Phase 3+)**: Depend on Foundational completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - no dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - shares `app/model.py`, `app/schema.py`, `app/views.py`, `config/example.yaml` with US1, so implement SEQUENTIALLY after US1
- **User Story 3 (P2)**: Depends on US1 and US2 (combines both flags) - test/validation only

### Within Each User Story

- Tests MUST be written and FAIL before implementation (RED)
- Model field (T007/T016) before schema parsing (T008/T017) before view wiring (T009/T018) before template gating (T010/T011/T019)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T003 (foundational contract keys) is [P] and independent of T002
- All test tasks within a story (differing files: `test_schema.py`, `test_visibility_toggles.py`, `test_config_schema.py`) are [P]
- T010/T011 (different template files) are [P]
- T012/T020 (documentation edits to `config/example.yaml`) conflict with each other across stories - do not run US1 and US2 example-config edits concurrently

---

## Parallel Example: User Story 1

```bash
# Launch all User Story 1 tests together (different files):
Task: "T004 Unit tests for show_search parsing in tests/unit/test_schema.py"
Task: "T005 Integration tests for search hiding in tests/integration/test_visibility_toggles.py"
Task: "T006 Contract tests for show_search in tests/contract/test_config_schema.py"

# Then launch template + example edits together (different files):
Task: "T010 Gate search form in app/templates/index.html"
Task: "T011 Gate search form in app/templates/config.html"
Task: "T012 Document show_search in config/example.yaml"
```

## Parallel Example: User Story 2

```bash
# Launch all User Story 2 tests together:
Task: "T013 Unit tests for show_bookmarks parsing in tests/unit/test_schema.py"
Task: "T014 Integration tests for bookmarks hiding in tests/integration/test_visibility_toggles.py"
Task: "T015 Contract tests for show_bookmarks in tests/contract/test_config_schema.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (baseline tests green)
2. Complete Phase 2: Foundational (`_parse_bool_flag` + contract keys)
3. Complete Phase 3: User Story 1 (search bar toggle)
4. **STOP and VALIDATE**: Test User Story 1 independently (`pytest tests/unit/test_schema.py -k show; pytest tests/integration/test_visibility_toggles.py -k search`)
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. User Story 1 (search toggle) → Test independently → Deploy/Demo (MVP): both P1 stories together deliver the complete feature - search and bookmarks toggles
3. User Story 2 (bookmarks toggle) → Test independently → Deploy/Demo
4. User Story 3 (combined, test/validation) → Deploy/Demo

### Parallel Team Strategy

- US1 and US2 share `model.py`/`schema.py`/`views.py`/`example.yaml`, so a single developer should implement them sequentially (US1 then US2).
- Test-writing tasks (different test files) can be distributed in parallel within a story.
- Template gating tasks (index.html vs config.html) are parallelizable.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to the specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (Test-First, Principle IV)
- Commit after each task or logical group
- Stop at any checkpoint to validate a story independently
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break independence