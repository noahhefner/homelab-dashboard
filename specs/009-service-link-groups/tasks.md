# Tasks: Tile Link Groups (Services Rebranded as "Tiles")

**Input**: Design documents from `/specs/009-service-link-groups/`

**Prerequisites**: spec.md (clarified 2026-08-31), plan.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: The project constitution mandates **test-first** for every change (Principle IV — non-negotiable). Therefore test tasks ARE required and included in every user-story phase. Follow red-green-refactor: write the failing test, confirm it fails for the expected reason, then make it pass.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US7)
- Include exact file paths in descriptions

## Key Design Decisions (from clarified spec)

- **Breaking rename**: config keys `services`→`tiles` and `service_groups`→`tile_groups`; Python `Service`→`Tile`, `ServiceGroup`→`TileGroup`; fields `services`→`tiles`; CSS `.service-*`→`.tile-*`. The legacy `services`/`service_groups` keys are NOT supported (Clarification Q1 → A).
- **Config syntax** (mirrors `bookmark_groups`): flat `tiles:` list, and/or grouped `tile_groups:` each with nested `tiles:`.
- **Tile groups always visible**: plain `<h3>` header + tile grid; NO collapse/expand, NO saved state (FR-010).
- **"Bookmarks" header**: hardcoded `<h3>Bookmarks</h3>` above the accordion when `bookmark_groups` is non-empty (FR-011).
- **Positioning**: tiles may link to internal homelab services OR external services (webmail, cloud portals) (FR-013, US7).

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Align the stale planning artifacts with the clarified spec (breaking rename + external positioning) so downstream tasks are immediately executable and consistent.

