# Tasks: About Info Modal

**Input**: Design documents from `/specs/013-about-info-modal/`

**Prerequisites**: plan.md, spec.md (user stories), research.md, data-model.md, contracts/html-contract.md, quickstart.md

**Tests**: Included. Test-First is NON-NEGOTIABLE (Constitution Principle IV), so each user story phase leads with failing tests (red) followed by implementation (green). The feature spec does not need to request tests for them to be mandatory here.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: == US1 / US2 (maps to spec.md user stories)
- Exact file paths included in every description

---

## Phase 1: Setup

**Purpose**: Establish a clean baseline so red-green verification is trustworthy.

- [X] T001 Run baseline quality gates and the full test suite (`make check` and `uv run pytest` from repo root) to confirm a clean starting state; record the passing test count as the baseline (expected ≥ 193)

**Checkpoint**: Baseline clean — feature work can begin.

---

## Phase 2: Foundational

**Purpose**: Verify the one shared capability the whole feature depends on. No code-level blocking prerequisites exist (tests use the existing app harness and `tests/soup_utils.py`).

**⚠️ CRITICAL**: Confirm this before any user story work.

- [X] T002 Verify `assets/app.js` still imports `"bootstrap/dist/js/bootstrap.bundle.min.js"` (line 2) so the Modal component's `data-*` API ships in every page bundle; do not modify — the feature relies on it (research.md R1)

**Checkpoint**: Foundation verified — user story implementation can begin.

---

## Phase 3: User Story 1 - Replace GitHub Link with an About Button and Modal (Priority: P1) 🎯 MVP

**Goal**: The homepage navbar shows an About icon button (no GitHub icon) that opens an in-page modal without navigating, containing the dashboard title, author's name, project blurb, config-file guidance, and a GitHub link.

**Independent Test**: Load the homepage, click the about icon (URL unchanged, no new tab, no navigation), and confirm the modal shows the required content. Structural test coverage: about button is a `<button>` with `data-bs-toggle="modal"`/`data-bs-target="#about-modal"` and no `a.github-link` remains.

### Tests for User Story 1 (write FIRST — must FAIL before implementation) ⚠️

> **NOTE: Write these tests FIRST, confirm they FAIL for the expected reason (current template still has the `a.github-link` anchor and no modal), then implement.**

- [X] T003 [P] [US1] Contract test in `tests/contract/test_about_modal_html.py`: assert the navbar about control is a `<button>` (no `href`), classes include `about-toggle`, has `data-bs-toggle="modal"` and `data-bs-target="#about-modal"`, `aria-label="About"`, contains `i.bi.bi-info-circle[aria-hidden=true]`; assert no `a.github-link` / `i.bi-github` remains in the homepage navbar; assert the modal exists with `id="about-modal"`, `tabindex="-1"`, `aria-labelledby="about-modal-title"`, `aria-hidden="true"`; assert the GitHub link inside the modal has `target="_blank"` and `rel` containing both `noopener` and `noreferrer` (per `specs/013-about-info-modal/contracts/html-contract.md`)
- [X] T004 [P] [US1] Integration test in `tests/integration/test_about_modal.py` (mirror `_write_config`/`_page_soup` helpers from `tests/integration/test_visibility_toggles.py`): homepage returns 200 and the modal contains the title `#about-modal-title` text, author `Noah Hefner`, the project blurb, and config guidance referencing `config/example.yaml` and `CONFIG_PATH`; the config editor page (`/config`) has no `#about-modal` and no about button; existing navbar controls (`[data-theme-toggle]`, `.config-link`, search `form`) are unchanged on the homepage (spec FR-012)

### Implementation for User Story 1

- [X] T005 [US1] Replace the GitHub anchor (lines 84-90) in `app/templates/index.html` with the About button markup from `specs/013-about-info-modal/contracts/html-contract.md` (`<button type="button" class="btn btn-link nav-link p-1 about-toggle" data-bs-toggle="modal" data-bs-target="#about-modal" aria-label="About">` + `<i class="bi bi-info-circle" aria-hidden="true"></i>`), removing the `bi-github` icon and `github-link` class (spec FR-001, FR-004, FR-008)
- [X] T006 [US1] Add the about modal markup from `specs/013-about-info-modal/contracts/html-contract.md` to `app/templates/index.html` between `</main>` (line 196) and the `{% for js in js_assets %}` loop (line 197): `div.modal.fade#about-modal` with `modal-dialog modal-dialog-centered modal-dialog-scrollable`, header (title + `.btn-close`), body (author, blurb, config guidance with `<code>`), and footer GitHub link with `target="_blank" rel="noopener noreferrer"` (spec FR-002, FR-004, FR-005)
- [X] T007 [P] [US1] Rename the four `.github-link` selector groups (base, `:hover`, `[data-bs-theme="dark"] :hover`, `:focus-visible`) to `.about-toggle` in `assets/app.css` (lines 47, 76, 83, 89); no style changes — the About button inherits the existing icon-button look (research.md R4)

**Checkpoint**: User Story 1 functionally complete — navbar shows the About icon, modal opens with all four content elements plus the GitHub link. Run the US1 tests → green.

