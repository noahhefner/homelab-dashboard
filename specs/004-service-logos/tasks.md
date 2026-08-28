# Tasks: Service Logos

**Input**: Design documents from `/specs/004-service-logos/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The constitution mandates test-first (Principle IV, non-negotiable). Test tasks are therefore included; they lock in the "any valid remote URL renders as a logo" behavior plus the monogram fallback and safety guarantees. Tests are written BEFORE implementation and confirmed to FAIL (RED) first.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `tests/`, plus root-level `config/example.yaml`, `README.md` (see `plan.md` Project Structure)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish a clean baseline before any logo changes, so the test-first work in later phases is verifiable against a known-good state.

- [X] T001 Run the existing backend suite `uv run pytest` and confirm it passes green (baseline before changes)

**Checkpoint**: Baseline is green; the workspace is ready for the logo contract tests.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify the existing remote-URL logo gate (`validate_url` + Jinja `is url` test) behaves as required before user-story test/implementation work. This feature intentionally reuses the existing mechanism (research.md §1); no new infrastructure is added.

**⚠️ CRITICAL**: No user story work can meaningfully begin until the logo URL gate is confirmed (or fixed).

- [X] T002 Confirm `app/security.py::validate_url` accepts any absolute `http`/`https` URL (any netloc) and rejects `javascript:`/`data:`/relative/malformed values, and that `create_app` registers it as the Jinja `is url` test (add a unit test in `tests/unit/test_security.py` if not already covered for these inputs; this confirms the URL gate satisfies spec FR-004/FR-005)

**Checkpoint**: The URL gate is confirmed; user story implementation can now begin.

---

## Phase 3: User Story 1 - Show a Recognizable Logo for Each Service (Priority: P1) 🎯 MVP

**Goal**: Any valid remote image URL set on a service's `icon` renders as that service's logo image; services without a URL logo show a monogram fallback.

**Independent Test**: Configure a service with a valid remote image URL for `icon` and one without; load the homepage and confirm the first renders an `<img>` logo with that URL while the second renders a monogram.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T003 [P] [US1] Add a test asserting a service with an arbitrary valid remote `http(s)` URL `icon` renders an `<img>` logo containing that exact URL, in `tests/unit/test_views_services.py` (spec FR-004)
- [X] T004 [P] [US1] Add a test asserting a service with a non-URL `icon` (e.g., a plain word) renders a monogram (first letter of the name) rather than an `<img>`, in `tests/unit/test_views_services.py` (spec FR-002)
- [X] T005 [P] [US1] Add a test asserting an unsafe/non-`http(s)` `icon` value (e.g., `javascript:...` or a relative path) is NOT emitted as an `<img src>` and is HTML-escaped, in `tests/unit/test_views_services.py` (spec FR-005)

### Implementation for User Story 1

- [X] T006 [US1] Update `config/example.yaml` so service `icon` values use dashboardicons.com logo URLs (jsDelivr SVG pattern, e.g. `https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg`) to demonstrate the recommended source (spec FR-007, research.md §2)
- [X] T007 [US1] Verify `app/templates/index.html` renders any valid URL `icon` as a lazy `<img>` (with `loading="lazy"` and `onerror` monogram fallback) and any non-URL value as a monogram; adjust the template only if the T003–T005 hardening tests reveal a gap (depends on T003, T004, T005)

**Checkpoint**: US1 fully functional — any remote URL renders as a logo, with a reliable monogram fallback.

---

## Phase 4: User Story 2 - Configure a Logo Without Writing Code (Priority: P1)

**Goal**: Assign or change a service's logo by editing only the YAML config; the change appears on reload with no code change or rebuild.

**Independent Test**: Edit a service's `icon` URL (or remove it) in the YAML config, reload the page, and confirm the tile reflects the change (logo or monogram) without restarting.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T008 [US2] Add an integration test in `tests/integration/test_config_reload.py` asserting that changing a service's `icon` to a different remote URL (and back to none) on a mtime-bumped config is reflected on the next page request (spec FR-003)

### Implementation for User Story 2

- [X] T009 [US2] Document how to assign a logo and where to source one (dashboardicons.com, using the jsDelivr URL pattern) in `README.md`, and note that any valid remote image URL works (spec FR-003, FR-007, US2-2; constitution Principle I)

**Checkpoint**: US2 complete — logo version/config changes are reflected on reload and documented.

---

## Phase 5: User Story 3 - Keep the Repository Free of Large Binary Assets (Priority: P2)

**Goal**: Logos require only a lightweight remote reference in config; no large logo binaries are committed, and the repository stays lean.

**Independent Test**: After configuring logos, `git status` shows no logo binary files added, while the (lightweight) config/docs/test changes are tracked.

### Implementation for User Story 3

- [X] T010 [US3] Verify via `git status` / `git check-ignore` that no logo binaries are committed and that `app/static/bootstrap/` and `node_modules/` remain gitignored (spec FR-004, US3; consistent with feature 003); update `.gitignore` only if an unexpected untracked asset appears

**Checkpoint**: US3 complete — only lightweight manifest/docs/tests are tracked; the repository stays free of logo binaries.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation accuracy.

- [X] T011 Run the full backend suite `uv run pytest` and confirm all tests pass in a clean run (including the existing rendering contract in `tests/integration/test_mobile_layout.py`)
- [X] T012 Execute the `specs/004-service-logos/quickstart.md` validation scenarios V1–V6 (any remote URL renders; monogram fallback; broken-logo fallback; reload reflects change; unsafe values never rendered as image source; dashboardicons.com encouraged)
- [X] T013 Confirm documentation (`README.md`) and `config/example.yaml` remain consistent and accurate after the changes, with no stale references (constitution Principle I)

**Checkpoint**: Feature complete and validated; remote logo URLs are supported, documented, and covered by tests.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup; confirms the URL gate all stories rely on
- **User Stories (Phase 3+)**: All depend on the Foundational URL-gate confirmation (T002)
  - US1 (Phase 3) is the MVP
  - US2 (Phase 4) relies on the same `icon`/URL mechanism
  - US3 (Phase 5) is a verification of the repo-state invariant
- **Polish (Final Phase)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependency on US2/US3
- **User Story 2 (P1)**: Depends on the `icon`/URL gateway (Phase 2); independent of US1/US3
- **User Story 3 (P2)**: Independent verification; no dependency on US1/US2

### Within Each User Story

- Tests FIRST and confirmed to FAIL before implementation
- URL rendering/fallback behavior (US1) before config-change verification (US2)
- Config example before documentation (US1/US2)

### Parallel Opportunities

- T001 (setup) can run before all others
- T002 (Foundational) is required before user-story work
- T003, T004, T005 (US1 tests) touch the same file (`tests/unit/test_views_services.py`) narrowly but are independent assertions; can be written in parallel
- US1 (T003–T007), US2 (T008–T009), US3 (T010) are largely independent after Phase 2 and can be staffed in parallel, though US1 is validated first as the MVP

---

## Parallel Example: User Story 1

```bash
# Launch tests first (RED):
Task: "Add test: any valid remote URL icon renders as <img> logo in tests/unit/test_views_services.py"
Task: "Add test: non-URL icon renders monogram in tests/unit/test_views_services.py"
Task: "Add test: unsafe icon value never rendered as <img src> in tests/unit/test_views_services.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (baseline)
2. Complete Phase 2: Foundational (confirm URL gate)
3. Complete Phase 3: User Story 1 (logo rendering + fallback + example config)
4. **STOP and VALIDATE**: Test US1 independently (any remote URL → logo; non-URL → monogram)
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → URL gate confirmed
2. Add User Story 1 → any remote URL renders as a logo, with monogram fallback (MVP)
3. Add User Story 2 → logo changes on reload, documented
4. Add User Story 3 → repo stays lean of logo binaries
5. Add Polish → full test pass, quickstart validated, docs accurate

### Parallel Team Strategy

- Team completes Setup + Foundational together
- Once the URL gate is confirmed, US1 (logo rendering), US2 (config-change + docs), and US3 (gitignore verification) can be worked in parallel; US1 is the confirmed MVP first

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (constitution Principle IV)
- Commit after each task or logical group
- **Current repo reality**: This feature deliberately reuses the existing `icon`-as-remote-URL behavior (feature 001). Expect NO application-code change unless the hardening tests reveal a gap — most deliverables are tests, the example config, and documentation (research.md §5).
- **Security**: Logo URLs are validated (absolute http/https + netloc) and HTML-escaped when rendered, preventing injection; no new secrets or network exposure at runtime. Remote logos load client-side only (unchanged behavior).
