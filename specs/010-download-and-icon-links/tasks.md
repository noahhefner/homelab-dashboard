---

description: "Task list for Download Config & Icon Links feature"
---

# Tasks: Download Config & Icon Links

**Input**: Design documents from `/specs/010-download-and-icon-links/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included. The project's Constitution (Principle IV, Testability) mandates a test-first (red-green-refactor) workflow, and `plan.md`'s Testing section requires tests for the download route and page rendering.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `tests/` at repository root (existing Flask layout).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the baseline tooling is ready; no new dependencies are introduced by this feature.

- [x] T001 Verify `uv sync` installs the Python deps and `uv run pytest` currently passes from a clean tree (baseline gate before writing failing tests)

**Checkpoint**: Tooling confirmed. No new dependency or build step is required, so no further setup is needed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared read/filesystem logic that both user stories' page rendering and US1's download depend on. This is minimal because the feature reuses the existing `read_raw` helper.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T002 Add a server-side helper `download_config(loader)` (returns `(bytes, filename)` or raises `ConfigEditorError`) in `app/editor.py` that reads the exact on-disk config bytes via the existing `read_raw` and derives the download filename as `os.path.basename(path)` (research D1/D2, FR-003)

**Checkpoint**: Foundation ready — a single reusable read+filename helper exists.

---

## Phase 3: User Story 1 - Download Config YAML From the Editor Page (Priority: P1) 🎯 MVP

**Goal**: Let the owner download the current config YAML from the editor page in both editing and read-only modes.

**Independent Test**: `GET /config/download` returns the exact on-disk bytes with `Content-Disposition: attachment; filename="<basename>"` in both editing and read-only modes, and returns a clear error (never an empty attachment) when the file is unreadable.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 [P] [US1] Integration test for exact-bytes + filename download + read-only mode in `tests/integration/test_config_download.py` (red before T005)
- [x] T004 [P] [US1] Integration test for unreadable-config download error (no empty/partial body) in `tests/integration/test_config_download.py` (red before T005)

### Implementation for User Story 1

- [x] T005 [US1] Add `GET /config/download` route in `app/views.py` that uses `download_config(loader)` and returns a Flask `Response` with `Content-Disposition: attachment; filename="..."` and a YAML mimetype; on `ConfigEditorError` return a clear error response (FR-001/002/003/004/005; per contracts/config-download.md)
- [x] T006 [US1] Add a "Download config" button (Bootstrap button + `bi-download` icon) linking to `url_for('dashboard.download_config')` in the top toolbar of `app/templates/config.html`, rendered in both editing and read-only modes (FR-001/004)

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Quick Links to Iconography Websites (Priority: P2)

**Goal**: Show links to iconography websites on the editor page to support finding icons while editing.

**Independent Test**: `GET /config` renders the "Icon sources" section with the two links (dashboardicons.com, homarr-labs/dashboard-icons) in both editing and read-only modes, each with `target="_blank" rel="noopener noreferrer"`.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T007 [P] [US2] Integration test for rendered icon-source links (both, both modes) in `tests/integration/test_config_download.py` (red before T008)

### Implementation for User Story 2

- [x] T008 [US2] Add the "Icon sources" section with the two static links (`https://dashboardicons.com`, `https://github.com/homarr-labs/dashboard-icons`) each `target="_blank" rel="noopener noreferrer"` in the top toolbar of `app/templates/config.html`, visible in both editing and read-only modes (FR-006/007/008; per contracts/config-download.md)

**Checkpoint**: User Stories 1 AND 2 both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Verify the full feature end-to-end and confirm no regressions or Security-Requirements gaps.

- [x] T009 [P] Add/confirm unit test for the `download_config` filename derivation (`os.path.basename`) and read-error path in `tests/unit/test_editor_config.py` (FR-003/005)
- [x] T010 Run `uv run pytest` and the `quickstart.md` validation scenarios (V1–V5) to confirm all pass in a clean run
- [x] T011 Run lint/format (`ruff`, `djlint` for `app/templates/config.html`, `ty`) and confirm clean
- [x] T012 Confirm Security Requirements: the download reads only the fixed resolved config path (no client path), filename is derived server-side, and icon links are static trusted `https` URLs opened with `noopener noreferrer`; no new write path/secrets/exposure.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — baseline only.
- **Foundational (Phase 2)**: Depends on Setup. `T002` (download helper) blocks US1's route implementation.
- **User Stories (Phase 3+)**: US1 depends on `T002`; US2 depends only on the page rendering (no dependency on US1's route, but shares the same template file `config.html`, so the two stories should be sequenced to avoid same-file conflicts).
- **Polish (Final Phase)**: Depends on both user stories.

### User Story Dependencies

- **User Story 1 (P1)**: Depends on `T002`; independently testable once its route + template additions are in.
- **User Story 2 (P2)**: Independent of US1's route; both add to `app/templates/config.html`, so they should not be edited in parallel to avoid conflicts.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.
- Test tasks → implementation tasks.

### Parallel Opportunities

- `T003` / `T004` (US1 tests) can run in parallel (same new file, different scenarios — write together).
- `T002` (foundational) can run in parallel with nothing else this early; it must finish before US1 implementation.
- US1 and US2 share `app/templates/config.html` — do **not** run their implementation tasks in parallel. Sequence US1 then US2, or combine the template edits.
- `T009` (unit) and `T010`–`T012` run after both stories.

---

## Parallel Example: User Story 1

```bash
# Launch the US1 integration tests together (write both scenarios in one file, red first):
Task: "Integration test for download bytes/filename/read-only in tests/integration/test_config_download.py"
Task: "Integration test for unreadable-config error in tests/integration/test_config_download.py"
```
Note: US1 and US2 modify `app/templates/config.html`, so keep their implementation sequential (US1 toolbar button first, then US2 icon links in the same toolbar).

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (`T002` download helper)
3. Complete Phase 3: User Story 1 (download button + route)
4. **STOP and VALIDATE**: Test User Story 1 independently via `pytest tests/integration/test_config_download.py`
5. Deploy/demo if ready.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. Add User Story 1 (download) → test independently → demo (MVP).
3. Add User Story 2 (icon links) → test independently → demo.

### Parallel Team Strategy

Single-owner/small-team project. The two stories share one template file, so the team should sequence US1 → US2 rather than parallelizing the shared `config.html` edits.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to the specific user story for traceability.
- Each user story is independently completable and testable.
- Verify failing tests before implementing (red → green).
- Commit after each task or logical group.
- Stop at any checkpoint to validate the story independently.
- Avoid: vague tasks, same-file conflicts (note the shared `app/templates/config.html` for US1/US2), cross-story dependencies that break independence.