- [X] T001 Update `specs/009-service-link-groups/data-model.md` to the clarified design: rename `services`→`tiles` and `service_groups`→`tile_groups` (config keys), `Service`→`Tile`, `ServiceGroup`→`TileGroup`; document `tile_groups[].tiles` nested list; note the breaking change with no legacy-key support; add that a Tile may target internal or external `http(s)` URLs.
- [X] T002 Update `specs/009-service-link-groups/contracts/config-contract.md`: rename top-level keys to `tiles`/`tile_groups`; document `tile_groups[].tiles` entries; remove the old `services`/`service_groups` backward-compat coexistence section; state legacy keys are unsupported.
- [X] T003 Update `specs/009-service-link-groups/contracts/ui-contract.md`: rename tile-group rendering to `tile_groups`; CSS classes to `tile-*`; add the hardcoded "Bookmarks" heading; note `aria-label="Tiles"`.
- [X] T004 Update `specs/009-service-link-groups/quickstart.md`: all validation scenarios use `tiles`/`tile_groups`; V1 becomes "flat `tiles` renders"; add a scenario confirming the legacy `services` key is NOT recognized; note the "Tiles" rebrand and external-service positioning.
- [X] T005 Update `specs/009-service-link-groups/research.md` decisions (§2, §7, §8) to reflect the breaking full-repo rebrand (config key renamed, legacy not supported) and the external-services positioning.
- [X] T006 Update `specs/009-service-link-groups/plan.md` Summary, Technical Context, Constraints, Constitution Check, and Project Structure to the clarified breaking-rename design (remove backward-compat language; reflect `tiles`/`tile_groups`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Rename the entire core "tiles" vocabulary (config key, model/schema, CSS classes, template class names, example config, and their tests) so every user story builds on a consistent `tiles`/`tile_groups` base. **⚠️ No user story can begin until this phase is complete.**

- [X] T007 [P] Rename the `Service` dataclass to `Tile` and its container field `services`→`tiles` in `app/model.py`, updating the `DashboardConfig` annotation accordingly.
- [X] T008 [P] Update `app/schema.py`: rename `_parse_service`→`_parse_tile`, `Service`→`Tile`, the root key `services`→`tiles`, and the `DashboardConfig(...)` call (`services=`→`tiles=`); add a `_parse_tile_group` mirroring `_parse_group` that reads a nested `tiles` list; add `tile_groups` parsing.
- [X] T009 [P] Update `app/views.py` `home()` to pass `tiles=config.tiles` and `tile_groups=config.tile_groups` to the template.
- [X] T010 [P] Update `app/templates/index.html`: rename the classes `service-tile`→`tile`, `service-icon`→`tile-icon`, `service-monogram`→`tile-monogram`, `service-name`→`tile-name`; set the section `aria-label="Tiles"`; iterate `tiles` instead of `services`.
- [X] T011 [P] Update `app/static/app.css`: rename `.service-icon`, `.service-icon img`, `.service-monogram`, `.service-name`, `.service-tile` → their `.tile-*` equivalents (including the mobile `@media` refinements); keep the generic `.app-tile`-based layout unchanged.
- [X] T012 [P] Update `config/example.yaml`: rename `services:`→`tiles:`; update the header comment to "tiles"; in the comment state tiles may link to homelab or external services (supports US7/FR-013).
- [X] T013 [P] Update `tests/unit/test_schema.py`: s/`services`→`tiles`/ and `Service`→`Tile` in test inputs and assertions.
- [X] T014 [P] Update `tests/unit/test_config_loader.py`: s/`services`→`tiles`/ and `config.services`→`config.tiles`/ in config dicts and assertions.
- [X] T015 [P] Update `tests/unit/test_config_flag.py`, `tests/unit/test_editor_config.py`: s/`services:`→`tiles:`/ in raw YAML fixtures and assertions.
- [X] T016 [P] Update `tests/integration/test_config_editor_flow.py` and `tests/integration/test_config_reload.py`: s/`services`→`tiles`/ and `service-monogram`→`tile-monogram`/ in fixtures and assertions.
- [X] T017 [P] Update `tests/unit/test_views_services.py` → rename file to `tests/unit/test_views_tiles.py`; s/`services`→`tiles`/, `service-monogram`→`tile-monogram`/, `service-tile`→`tile`/.
- [X] T018 [P] Update `tests/integration/test_homepage_services.py` → rename to `tests/integration/test_homepage_tiles.py`; read `data.get("tiles", [])`; update "services" wording.
- [X] T019 [P] Update `tests/contract/test_config_schema.py`: allowed keys `{"title","tiles","tile_groups","bookmark_groups","editor","edit_config"}`; `test_contract_service_required_fields`→iterate `data.get("tiles", [])`; update the example parse assertions.
- [X] T020 [P] Update `tests/unit/test_editor_config.py` / `tests/integration/test_invalid_config.py` raw-YAML fixtures using `services:`→`tiles:`.
- [X] T021 Run `uv run pytest -q` and confirm the full suite is green after the rename.

**Checkpoint**: Foundation ready — the app persists/reloads/configures/renders "tiles", and all existing tests pass on the renamed vocabulary. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Use the Flat "Tiles" List (Priority: P1) 🎯 MVP

**Goal**: A flat `tiles:` list renders a plain row of clickable tiles in the main area, with no grouping and no errors (spec FR-001).

**Independent Test**: Write a config with only a flat `tiles:` list, load the homepage, and confirm every tile renders as a `tile` link in the main `col-12 col-lg-9` area, opening `http(s)` URLs in a new tab, with icon/monogram fallback.

- [X] T022 [P] [US1] Add a unit test asserting a flat `tiles` list renders each tile's name and URL (opening in a new tab, `noopener noreferrer`) in `tests/unit/test_views_tiles.py` (analogous to the pre-rename `test_services_render_name_and_url`). Write first; confirm it fails for the rename reason, then make it pass.
- [X] T023 [P] [US1] Add an integration test verifying the flat `tiles` list from `config/example.yaml` renders every tile name on the homepage in `tests/integration/test_homepage_tiles.py`.
- [X] T024 [US1] Confirm `app/templates/index.html` renders the flat `tiles` list (from the Foundational rename) as a tile grid with `tile` classes and valid escaped names/URLs; ensure no `tile_groups` iteration is needed for this story.

**Checkpoint**: User Story 1 fully functional and testable independently (flat `tiles` renders). **MVP delivered** — stop and validate.

---

## Phase 4: User Story 2 - Organize Tiles Into Named Groups With Always-Visible Headers (Priority: P1)

**Goal**: Tiles can be split into named `tile_groups`, each rendering a labeled header followed by its tiles, always visible with no collapse/expand (spec FR-002/003/004/006/010).

**Independent Test**: Write a config with two or more `tile_groups`, each with nested `tiles`; load the homepage and confirm each group renders a header showing its name followed by only its own tiles, in declared order, fully visible with no collapse control.

- [X] T025 [P] [US2] Add a unit test in `tests/unit/test_schema.py` asserting `parse_dashboard` builds `TileGroup` objects from `tile_groups[].tiles` (names/URLs parsed; empty group valid). Write first; confirm it fails, then make it pass.
- [X] T026 [US2] Add schema validation for a `tile_groups` entry: missing `name` or non-list `tiles` -> `ConfigValidationError` (spec FR-007) in `app/schema.py`; add unit tests in `tests/unit/test_schema.py` (associating with FR-007).
- [X] T027 [P] [US2] Add an integration test in `tests/integration/test_homepage_tiles.py` asserting grouped tiles render: each group has a header with its name, its own tiles only, no `data-bs-toggle`/collapse within a tile group.
- [X] T028 [US2] Update `app/templates/index.html`: after the flat `tiles` section, iterate `tile_groups`; for each render a `<h3 class="group-title">{{ group.name }}</h3>` followed by a `.row g-3` of its tiles using the same `tile` tile markup. No collapse control (FR-010).
- [X] T029 [US2] Confirm mixed flat `tiles` + `tile_groups` renders flat first then groups (spec FR-006) via an integration test in `tests/integration/test_homepage_tiles.py`.

**Checkpoint**: User Stories 1 AND 2 work independently (flat + grouped tiles).

---

## Phase 5: User Story 3 - Set an Icon for Each Tile Group (Priority: P2)

**Goal**: A `tile_groups[].icon` value renders beside the group name; groups without an icon show the name alone (spec FR-005).

**Independent Test**: Give one `tile_groups` entry an `icon` (valid `http(s)` URL) and another none; load the homepage and confirm the first shows the icon beside the group name and the second shows only the name.

- [X] T030 [P] [US3] Add schema unit test in `tests/unit/test_schema.py` asserting a `tile_groups[].icon` is preserved on the `TileGroup` (string, optional) and a missing icon is `None`.
- [X] T031 [P] [US3] Add an integration test in `tests/integration/test_homepage_tiles.py` asserting a group with an icon renders an `<img>` next to the group name (with `onerror` fallback), and a group without an icon renders the name with no `<img>`.
- [X] T032 [US3] Update `app/templates/index.html` tile-group header to render the optional group icon using the same escaped `icon`-as-`<img>`-with-monogram-fallback pattern used for tile icons and bookmark group icons (FR-005).

**Checkpoint**: User Stories 1, 2, and 3 work independently.

---

## Phase 6: User Story 4 - Move Between Flat and Grouped Layouts Effortlessly (Priority: P2)

**Goal**: Moving a tile between groups, or in/out of the flat list, or renaming a group, takes effect on reload with no code change or rebuild (spec FR-008 via live reload; FR-009 via the editor).

**Independent Test**: Edit the config text to move a tile from one group to another (and from a group into the flat `tiles` list), bump the file mtime, and confirm on the next request the tile renders in its new location.

- [X] T033 [P] [US4] Add an integration test in `tests/integration/test_config_reload.py` that moves a tile between two `tile_groups` (mtime-bumped config) and asserts the tile renders in the new group on the next page request (spec FR-008).
- [X] T034 [P] [US4] Add an integration test asserting a tile moved from a group into the flat `tiles` list renders in the ungrouped area after reload.
- [X] T035 [US4] Confirm the in-browser config editor's save path validates `tile_groups`/`tiles` the same as flat config (spec FR-009); add an integration assertion in `tests/integration/test_config_editor_flow.py` that a saved config containing valid `tile_groups` renders on the next load and a malformed one is rejected.

**Checkpoint**: User Stories 1–4 work independently.

---

## Phase 7: User Story 5 - See a "Bookmarks" Header Above the Bookmark Accordion (Priority: P1)

**Goal**: A hardcoded "Bookmarks" heading renders directly above the bookmark accordion when bookmark groups exist (spec FR-011).

**Independent Test**: Load the homepage with at least one `bookmark_groups` entry and confirm a heading reading exactly "Bookmarks" appears above the accordion; it is not configurable.

- [X] T036 [P] [US5] Add an integration test in `tests/integration/test_navbar.py` (or a new `tests/integration/test_bookmarks_header.py`) asserting `<h3 ...>Bookmarks</h3>` (or a heading with text "Bookmarks") appears before the `bookmark-accordion` when `bookmark_groups` is non-empty.
- [X] T037 [US5] Update `app/templates/index.html`: inside the `aside[aria-label="Bookmarks"]`, before the accordion, render a hardcoded `<h3 class="group-title">Bookmarks</h3>` only when `bookmark_groups` is non-empty (FR-011).

**Checkpoint**: User Stories 1–5 work independently.

---

## Phase 8: User Story 6 - Rebrand Everything as "Tiles" (Internal and User-Facing) (Priority: P1)

**Goal**: No applicable "services" reference remains for the former services feature anywhere in the repository (source, config, CSS, tests, docs); everything uses "tiles" (spec FR-012, SC-006).

**Independent Test**: Run a repository-wide case-insensitive search for "services" (excluding `.git`, `node_modules`, `.venv`, and the final user-config bookmark label "National Benefits Services") and confirm no applicable reference remains; the homepage `aria-label` is "Tiles".

- [X] T038 [P] [US6] Update the `<meta name="description">` and HTML comment in `app/templates/index.html` from "services" to "tiles".
- [X] T039 [P] [US6] Update `README.md`: rename the "**Services**" feature bullet to "**Tiles**" and reword all config comments/mentions ("Put links to your homelab services here" → "...tiles here"; any `services:` snippet → `tiles:`).
- [X] T040 [P] [US6] Rename remaining test files/functions containing "service": e.g. rename `tests/integration/test_config_reload.py` function `test_service_logo_change_reflected_on_reload`→`test_tile_logo_change_reflected_on_reload`; scan all `tests/` for `service` in identifiers and function names and rename to `tile`.
- [X] T041 [P] [US6] Add an integration assertion in `tests/integration/test_homepage_tiles.py` that the homepage main section has `aria-label="Tiles"` (not "Services").
- [X] T042 Run `grep -rni "service"` over `app/`, `config/example.yaml`, `tests/`, and `README.md` (excluding `.git`, `node_modules`, `.venv`, and the final-user bookmark label "National Benefits Services"); fix any remaining applicable reference to "tiles" (FR-012, SC-006).
- [X] T043 Run `uv run pytest -q` and confirm the full suite is green after the rebrand.

**Checkpoint**: User Stories 1–6 work independently; the whole repository uses "tiles".

---

## Phase 9: User Story 7 - Use Tiles for Both Homelab and External Services (Priority: P2)

**Goal**: Documentation and the example config convey that a tile can link to an internal homelab service OR an external service (e.g., webmail, a cloud portal); both open in a new tab (spec FR-013, SC-007).

**Independent Test**: Read README/example config comments and confirm they present tiles as usable for both kinds, with at least one homelab example and one external example; click an external `http(s)` tile and confirm it opens in a new tab.

- [X] T044 [P] [US7] Update `config/example.yaml` to include at least one tile pointing to an external service (e.g., an email provider's webmail or a cloud-account portal) alongside internal homelab tiles; update the `tiles:` header comment to state tiles may link to homelab or external services (FR-013).
- [X] T045 [P] [US7] Update `README.md` to describe a tile as usable for both internal homelab services and external services (e.g., email providers, cloud accounts), with an example of each (FR-013, SC-007).
- [X] T046 [US7] Confirm a tile with an external `http(s)` URL renders identically and opens in a new tab via an existing/added integration test in `tests/integration/test_homepage_tiles.py`.

**Checkpoint**: User Stories 1–7 all work independently.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, consistency, and cleanup.

- [X] T047 Run `uv run pytest -q` and confirm the entire suite (unit + integration + contract) passes in a clean run.
- [X] T048 Execute the scenarios in `specs/009-service-link-groups/quickstart.md` (V1–V7), confirming flat `tiles`, grouped `tile_groups`, group icons, mixed flat+grouped, the "Bookmarks" header, the full "Tiles" rebrand, and malformed-group rejection all behave as documented.
- [X] T049 Run the repo's lint/format tooling (per `pyproject.toml` / README, e.g. `ruff`) over all changed files and fix issues.
- [X] T050 Final repo-wide `grep -rni "service"` sweep (excluding `.git`, `node_modules`, `.venv`, and the final-user bookmark label "National Benefits Services") to confirm no applicable "services" reference remains; confirm README/quickstart reflect the "Tiles" terminology and external-service positioning.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately (aligns stale docs).
- **Foundational (Phase 2)**: Depends on Setup. **BLOCKS all user stories** (the "tiles" rename is the base everything builds on).
- **User Stories (Phase 3+)**: All depend on Foundational completion. US2 depends on the `tile_groups` schema added in Foundational (T008). US3 depends on US2's group header (T028). US4 depends on US2 (grouping) + reload/editor. US5 (bookmarks header) is independent of tile grouping and could proceed once Foundational is done. US6 (full rebrand) depends on Foundational (the core rename) but otherwise spans; its doc/aria/test sweeps are largely independent. US7 (docs/example) can proceed once Foundational has renamed the example config.
- **Polish (Phase 10)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: After Foundational — no dependency on other stories.
- **US2 (P1)**: After Foundational; uses `tile_groups` schema from T008.
- **US3 (P2)**: After US2 (renders into the group header from T028).
- **US4 (P2)**: After US2 (grouping) — exercises reload/editor of groups.
- **US5 (P1)**: After Foundational — independent of tile grouping.
- **US6 (P1)**: After Foundational — spans the whole repo; can be worked in parallel with other stories where files don't overlap.
- **US7 (P2)**: After Foundational — docs/example only.

### Within Each User Story

- Tests MUST be written and FAIL before implementation (constitution red-green-refactor).
- Schema/model before rendering; rendering before integration tests.
- Story complete and independently testable before moving to the next priority.

### Parallel Opportunities

- All Phase 1 setup tasks (T001–T006) touch different files → parallel.
- All Foundational tasks (T007–T020) touch different files → parallel. T021 (single test run) is the phase checkpoint, not parallel.
- Within a story, tasks marked [P] run in parallel; the non-[P] task depends on them.
- Different user stories can be worked in parallel by different people where file sets don't overlap (e.g., US5 bookmarks header vs. US3 group icons).

---

## Parallel Example: User Story 2

```bash
# Launch schema + rendering-contract tests for US2 together:
Task: "Add unit test for TileGroup parsing in tests/unit/test_schema.py (T025)"
Task: "Add integration test for grouped rendering in tests/integration/test_homepage_tiles.py (T027)"

# Launch implementation after tests fail:
Task: "Validate tile_groups schema in app/schema.py (T026)"
Task: "Render tile_groups with headers in app/templates/index.html (T028)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (align docs).
2. Complete Phase 2: Foundational (the "tiles" rename) — CRITICAL, blocks all stories.
3. Complete Phase 3: User Story 1 (flat `tiles` renders).
4. **STOP and VALIDATE**: run `uv run pytest -q` and confirm US1 independently.
5. Deploy/demo if ready.

### Incremental Delivery

1. Setup + Foundational → the dashboard speaks "tiles" end to end.
2. Add US1 (flat tiles) → test → deploy/demo (MVP).
3. Add US2 (tile groups) → test → deploy/demo.
4. Add US5 (Bookmarks header) + US3 (group icons) → test → deploy/demo.
5. Add US4 (reorganization) → test → deploy/demo.
6. Add US6 (full rebrand sweep) + US7 (external positioning docs) → test → deploy/demo.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together.
2. Once Foundational is done:
   - Developer A: US1 then US2 (grouping core).
   - Developer B: US5 (bookmarks header) — independent.
   - Developer C: US3 (group icons) after US2, or US6 (rebrand doc sweep) in parallel.
3. Stories integrate independently; Polish runs last.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to its user story for traceability.
- The constitution mandates test-first: write the failing test, watch it fail, then implement (TDD).
- Commit after each task or logical group; never commit secrets.
- Stop at any checkpoint to validate the story independently.
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break independence.
- The legacy `services`/`service_groups` config keys are intentionally NOT supported (breaking change); do not add back-compat aliases.
