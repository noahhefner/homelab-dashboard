---

description: "Task list for fixing all pyrefly errors"
---

# Tasks: Fix Pyrefly Errors

**Input**: Design documents from `/specs/014-fix-pyrefly-errors/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md)

**Tests**: No new test tasks are generated. The user explicitly requested only changes that correct pyrefly errors and no new unit tests. Existing tests are used as the behavior contract.

**Organization**: Tasks are grouped by user story so each story can be validated independently. All implementation changes serve User Story 1; User Stories 2 and 3 are verification slices that prove behavior preservation and trustworthy type coverage.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Application: `app/`
- Tests: `tests/`
- Feature docs: `specs/014-fix-pyrefly-errors/`

---

## Phase 1: Setup

**Purpose**: Confirm the baseline and toolchain before editing

- [x] T001 Run `uv run pyrefly check app tests` and `uv run pytest` from the repository root and record the baseline (23 errors, 205 passing tests). See `specs/014-fix-pyrefly-errors/research.md` for the expected diagnostic groups.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared test-helper change required by three test-file fixes

**⚠️ CRITICAL**: Complete this before the test-edit tasks that use the helper

- [x] T002 Add `attr_str(tag: Tag, name: str) -> str | None` to `tests/soup_utils.py`, importing `Tag` from `bs4` and returning the attribute only when `isinstance(value, str)`; update the module docstring only if needed. This is test tooling, not a new test.

**Checkpoint**: The shared helper is available; User Story 1 edits can proceed

---

## Phase 3: User Story 1 - Clean Type-Check Gate Across the Whole Project (Priority: P1) 🎯 MVP

**Goal**: Resolve all 23 baseline pyrefly errors in application and test code so the type-check gate reports zero errors.

**Independent Test**: `uv run pyrefly check app tests` reports `0 errors`, and `make typecheck` exits successfully.

- [x] T003 [US1] Fix the Jinja test contract in `app/security.py`: rename the `validate_url` parameter from `url` to `value`, change the signature to `def validate_url(value: object) -> bool:`, update internal references, and return `bool(parsed.netloc)` instead of the raw netloc string. Do not change accept/reject logic.
- [x] T004 [P] [US1] Annotate `ConfigLoader.get()` in `app/config.py` as `-> tuple[DashboardConfig | None, str | None]` and add `from app.model import DashboardConfig`. Do not change the returned tuple or reload behavior.
- [x] T005 [P] [US1] Narrow config results in `tests/unit/test_config_loader.py`: add `assert config is not None` before `config.tile_groups` at line 43 and before `reloaded.tile_groups` at line 64; replace the inline `loader.get()[0]` accesses at lines 71 and 82 with a local `config, _ = loader.get()` followed by `assert config is not None`.
- [x] T006 [P] [US1] In `tests/contract/test_about_modal_html.py`, add `assert modal is not None` after `modal = soup.select_one("#about-modal")` in `test_gh_link_inside_modal_opens_in_new_tab_safely`.
- [x] T007 [P] [US1] In `tests/integration/test_homepage_tiles.py`, add `assert header is not None` after both `header = soup.select_one("h3.group-title")` assignments in the tile-group icon tests.
- [x] T008 [P] [US1] In `tests/integration/test_mobile_layout.py`, import `attr_str`, add `assert tiles is not None` / `assert bookmarks is not None` before class checks in `test_mobile_stack_uses_full_width_columns` and `test_single_consistent_lg_breakpoint`, and use `attr_str(link, "href")` / `attr_str(script, "src")` in the remote-asset filtering lists. Keep the same filter conditions.
- [x] T009 [P] [US1] In `tests/integration/test_navbar.py`, import `attr_str`, replace the two inline `.navbar-brand` assertions with a `brand` variable plus `assert brand is not None`, and in `test_navbar_uses_custom_search_engine_in_action` read the form action through `attr_str(form, "action")` and assert it is not `None` before `.startswith(...)`.
- [x] T010 [P] [US1] In `tests/integration/test_visibility_toggles.py`, wrap the three class-attribute checks in `(tiles.get("class") or [])` and add `assert tiles is not None` before the check in `test_tiles_side_by_side_with_bookmarks_by_default`.
- [x] T011 [P] [US1] In `tests/unit/test_bookmark_icons.py`, import `attr_str` and replace `(img.get("src") or "").startswith("javascript:")` with `(attr_str(img, "src") or "").startswith("javascript:")` in `test_unsafe_icon_value_not_rendered_as_src`.
- [x] T012 [P] [US1] In `tests/unit/test_views_tiles.py`, add `assert plex is not None` after `plex = soup.select_one("a.app-tile")`, then read the image through a local `image = plex.select_one("img")`, assert `image is not None`, and compare `image.get("src")` to the existing expected URL.
- [x] T013 [US1] Run `uv run pyrefly check app tests` and `make typecheck`; confirm `0 errors` and that the warning count remains 21 (only `yaml` untyped-import notices). Do not add `types-PyYAML` or suppression comments.

**Checkpoint**: The full type-check gate is green; User Story 1 is independently complete

---

## Phase 4: User Story 2 - Preserve Runtime and Test Behavior (Priority: P2)

**Goal**: Prove the type-only changes did not alter dashboard, config, URL-validation, or rendering behavior.

**Independent Test**: The full existing pytest suite passes with no tests added, removed, skipped, or weakened.

- [x] T014 [US2] Run `uv run pytest` (or `make test`) against `tests/` and confirm all 205 existing tests pass; confirm the collected test count and test files match the baseline from T001.
- [x] T015 [P] [US2] Review `git diff -- app/security.py app/config.py` and confirm the only production changes are annotations, the parameter rename required by Jinja's typed contract, and the `bool(...)` return representation; no accept/reject, loading, reloading, or tuple-shape behavior changed.

**Checkpoint**: User Story 2 is verified; runtime behavior is unchanged

---

## Phase 5: User Story 3 - Keep Type Coverage and Diagnostics Trustworthy (Priority: P3)

**Goal**: Prove the fixes did not weaken type checking and that future regressions remain detectable.

**Independent Test**: No exclusions or suppressions were added, no new dependency was introduced, and a deliberately introduced type error is still reported.

- [x] T016 [US3] Verify `pyproject.toml` `[tool.pyrefly]` still includes the same paths and that no file-wide or project-wide ignore/suppression directives were added; inspect changes with `git diff -- pyproject.toml` and search the changed Python files for new ignore comments.
- [x] T017 [P] [US3] Confirm no runtime or development dependency was added for this change by reviewing `git diff -- pyproject.toml`; `types-PyYAML` must not be added, and the 21 warning-level diagnostics must remain unchanged.
- [x] T018 [US3] Sanity-check coverage per `specs/014-fix-pyrefly-errors/quickstart.md` section 6: temporarily introduce a deliberate type error into a previously failing expression, run `uv run pyrefly check app tests`, confirm the error is reported, then revert the temporary edit completely.

**Checkpoint**: User Story 3 is verified; type coverage is intact

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final project-wide validation

- [x] T019 Run `uv run ruff check app tests` and `uv run ruff format --check app tests`; fix only formatting/lint issues caused by the type edits, with no unrelated refactoring.
- [x] T020 Run `make check` from `Makefile` and confirm linting, Python formatting, pyrefly, djlint, and Prettier all pass.
- [x] T021 Run the full validation sequence in `specs/014-fix-pyrefly-errors/quickstart.md` and review `git status --short` / `git diff --stat` to confirm only the planned files changed, no new test files exist, and no suppressions or exclusions were introduced.
- [x] T022 Confirm `AGENTS.md` already points to `specs/014-fix-pyrefly-errors/plan.md`; do not make unrelated agent-context changes.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — starts immediately.
- **Foundational (Phase 2)**: Depends on T001; blocks all User Story 1 test-edit tasks that use `attr_str`.
- **User Story 1 (Phase 3)**: Depends on Phase 2. T003–T012 are file-local edits; T013 depends on all of them.
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion (T013).
- **User Story 3 (Phase 5)**: Depends on User Story 1 completion (T013); can run in parallel with User Story 2.
- **Polish (Phase 6)**: Depends on User Stories 1–3.

### User Story Dependencies

- **User Story 1 (P1)**: Requires T002 only; no dependency on US2 or US3.
- **User Story 2 (P2)**: Requires US1 fixes; verifies behavior preservation.
- **User Story 3 (P3)**: Requires US1 fixes; verifies coverage preservation and can run alongside US2.

### Within User Story 1

- T003 fixes the sole application diagnostic.
- T004 establishes the `ConfigLoader.get()` contract; T005 narrows its call sites.
- T006–T012 are independent per-file test edits.
- T013 validates the combined result and must run last in the phase.

### Parallel Opportunities

- T003–T012 target different files and can mostly run in parallel after T002. T005 conceptually follows T004, but the edits are in separate files and can be prepared concurrently.
- T014 and T015 can run in parallel within US2.
- T016, T017, and T018 can run in parallel within US3.
- US2 and US3 can run in parallel after T013.
- T019 and T020 are sequential because `make check` includes lint/format checks.

---

## Parallel Example: User Story 1

```text
T003  app/security.py
T004  app/config.py
T005  tests/unit/test_config_loader.py
T006  tests/contract/test_about_modal_html.py
T007  tests/integration/test_homepage_tiles.py
T008  tests/integration/test_mobile_layout.py
T009  tests/integration/test_navbar.py
T010  tests/integration/test_visibility_toggles.py
T011  tests/unit/test_bookmark_icons.py
T012  tests/unit/test_views_tiles.py
```

All target different files and may be edited concurrently. Run T013 only after they are complete.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: confirm the baseline.
2. Complete Phase 2: add the shared test helper.
3. Complete Phase 3: apply all type fixes and run T013.
4. **STOP and VALIDATE**: `uv run pyrefly check app tests` reports 0 errors and `make typecheck` passes.
5. This is a complete, shippable type-only change with no new tests.

### Incremental Delivery

1. Apply the production contract fixes (T003, T004) and validate the application error is gone.
2. Apply the test narrowing edits (T005–T012) and validate the test errors are gone.
3. Run behavior and coverage verification (US2, US3).
4. Run the full project gate (Polish) and deliver.

---

## Notes

- No new tests are generated or requested; T014 verifies the existing 205-test suite instead.
- `[P]` marks file-level parallelism, not permission to skip validation.
- Do not add `types-PyYAML`, ignore comments, exclusions, or new dependencies.
- Keep changes limited to correcting the 23 pyrefly errors; avoid opportunistic refactors.
- Commit after each logical group (production contract fixes, test narrowing, final validation).
