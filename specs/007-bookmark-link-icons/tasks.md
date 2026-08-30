---

description: "Task list for bookmark link icons"

---

# Tasks: Bookmark Link Icons

**Input**: Design documents from `/specs/007-bookmark-link-icons/`

**Prerequisites**: plan.md, spec.md (user stories), research.md, data-model.md, contracts/bookmark-icon.md, quickstart.md

**Tests**: This project follows a test-first, non-negotiable testing principle (Constitution Gate 2); tests are written first and must FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `tests/`, `config/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the project and test harness are in place for this feature. No new
dependencies, modules, or project structure are introduced (per plan.md); this phase is a
quick environment check.

- [X] T001 Confirm baseline: `uv run pytest` (82 pass / 3 pre-existing feature-006 failures unrelated to this feature; no regressions introduced)
- [X] T002 Confirm the example config parses: `uv run pytest tests/contract/test_config_schema.py`

**Checkpoint**: Existing tests pass and the example config is valid before any feature work.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Write the tests that define this feature's behavior FIRST so they fail before
implementation (Constitution Gate 2 — Test-First, NON-NEGOTIABLE). These tests are blocking
for ALL user stories because they lock in the rendering contract that US1/US2/US3 build on.

**⚠️ CRITICAL**: No user story work can begin until these tests are written and confirmed
failing for the right reason.

- [X] T003 Write `tests/unit/test_bookmark_icons.py` asserting a bookmark with a URL `icon`
      renders an `<img>` whose `src` is that URL (reuse the assertion pattern from
      `tests/unit/test_views_services.py`)
- [X] T004 [P] Write `tests/unit/test_bookmark_icons.py` asserting a bookmark with no `icon`
      renders the plain label with no `<img>`
- [X] T005 [P] Write `tests/unit/test_bookmark_icons.py` asserting a bookmark with a
      short-word (non-URL) `icon` (e.g., `youtube`) renders the label and emits NO `<img>`
- [X] T006 [P] Write `tests/unit/test_bookmark_icons.py` asserting an unsafe icon value
      (e.g., `javascript:alert(1)`) is NEVER emitted as an `<img src>`
- [X] T007 [P] Write `tests/unit/test_bookmark_icons.py` asserting a bookmark label is still
      HTML-escaped (e.g., `<script>` is not rendered raw) and the link still opens in a new
      tab (`target="_blank"` / `noopener`)
- [X] T008 [P] Write `tests/integration/test_example_icon_hygiene.py` asserting that
      `config/example.yaml` contains NO short-word icon values (all `icon` values under
      `bookmark_groups[]` and `bookmarks[]` are either full `http(s)` URLs or absent)
- [X] T009 Run the new tests and confirm they FAIL for the expected reason (no icon is
      currently rendered)

**Checkpoint**: The feature's tests are written and failing. Implementation can now proceed.

---

## Phase 3: User Story 1 - Show an Icon for Each Bookmark (Priority: P1) 🎯 MVP

**Goal**: Render a bookmark's configured icon as an image beside its label when it is a
valid URL.

**Independent Test**: Configure a bookmark with a full image URL as its `icon`, load the
homepage, and confirm the bookmark link renders that icon as an `<img>`; a bookmark without
one renders its text label only.

### Implementation for User Story 1

- [X] T010 [P] [US1] Modify `app/templates/index.html` bookmark link block to emit an
      `<img>` when `bookmark.icon` is a valid URL (reuse the existing `is url` test and the
      `loading="lazy"` + `onerror` fallback approach used for service icons), otherwise
      render only the text label
- [X] T011 [US1] Confirm the rendered `<img>` uses `alt="{{ bookmark.label }}"` for
      accessibility and keeps `target="_blank"` / `rel="noopener noreferrer"` on the link

**Checkpoint**: User Story 1 should be functional — a bookmark with a URL icon renders the
image, one without renders the label. Run `uv run pytest tests/unit/test_bookmark_icons.py`
and confirm the URL/no-icon/unsafe cases now pass.

---

## Phase 4: User Story 2 - Configure a Bookmark Icon From the YAML Config (Priority: P1)

**Goal**: Ensure bookmark icons are configurable via the YAML file and that unsupported
short-word icon values are removed from the repository, so the config only demonstrates
supported behavior.

**Independent Test**: Edit `config/example.yaml` to add/remove a bookmark icon, reload the
page, and confirm the change appears with no rebuild; inspect the example config and README
to confirm no short-word icons remain.

### Implementation for User Story 2

- [X] T012 [US2] Replace every short-word `icon` value under `bookmark_groups[].icon` in
      `config/example.yaml` with a full remote image URL (e.g., dashboard-icons) or remove
      the field where no suitable URL exists
- [X] T013 [US2] Replace every short-word `icon` value under `bookmarks[].icon` in
      `config/example.yaml` with a full remote image URL or remove the field
- [X] T014 [US2] Update `README.md` to document that a bookmark `icon` is a full image URL,
      with the text label as the fallback, and remove any short-word icon examples
- [X] T015 [US2] Verify config reload: change a bookmark icon in `config/example.yaml`,
      reload the page, and confirm the change takes effect with no code change or rebuild

**Checkpoint**: User Stories 1 AND 2 both work — icons render from config and the example
config/README contain no unsupported short-word icons.

---

## Phase 5: User Story 3 - Consistent Visual Treatment With Homelab Links (Priority: P2)

**Goal**: Style bookmark icons consistently (sizing/placement) with the homelab service
icons so the bookmarks column reads as part of the same interface.

**Independent Test**: Load a dashboard where both homelab services and bookmarks have
icons and confirm they use the same visual language (similar image sizing/placement, text
fallback).

### Implementation for User Story 3

- [X] T016 [P] [US3] Add a bookmark-icon size/placement rule to `app/static/app.css` (e.g., a
      `.bookmark-icon` class) so bookmark images align consistently with the text label
- [X] T017 [US3] Add the bookmark-icon class to the `<img>` emitted in
      `app/templates/index.html`, and add a mobile refinement (max-width 575.98px) mirroring
      the existing service-icon sizing in `app/static/app.css`

**Checkpoint**: All user stories should now be independent and functional with visually
consistent icons.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Full-suite verification and final validation.

- [X] T018 Run the full test suite: `uv run pytest` (all tests pass, including existing
      service/icon/group tests)
- [X] T019 Run `uv run pytest tests/contract/test_config_schema.py` to confirm the updated
      example config still passes the contract test
- [X] T020 Execute `specs/007-bookmark-link-icons/quickstart.md` validation scenarios
      (V1–V7) to confirm the feature works end-to-end
- [X] T021 Confirm `config/example.yaml` and `README.md` contain no short-word icon values
      (final repo-hygiene check)

**Checkpoint**: Feature complete and validated.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories (tests
  first).
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion.
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion; independent of US1
  (different files: config + README).
- **User Story 3 (Phase 5)**: Depends on US1 (it styles the `<img>` US1 emits) and
  Foundational completion.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational. No dependency on US2/US3.
- **User Story 2 (P1)**: Can start after Foundational. Independent of US1 (config + README).
- **User Story 3 (P2)**: Depends on US1's template change (adds/stylizes the icon element).

### Within Each User Story

- Tests (Phase 2) MUST be written and FAIL before implementation (Constitution Gate 2).
- Template rendering before styling (US3 depends on US1).

### Parallel Opportunities

- Phase 2 test tasks T003–T008 can run in parallel (different assertions / different
  files).
- US1 (Phase 3) and US2 (Phase 4) can be implemented in parallel — different files
  (`index.html` vs `config/example.yaml` + `README.md`).
- T010 and T016 touch the same file domain only after US1; US3 CSS work can start once the
  icon element exists.

---

## Parallel Example: User Story 1 + User Story 2

```bash
# Launch the test-writing tasks together (Phase 2):
Task: "T003 tests/unit/test_bookmark_icons.py URL <img> assertion"
Task: "T005 tests/unit/test_bookmark_icons.py short-word no-<img> assertion"

# US1 (template) and US2 (config+README) can run in parallel:
Task: "T010 [US1] Modify app/templates/index.html to render bookmark icon"
Task: "T012 [US2] Clean short-word group icons in config/example.yaml"
Task: "T014 [US2] Update README.md bookmark icon docs"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (confirm clean test run)
2. Complete Phase 2: Foundational (write failing tests — CRITICAL, blocks all stories)
3. Complete Phase 3: User Story 1 (template renders bookmark icon)
4. **STOP and VALIDATE**: Run `uv run pytest tests/unit/test_bookmark_icons.py`; confirm
   the icon-rendering tests pass.
5. Deploy/demo if ready (MVP: bookmarks can show icons).

### Incremental Delivery

1. Setup + Foundational → test foundation ready (tests failing as red).
2. Add User Story 1 → icon renders → Test independently → Deploy/Demo (MVP!).
3. Add User Story 2 → config cleanup + README → Test independently.
4. Add User Story 3 → consistent styling → Test independently.
5. Each story adds value without breaking previous stories.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- Each user story should be independently completable and testable.
- Verify tests fail before implementing (Constitution Gate 2).
- Commit after each task or logical group.
- Stop at any checkpoint to validate the story independently.
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break
  independence.
