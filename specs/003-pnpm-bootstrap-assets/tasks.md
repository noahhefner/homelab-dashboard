# Tasks: pnpm Bootstrap Assets

**Input**: Design documents from `/specs/003-pnpm-bootstrap-assets/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The constitution mandates test-first (Principle IV, non-negotiable). This feature is developer/build tooling; test tasks therefore cover (a) verifying existing rendering tests still pass (the "styled page" contract) and (b) a provisioning-correctness check that the expected Bootstrap files exist after running the provisioning command.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `tests/`, plus new root-level `package.json` / `pnpm-lock.yaml` / `scripts/` at repository root (see `plan.md` Project Structure)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the pnpm-managed dependency tracking for Bootstrap and lay the groundwork used by every user story.

- [X] T001 Create `package.json` at repository root declaring `"private": true`, a project `name`/`description` mirroring the app, `"type": "commonjs"` (default), and the pinned dependency `"bootstrap": "5.3.3"`
- [X] T002 [P] Add npm `scripts` to `package.json`: `"provision"` (runs `scripts/provision-bootstrap.sh`) and `"setup"` (`pnpm install && pnpm provision`)
- [X] T003 [P] Add `node_modules/` and `app/static/bootstrap/` to `.gitignore` so pnpm store artifacts and the materialized Bootstrap assets stay out of source control (spec FR-003, US3)
- [X] T004 Run `pnpm install` to generate and commit the `pnpm-lock.yaml` lockfile pinning the exact `bootstrap` version

**Checkpoint**: `package.json` + `pnpm-lock.yaml` exist and are tracked; `node_modules/` and `app/static/bootstrap/` are gitignored.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement the provisioning mechanism (the copy step) so user stories can actually fetch/produce Bootstrap assets, and wire it into the container build.

**⚠️ CRITICAL**: No user story work can meaningfully begin until provisioning actually produces assets.

- [X] T005 Create `scripts/provision-bootstrap.sh` that copies `node_modules/bootstrap/dist/css/bootstrap.min.css` → `app/static/bootstrap/css/bootstrap.min.css` and `node_modules/bootstrap/dist/js/bootstrap.bundle.min.js` → `app/static/bootstrap/js/bootstrap.bundle.min.js`, creating the destination directories as needed
- [X] T006 [P] Make `scripts/provision-bootstrap.sh` fail safely: exit non-zero with an actionable message if `node_modules/bootstrap/dist` is missing, and (optionally) write to a temp dir then move into place so a failure never leaves partially-updated assets (spec FR-005)
- [X] T007 Update `Dockerfile` to a two-stage build: a Node stage (`node:22-slim`) uses `corepack enable`, `pnpm install --frozen-lockfile`, and the provisioning script to produce the Bootstrap assets; the existing Python stage copies only those produced assets into `app/static/bootstrap/` (spec FR-007, SC-004)

**Checkpoint**: Provisioning works locally and inside the container build; the deployed image contains styled Bootstrap assets with no manual step.

---

## Phase 3: User Story 1 - Provision on a fresh checkout (Priority: P1) 🎯 MVP

**Goal**: A developer on a fresh clone runs the provisioning command and gets a correctly-styled page with default UIkit-free, Bootstrap assets present.

**Independent Test**: From a clean checkout (no `app/static/bootstrap/` files), run `pnpm setup`; confirm both Bootstrap files appear under `app/static/bootstrap/` and the homepage renders styled exactly as before.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T008 [P] [US1] Add a provisioning-correctness test `tests/integration/test_asset_provisioning.py` that runs the provisioning command and asserts `app/static/bootstrap/css/bootstrap.min.css` and `app/static/bootstrap/js/bootstrap.bundle.min.js` exist (spec FR-002, SC-001)
- [X] T009 [P] [US1] Confirm the existing rendering contract still holds: `tests/integration/test_mobile_layout.py` asserts the homepage references `/static/bootstrap/...` — keep passing as validation that provisioning yields a styled page

### Implementation for User Story 1

- [X] T010 [US1] Verify the full fresh-checkout flow locally: from a clean worktree, run `pnpm setup` and confirm the project directory layout (`node_modules/`, `app/static/bootstrap/`) is produced correctly (depends on T005, T001–T004)

**Checkpoint**: US1 fully functional — one command provisions assets and the page is styled.

---

## Phase 4: User Story 2 - Track and update the Bootstrap version (Priority: P1)

**Goal**: The Bootstrap version is readably recorded in `package.json` and can be bumped through a simple, repeatable action that refreshes the assets.

**Independent Test**: Read the pinned version in `package.json`, bump it, re-run provisioning, and confirm `app/static/bootstrap/` now reflects the newer version and the page still renders.

### Tests for User Story 2 ⚠️

- [X] T011 [P] [US2] Add a check that `package.json` declares a pinned (exact, non-range) `bootstrap` version, in `tests/integration/test_asset_provisioning.py` (spec FR-001, SC-002)
- [X] T012 [P] [US2] Add a check that re-running provisioning is idempotent and reconciles version drift (e.g., the produced files match the declared version), in `tests/integration/test_asset_provisioning.py` (spec FR-004)

### Implementation for User Story 2

- [X] T013 [US2] Document and verify the update flow in `README.md` (or `scripts/README.md`): "to update Bootstrap, run `pnpm add bootstrap@X.Y.Z` then `pnpm provision`" so the version stays visible and updates are repeatable (spec US2-2, constitution Principle I)

**Checkpoint**: US2 complete — version is declarative and updateable; provisioning reflects the recorded version.

---

## Phase 5: User Story 3 - Keep the repository clean (Priority: P2)

**Goal**: Downloaded Bootstrap assets and node_modules stay out of version control; the package registry remains the source of truth.

**Independent Test**: After provisioning, `git status` shows no tracked/untracked files under `app/static/bootstrap/` (nor `node_modules/`), while `package.json` and `pnpm-lock.yaml` are tracked.

### Tests for User Story 3 ⚠️

- [X] T014 [P] [US3] Add a test (or documented manual check) in `tests/integration/test_asset_provisioning.py` confirming that after provisioning, nobody can `git add app/static/bootstrap/` as part of the commit set — verified via `.gitignore` pattern coverage (spec FR-003, SC-003)

### Implementation for User Story 3

- [X] T015 [US3] Verify with `git status` (and `git check-ignore app/static/bootstrap/css/bootstrap.min.css`) that the provisioned assets are ignored by the `.gitignore` entries added in T003, and confirm `package.json` + `pnpm-lock.yaml` remain tracked (spec FR-003, US3)

**Checkpoint**: US3 complete — repository stays clean of downloaded assets; only the manifest/lockfile are version-controlled.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation.

- [X] T016 Run the full backend suite `uv run pytest` and confirm all tests pass in a clean run (including the existing `/static/bootstrap/` rendering contract)
- [X] T017 Execute the `specs/003-pnpm-bootstrap-assets/quickstart.md` validation scenarios V1–V6 (fresh checkout, asset exclusion, version visible/updatable, idempotent re-provision, container build styled, tests pass)
- [X] T018 Update `README.md` prerequisites/quickstart to document that `node` + `pnpm` are required to provision Bootstrap assets (constitution Principle I — keep developer docs accurate)

**Checkpoint**: Feature complete and validated; provisioning works across developer and container flows, assets are not committed, and docs are accurate.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup (package.json + lockfile) — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational (provisioning works)
  - US1 (Phase 3) is the MVP
  - US2 (Phase 4) builds on the provisioning mechanism
  - US3 (Phase 5) builds on the `.gitignore` entries from Setup
- **Polish (Final Phase)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependency on US2/US3
- **User Story 2 (P1)**: Depends on the provisioning mechanism (Phase 2)
- **User Story 3 (P2)**: Depends on Setup `.gitignore` (T003); no dependency on US1/US2

### Within Each User Story

- Tests FIRST and confirmed to FAIL before implementation
- Provisioning script before the fresh-checkout flow (US1)
- Version declaration before the update verification (US2)

### Parallel Opportunities

- T001, T002, T003 (Phase 1) touch different files/concerns and can run in parallel; only T004 (lockfile) must follow T001
- T005, T006, T007 (Phase 2) can run in parallel (script, script safety, Dockerfile)
- [P]-marked test tasks can run in parallel
- US1/US2/US3 are largely independent after Phase 2 and can be staffed in parallel, though US1 should be validated first as the MVP

---

## Parallel Example: User Story 1

```bash
# Launch tests first (RED):
Task: "Run tests/integration/test_asset_provisioning.py provisioning-correctness check"
Task: "Run tests/integration/test_mobile_layout.py rendering-contract check"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (package.json, lockfile, gitignore)
2. Complete Phase 2: Foundational (provisioning script + Docker two-stage build)
3. Complete Phase 3: User Story 1 (fresh-checkout provisioning)
4. **STOP and VALIDATE**: Test US1 independently (one command → styled page)
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → provisioning works locally and in the container
2. Add User Story 1 → fresh checkout provisions cleanly (MVP)
3. Add User Story 2 → version declarative + updateable
4. Add User Story 3 → repo stays clean of assets
5. Add Polish → full test pass, docs accurate, quickstart validated

### Parallel Team Strategy

- Team completes Setup + Foundational together
- Once Foundational is done, US1 (fresh checkout), US2 (version update), and US3 (gitignore verification) can be worked in parallel; US1 is the confirmed MVP first

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (constitution Principle IV)
- Commit after each task or logical group
- **Current repo reality**: `app/static/bootstrap/` is currently **untracked** (feature 002 changes are uncommitted). The `.gitignore` entries ensure these assets never enter version control going forward; if feature 002 is later committed, the assets remain excluded.
- **Security**: pnpm installs only the pinned `bootstrap` package; no secrets handled; provisioning occurs at dev/build time, not runtime. Bootstrap files are trusted third-party assets served statically (unchanged behavior).