---

## Phase 4: User Story 2 - Dismissal, Accessibility, and Responsive Fit (Priority: P2)

**Goal**: The modal closes easily (close button, backdrop click, Esc), is keyboard/screen-reader friendly, fits mobile viewports, and is legible in dark mode.

**Independent Test**: Open the modal and confirm each dismissal method (`.btn-close`, backdrop, Esc), that open/close cycles repeat without error, and that the dialog is centered/scrollable on small viewports and inherits the `data-bs-theme` palette.

### Tests for User Story 2 (write FIRST — must FAIL before this story is complete) ⚠️

> **NOTE: Append to the existing file. Sequential (same file), so not marked [P].**

- [X] T008 [US2] Extend `tests/integration/test_about_modal.py` with dismissal/UX assertions: `.modal-dialog` carries both `modal-dialog-centered` and `modal-dialog-scrollable` classes (spec FR-010); `.modal-header .btn-close` has `data-bs-dismiss="modal"` (spec FR-006); exactly one `#about-modal` element exists in the homepage markup (repeated-open purity, spec FR-011); the about button and modal inherit the existing `data-bs-theme` root attribute already covered by `tests/integration/test_dark_mode.py` (spec FR-009)

### Implementation for User Story 2

- [X] T009 [US2] Verify/adjust the modal markup added in T006 in `app/templates/index.html` so every US2 acceptance criterion is structurally satisfied: `.btn-close` present with `data-bs-dismiss="modal"`, `modal-dialog-centered modal-dialog-scrollable` present, single `#about-modal` instance, backdrop/Esc handled by the shipped Bootstrap Modal component (no custom JS allowed — Doctrine VI); make no change if already compliant (spec FR-006, FR-007, FR-010, FR-011)

**Checkpoint**: User Stories 1 AND 2 both complete and independently testable.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Bundle validation and full-suite verification.

- [X] T010 [P] Rebuild the frontend bundle with `pnpm build` from repo root to validate the `assets/app.css` change compiles through Vite and `app/static/manifest.json` regenerates; note `app/static/` is gitignored so the bundle is a local runtime validation, not a commit
- [X] T011 [P] Run `make check` (ruff lint, ruff format check, ty typecheck, djlint over `app/templates`, prettier check over `assets/`) and fix any formatting drift in `assets/app.css` or `app/templates/index.html` (e.g., `npx prettier --write assets/app.css`, then re-check)
- [X] T012 [P] Run the full test suite (`uv run pytest`) and confirm all tests pass — new contract + integration tests plus the baseline suite (≥ baseline count from T001)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup; verifies the bundle capability all stories rely on
- **User Stories**: US1 (Phase 3) then US2 (Phase 4) — US2 structurally depends on the modal existing (created in US1)
- **Polish (Final Phase)**: Depends on both user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phases 1-2 — no story dependencies
- **US2 (P2)**: Requires the modal markup from US1's T005/T006; otherwise independently testable

### Within Each User Story

- Tests MUST be written and confirmed FAILING before implementation (initially, the current template has no modal and still ships `a.github-link`, so T003/T004/T008 fail for the expected reason)
- Implementation tasks come after their red tests (T005/T006 after T003/T004; T009 after T008)

### Parallel Opportunities

- T003 + T004 (US1 tests) run in parallel — different files
- T007 runs in parallel with T005/T006 — different file (`assets/app.css` vs `app/templates/index.html`)
- T010, T011, T012 (Polish) run in parallel — independent validation commands
- All tasks touch distinct files except the intra-story sequential chains (T003→T005/T006, T004→T005/T006, T008→T009)

---

## Parallel Example: User Story 1

```bash
# Launch both test files together (red first):
Task: "Contract test in tests/contract/test_about_modal_html.py"
Task: "Integration test in tests/integration/test_about_modal.py"

# Then template + CSS in parallel:
Task: "Replace GitHub anchor with About button in app/templates/index.html"
Task: "Rename .github-link selectors to .about-toggle in assets/app.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1-2 (baseline + bundle verification) → quick, no code
2. Phase 3: User Story 1 → tests-red, implement, tests-green
3. **STOP and VALIDATE**: homepage renders, about button opens modal, content correct, GitHub link moved into modal, `make check` + pytest green
4. Deploy/demo if ready — deliver the requested behavior independently

### Incremental Delivery

1. US1 → independent value (the requested change), fully testable
2. US2 → dismissal/UX hardening layered on the same modal
3. Polish → bundle + full-suite validation

---

## Notes

- The built bundle lives in `app/static/`, which is gitignored; only `assets/app.css`, `assets/app.js` (unchanged), and `app/templates/index.html` are committed source for this feature
- No Python/backend changes: no model, schema, config-parsing, or route work (per plan.md structure decision)
- Modal behavior (backdrop, Esc, focus) comes from the already-bundled Bootstrap Modal JS — do not add custom JS/`<script>` in the template
- Content is static template text (data-model.md) — no runtime/config-derived values
- Commit after each task or logical group; stop at any checkpoint to validate independently