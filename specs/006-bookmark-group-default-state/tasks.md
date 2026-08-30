# Tasks: Bookmark Group Default State

**Input**: Design documents from `/specs/006-bookmark-group-default-state/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/group-default-state.md, quickstart.md

**Tests**: Test tasks are included because the project Constitution (Testing, Principle IV) makes test-first non-negotiable: tests MUST be written before the code they validate and pass in a clean run. All tests are deterministic static-markup / schema-model unit assertions (no network needed).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project web app**: `app/`, `tests/` at repository root (per plan.md Structure Decision)
- Config parsing in `app/schema.py`, models in `app/model.py`, template `app/templates/index.html`, client logic in `app/static/app.js`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the baseline is green before any changes. No new dependencies or infrastructure are required for this feature (the change reuses the existing YAML config and localStorage collapse machinery).

- [X] T001 Run the existing test suite (`uv run pytest`) and confirm the baseline passes before implementation

**Checkpoint**: Baseline green; no new deps/assets needed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: User Story 1 is the P1 story and contains the model/schema change that everything else builds on. There is no separate blocking infrastructure, so implementation proceeds directly into the user-story phases in priority order.

---

## Phase 3: User Story 1 - Configure a Group's Initial State (Priority: P1) 🎯 MVP

**Goal**: Add an optional per-group `collapsed` config value so a group starts open or closed on page load (default: open).

**Independent Test**: With a group `collapsed: true` and no saved user choice, the rendered page marks that group's toggle as defaulting to closed; with `collapsed: false`/unset it defaults to open.

### Tests for User Story 1 ⚠️ (write first, ensure they FAIL)

- [X] T002 [P] [US1] Unit test: `collapsed: true` parses to `True`, `collapsed: false`/absent parses to `False` in `tests/unit/test_schema.py`
- [X] T003 [P] [US1] Unit test: non-boolean `collapsed` raises a config validation error in `tests/unit/test_schema.py`
- [X] T004 [P] [US1] Integration test: a `collapsed: true` group's toggle renders the default-collapsed marker, and an unset group renders the open default, in `tests/integration/test_bookmark_groups.py`

### Implementation for User Story 1

- [X] T005 [P] [US1] Add `collapsed: bool = False` field to the `BookmarkGroup` dataclass in `app/model.py`
- [X] T006 [US1] Parse and validate the `collapsed` boolean in `_parse_group` (default `False`; reject non-boolean) in `app/schema.py` (depends on T005)

### Implementation for User Story 1 (template + JS)

- [X] T007 [US1] Emit the configured default onto the group toggle as a data attribute (e.g., `data-default-collapsed="true|false"`) in `app/templates/index.html`
- [X] T008 [US1] Update the collapse logic in `app/static/app.js` so that when there is no saved user choice for a group, the client falls back to the config-derived default from the data attribute (T007); when the attribute is absent, keep the existing open default

**Checkpoint**: US1 is complete — a group configured `collapsed: true` (no saved choice) renders collapsed; `false`/unset renders open.

---

## Phase 4: User Story 2 - Honor a User's Explicit Choice (Priority: P2)

**Goal**: Ensure a user's previously saved open/closed choice for a group takes precedence over the config default.

**Independent Test**: With a group configured `collapsed: true`, if a saved "open" choice exists for it, the group renders open across reloads (the saved choice beats the config default).

### Tests for User Story 2 ⚠️ (write first, ensure they FAIL)

- [X] T009 [P] [US2] Unit test: the JS collapse logic prefers a saved `localStorage` value over the config-derived default in `tests/unit/test_bookmark_group_state.py`

### Implementation for User Story 2

- [X] T010 [US2] Confirm/refine `app/static/app.js` so a saved per-group value takes precedence over the config default when initializing each group's state (complements T008)

**Checkpoint**: US2 is complete — saved user choices override config defaults; both US1 and US2 now behave independently and correctly together.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and example-config coverage that make the new option discoverable.

- [X] T011 [P] Add an example `collapsed: true` group to `config/example.yaml` and document the per-group `collapsed` option in `README.md`
- [X] T012 [P] Validate the end-to-end behavior against `specs/006-bookmark-group-default-state/quickstart.md` (V1–V5) and confirm `uv run pytest` passes cleanly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — baseline check runs first.
- **User Story 1 (Phase 3)**: Depends on Setup (baseline green). Contains the model/schema/template/JS changes.
- **User Story 2 (Phase 4)**: Depends on US1 (the JS precedence logic complements the config-default handling threaded through the same code paths).

### User Story Dependencies

- **US1 (P1)**: No upstream story deps — the MVP slice.
- **US2 (P2)**: Depends on US1; shares `app/static/app.js` with US1, so the two stories run sequentially.

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Constitution test-first).
- Model → schema → template → JS within US1.

### Parallel Opportunities

- US1 tests (T002/T003/T004) are [P] within the story.
- Model (T005) and schema (T006) are sequential (schema depends on the field); T007/T008 build after.
- US2's single test (T009) is independent of US1's implementation files and can be written early.
- Polish tasks (T011/T012) are [P] and independent.

---

## Parallel Example: User Story 1 tests

```bash
# Launch all US1 tests together (test-first window):
Task: "Unit test: collapsed true/false/absent parsing in tests/unit/test_schema.py"
Task: "Unit test: non-boolean collapsed raises in tests/unit/test_schema.py"
Task: "Integration test: collapsed default marker on rendered toggle in tests/integration/test_bookmark_groups.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (baseline green).
2. Complete Phase 3: User Story 1 (per-group default state).
3. **STOP and VALIDATE**: Confirm `uv run pytest` is green and a `collapsed: true` group renders collapsed on load.
4. Deploy/demo the MVP.

### Incremental Delivery

1. Setup → US1 (config default) → validate.
2. Add US2 (saved choice precedence) → validate.
3. Polish + example config/docs → full green run.

### Parallel Team Strategy

1. Team confirms baseline (Phase 1).
2. Developer A: US1 (model → schema → template → JS).
3. Developer B: may write the US2 test (T009) and Polish (T011/T012) in parallel, but US2's JS change (T010) lands after US1's JS change.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps each task to its user story for traceability.
- US1 and US2 both touch `app/static/app.js` and `app/templates/index.html`, so they must run sequentially (not parallel) despite being separate stories.
- The `collapsed` value is validated strictly as a boolean; a non-boolean value is a config error, consistent with the project's strict parsing.
- Verify tests fail before implementing, then pass in a clean run (Constitution Principle IV).
