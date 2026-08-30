---

description: "Task list for feature 008: Edit Config From Browser"
---

# Tasks: Edit Config From Browser

**Input**: Design documents from `/specs/008-edit-config-browser/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/config-editor.md, quickstart.md

**Tests**: Included. The Constitution (Testability gate IV) and plan.md require tests written
alongside this change with a red-green cycle. Each user-story phase begins with its tests
(pytest, `uv run pytest`).

**Organization**: Tasks are grouped by user story to enable independent implementation and
testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single Flask web app at repo root: `app/`, `tests/`
- Python 3.14, Flask 3.x, Jinja2 templates, PyYAML (`yaml.safe_load`), Bootstrap 5.3
- Editor is a **plain `<textarea>`** — NO editor library, NO bundler, NO build step (Clarification 2026-08-30 → Option A)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Make the single config file the feature operates on reliably readable and
expose the routes/template shell that every user story builds on.

- [x] T001 Add a `GET /config` route in `app/views.py` (returns the config page; renders
  `config.html`) — always available, read-only entry point for User Story 1
- [x] T002 [P] Add `app/templates/config.html` Jinja2 template (Bootstrap layout matching
  `index.html`: extends the same base look; shell with placeholders for the raw config text
  block, edit controls, and messages)
- [x] T003 [P] Add an `editor_enabled()` accessor to `ConfigLoader` in `app/config.py` that
  reads the top-level `editor`/`edit_config` boolean flag from the raw YAML and returns
  `False` when absent, non-boolean, or `false` (default-deny; spec FR-010)

**Checkpoint**: `/config` renders a page; `ConfigLoader` can report whether editing is enabled.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core module that MUST be complete before ANY user story works. `app/editor.py`
owns the bounded read/validate/write contract that every story depends on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create `app/editor.py` implementing the bounded editor module with:
  `read_raw()` (returns current config file text), `validate_content(text)` (returns error
  or None — runs `yaml.safe_load` then `parse_dashboard`, reusing `app/schema.py`), and
  `write_atomic(text)` (write a same-directory temp file, then `os.replace`, confined to
  the resolved `CONFIG_PATH`; never accepts a client-supplied path)
- [x] T005 [P] Add atomic-write implementation + last-known-good backup in `app/editor.py`:
  before `write_atomic` overwrites, copy the current on-disk bytes to a bounded backup at
  `<config_path>.backup.yaml` (single recent copy; FR-006 / data-model)
- [x] T006 [P] Add `POST /config/save` route stub in `app/views.py` that (a) returns `403
  {ok:false,error:"Config editing is disabled."}` when `ConfigLoader.editor_enabled()` is
  `False` (FR-010), and (b) when enabled, delegates to `app/editor.py` (implemented in US2)
- [x] T007 [P] Write unit tests for `app/editor.py` in `tests/unit/test_editor_config.py`:
  round-trip exactness, validation gate (malformed YAML / format violation → no write,
  error), atomic-write behavior, and backup/recover
- [x] T008 [P] Write unit tests for the opt-in flag in `tests/unit/test_config_flag.py`:
  `editor_enabled()` is `False` by default/absent, `True` when the flag is set, and
  read-only behavior of `GET /config` when disabled
- [x] T009 Write integration test file `tests/integration/test_config_editor_flow.py` that
  drives save → reload via the Flask test client against a `tmp_path` config file (shared
  helpers for writing YAML and bumping mtime, mirroring `tests/integration/test_config_reload.py`)

**Checkpoint**: Foundation ready — `app/editor.py` can read/validate/write/backup a config,
routes enforce the disabled-by-default flag, and tests exist (failing/red before US1 impl).

---

## Phase 3: User Story 1 - View the Current Config in the Browser (Priority: P1) 🎯 MVP

**Goal**: Owner opens `/config` and sees the exact current YAML, read-only, with no edit/save
controls when editing is disabled (spec US1, FR-001/FR-010).

**Independent Test**: `uv run pytest tests/unit/test_config_flag.py` passes; opening the page
shows the exact YAML and no save/modify controls.

### Tests for User Story 1

- [x] T010 [P] [US1] Add integration test in `tests/integration/test_config_editor_flow.py`
  that `GET /config` renders the exact raw YAML text and, with the editor flag absent, shows
  no edit/save controls

### Implementation for User Story 1

- [x] T011 [US1] Implement the read/view payload in `app/views.py` `GET /config`: load the
  raw config text via `app/editor.read_raw()` (handle unreadable/missing file → render a
  clear error message, not a broken page; spec US1 scenario 3); expose
  `raw_config` (escaped via `app.security.escape_html` — FR-009), `editing_enabled`,
  `writable`, and `config_path` (display only)
- [x] T012 [US1] Render the read-only view in `app/templates/config.html`: show the current
  YAML (escaped) as a scrollable monospace block; when `editing_enabled` is `False`, show NO
  save/edit controls and a note that editing is disabled (spec US1 scenario 2)
- [x] T013 [US1] Style the config display block (scrollable monospace, focus/theme parity)
  via `app/static/app.css`

**Checkpoint**: US1 complete — owner can view the live config read-only; disabled-by-default
is enforced. Independently testable and deployable (MVP foundation for the whole feature).

---

## Phase 4: User Story 2 - Edit and Save the Config From the Browser (Priority: P1)

**Goal**: Owner edits raw YAML in a `<textarea>` and saves; valid saves write to file
atomically; invalid saves are rejected with a specific message and leave prior config intact
(spec US2, FR-002/003/004, contract tests 1-3, 5).

**Independent Test**: `uv run pytest tests/unit/test_editor_config.py` passes; save a valid
edit → `200` and file updated; submit malformed YAML → `400` with no change.

### Tests for User Story 2

- [x] T014 [P] [US2] Add contract/unit tests in `tests/unit/test_editor_config.py` for the
  validation gate: malformed YAML → rejected with a specific error and previous bytes
  unchanged; valid YAML but format violation (e.g., `services: "not-a-list"`) → rejected,
  nothing written (contract tests 2 & 3 / quickstart scenario 3)
- [x] T015 [P] [US2] Add test in `tests/unit/test_editor_config.py` for the exact byte
  round-trip: `GET /config`-style text → save the same bytes → identical bytes on re-read
  (no reformatting; contract test 5 / quickstart scenario 2)

### Implementation for User Story 2

- [x] T016 [US2] Implement `POST /config/save` in `app/views.py`: parse JSON
  `{content: <raw YAML>}`, call `app/editor.validate_content()`; on failure return `400
  {ok:false,error:<specific message>}` and DO NOT write; on success call
  `app/editor.write_atomic()` and return `200 {ok:true,message:"Saved. The dashboard will
  reflect the change."}` (contract §2)
- [x] T017 [US2] Add the `<textarea id="config-editor">` to `app/templates/config.html`,
  pre-filled with the escaped `raw_config` value, plus a Save button (rendered ONLY when
  `editing_enabled` is `True`)
- [x] T018 [US2] Add client-side submit handling in `app/templates/config.html` (inline
  script or `app/static/app.js`): POST `{content: textarea.value}` to `/config/save`,
  disable the Save button while in flight, and render the response message per status
  (`200` success; `400`/`500` show the server error and keep textarea content intact;
  `403` hides save) — contract §3 "Client feedback"
- [x] T019 [US2] Add error-path handling for an unbounded write failure and unreadable state:
  return `500 {ok:false,error:"Could not write the config file."}` and preserve the existing
  file (contract test 6 / US2 scenario 4 / FR-007)

**Checkpoint**: US2 complete — owner can edit and save; validation before write; invalid
saves never corrupt the good config.

---

## Phase 5: User Story 3 - Change Kick In Without Extra Steps (Priority: P1)

**Goal**: A saved valid edit is reflected by the dashboard on the next request, with no
manual restart (spec US3, FR-005/008, contract test 1).

**Independent Test**: `uv run pytest tests/integration/test_config_editor_flow.py` passes —
save a change via `POST /config/save`, then load `/` and see the new value with no manual
step; a failed/invalid save leaves the dashboard serving the last valid config.

### Tests for User Story 3

- [x] T020 [P] [US3] Add integration test in `tests/integration/test_config_editor_flow.py`
  (end-to-end): enable editing, `POST /config/save` a change, then `GET /` reflects the
  change on the next request via ConfigLoader hot-reload (bump mtime where needed;
  quickstart scenario 4)
- [x] T021 [P] [US3] Add integration test that an invalid save does NOT take effect: after a
  rejected `400`, `GET /` keeps rendering the last valid config (FR-008 / US3 scenario 2)

### Implementation for User Story 3

- [x] T022 [US3] Verify/ensure the save path leaves the dashboard serving valid data even
  while the config is being re-read concurrently (write is atomic; no partial file is ever
  loadable by `ConfigLoader`) — confirms no State-transition regression in
  `app/config.py`/`app/editor.py`

**Checkpoint**: US3 complete — save → reflected with no restart; dashboard stays up on
invalid saves.

---

## Phase 6: User Story 4 - Recover From a Bad Edit (Priority: P2)

**Goal**: A previously valid config can be restored from the browser after a bad edit
(spec US4, FR-006, data-model "Last-Known-Good Backup").

**Independent Test**: `uv run pytest tests/unit/test_editor_config.py -k "backup or recover"`
passes; after a validated overwrite a backup exists, and the revert control restores it
(quickstart scenario 5).

### Tests for User Story 4

- [x] T023 [P] [US4] Add unit tests in `tests/unit/test_editor_config.py` for backup/recover:
  after a validated `write_atomic`, `<config>.backup.yaml` holds the previous valid bytes;
  revert restores them

### Implementation for User Story 4

- [x] T024 [US4] Add a "revert to last-known-good" capability in `app/editor.py` /
  `app/views.py` (`GET`-provided backup value or re-read of `<config>.backup.yaml`) exposed
  only when `editing_enabled` is `True` and a backup exists (spec US4 scenario 1 & 2)
- [x] T025 [US4] Add a Revert button to `app/templates/config.html` (rendered only when
  enabled and a backup exists) with a visual confirmation before overwriting the current
  content (contract §3 "Editing controls")

**Checkpoint**: US4 complete — owner can recover the last good config from the browser.

---

## Phase 7: User Story 5 - Protect the Edit Action (Priority: P2)

**Goal**: Editing is off by default and only exposed when the owner enables the flag; direct
save attempts are blocked when disabled (spec US5, FR-010, contract test 4).

**Independent Test**: `uv run pytest tests/unit/test_config_flag.py` passes — editing disabled
by default (no controls; `POST /config/save` → `403`, nothing written); enabling the flag
makes editing available.

### Tests for User Story 5

- [x] T026 [P] [US5] Add tests in `tests/unit/test_config_flag.py` confirming that with the
  flag absent/`false`, `POST /config/save` returns `403` and writes nothing (contract test 4)

### Implementation for User Story 5

- [x] T027 [US5] Verify end-to-end opt-in enforcement: with `editor_enabled()` `False`, the
  save route returns `403` and `GET /config` shows no edit controls; with the flag `True`,
  saving succeeds per US2 — audit `app/views.py` route guards and flag parsing
- [x] T028 [US5] Confirm the `editor` flag itself is validated (non-boolean value must not
  silently enable editing): guard `editor_enabled()` in `app/config.py` to coerce only
  `isinstance(value, bool) and value is True` to enabled (default-deny; data-model
  "Editor-Enable Flag")

**Checkpoint**: US5 complete — editing is protected and opt-in; default-deny enforced.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and harden the feature.

- [x] T029 Add stale-editor detection (FR-011): capture the config's mtime/size when
  `GET /config` renders and reject/inform the owner on `POST /config/save` if the file
  changed on disk since it was opened (never silently overwrite newer changes)
- [x] T030 [P] Confirm output escaping everywhere config text is rendered back into the page
  (`escape_html` on `raw_config` and any mirrored values; FR-009, Security Requirements) in
  `app/views.py` and `app/templates/config.html`
- [x] T031 [P] Harden save for very large configs: ensure `GET /config` render and save
  stay interactive under the 2s page target (SC-004) via a single pass read/write (no
  unnecessary copies beyond the required backup)
- [x] T032 Run the full suite `uv run pytest` and confirm all feature-008 tests plus the
  existing 86 tests pass with no regressions; run `ruff check .` and `djlint --lint`
- [x] T033 [P] Verify all quickstart.md validation scenarios end-to-end and tick the
  acceptance checklist there

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational completion
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: After Foundational. No dependencies on other stories. Read-only; safest
  first increment.
- **US2 (P1)**: After Foundational. Depends on US1's `GET /config` + flag plumbing
  (T013/T003) but is independently testable on the save route.
- **US3 (P1)**: After Foundational + US2 (save must exist to be reflected). Relies on
  existing `ConfigLoader` hot-reload.
- **US4 (P2)**: After Foundational + US2 (backup is written during save). Independently
  testable on `app/editor.py`.
- **US5 (P2)**: After Foundational. Independently testable (flag gating) — partially
  enforced in earlier phases (T003, T006, T008), finalized here.

### Within Each User Story

- Tests are written FIRST and must FAIL before implementation (red-green; Constitution IV)
- Read/validate core (`app/editor.py`) before routes before UI
- Story complete and passing before moving to the next priority

### Parallel Opportunities

- Phase 1: T002 (template) and T003 (flag accessor) are [P] — independent of T001
- Foundational: T005 & T006 are [P]; T007/T008/T009 test files are [P] against the same
  `app/editor.py` contract
- Within each story, the listed [P] test tasks can be written in parallel
- Stories US1–US5 can largely proceed in parallel after Foundational (shared module is
  stable), personal-team capacity permitting

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (`app/editor.py` + flag gating + tests)
3. Complete Phase 3: User Story 1 (read-only view)
4. **STOP and VALIDATE**: `uv run pytest tests/unit/test_config_flag.py
   tests/unit/test_editor_config.py` — read-only view works, no regressions
5. Though scope is narrow, this establishes the safe foundation; deployable as read-only
   inspection

### Incremental Delivery

1. Setup + Foundational → view/read + disabled-by-default enforced
2. US1 view → inspect live config (read-only)
3. US2 edit/save → primary value; validate before write
4. US3 auto-apply → zero-manual-step edits
5. US4 recover → bad-edit safety net
6. US5 hardening + Polish (FR-011 stale detection, escaping, large-config perf, full suite)

### Parallel Team Strategy

1. Team completes Setup + Foundational together
2. Once Foundation is done: developer(s) pick user stories (US1 → US2 → US3 → US4 → US5)
   since each is independently testable after the shared module is stable

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to the user story for traceability
- Each user story is independently completable and testable
- Tests must fail before implementing (red-green)
- Commit after each task or logical group
- Stop at any checkpoint to validate the story independently
- The editor is a plain `<textarea>` — do NOT introduce any editor library, bundler, or
  build step
- Respect the known latent regression in `app/security.py` (`validate_url` returns
  `parsed.netloc` instead of `True` at line 15) — do NOT touch it for this feature; reuse
  `escape_html` for rendering and `parse_dashboard`/`validate_url` as they are today
