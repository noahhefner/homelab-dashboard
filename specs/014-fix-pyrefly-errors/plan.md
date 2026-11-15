# Implementation Plan: Fix Pyrefly Errors

**Branch**: `014-fix-pyrefly-errors` | **Date**: 2026-11-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/014-fix-pyrefly-errors/spec.md`

## Summary

Resolve the current 23 pyrefly error-level diagnostics (1 in application code, 22 in tests) without changing runtime behavior, adding tests, or weakening type coverage. The remediation has three parts:

1. Correct the custom Jinja test contract: annotate `validate_url` with the parameter name and `bool` return type that Jinja's typed test-callable expects.
2. Give `ConfigLoader.get()` an accurate optional return type so callers and pyrefly understand that a missing/invalid config is a legitimate outcome; narrow with explicit assertions in the existing tests that read config fields.
3. Add explicit narrowing to existing HTML assertions: assert required elements are present, and introduce one small `tests/soup_utils.py` helper that returns single-valued attributes as `str | None` so `href`/`src`/`action` checks do not fail on BeautifulSoup's multi-valued attribute type.

No new unit tests, test files, dependencies, configuration exclusions, or project-wide suppressions are introduced. A scratch-copy dry run of this exact approach produced 0 pyrefly errors, the full existing pytest suite passing, and ruff lint/format clean.

## Technical Context

**Language/Version**: Python 3.15 (project `requires-python = ">=3.15"`; README documents 3.14+)

**Primary Dependencies**: Flask 3.1.3 with bundled Jinja2, PyYAML 6.x; dev tooling: pyrefly 1.4.1, pytest 9.x, Ruff 0.17.x, BeautifulSoup4 4.15.x

**Storage**: Single YAML config file loaded at runtime; no schema or persistence changes

**Testing**: pytest (contract, integration, and unit suites); existing tests only, no new test cases or files

**Target Platform**: Linux server (self-hosted homelab) and local developer workstations

**Project Type**: Web application (Flask backend, Jinja2 templates, Bootstrap/Vite frontend)

**Performance Goals**: No runtime performance impact. The type-check gate must remain fast enough for the normal edit → check loop; it currently completes in a few seconds.

**Constraints**: Fix error-level diagnostics only; leave the 21 pre-existing `untyped-import` warnings for `yaml` untouched; do not add runtime dependencies; preserve Python 3.15 compatibility; no new tests; no behavior changes; no file exclusions or blanket suppressions; ruff lint and format must stay clean.

**Scale/Scope**: `app/` (7 Python modules) and `tests/` (contract, integration, unit). 23 baseline errors: 1 application error in `app/security.py` via `app/__init__.py`, and 22 test errors across 8 test files.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Developer Experience First | PASS | Turns the failing type-check gate green, making `make check` trustworthy and diagnostics actionable again. |
| II. Readability Over Cleverness | PASS | Uses explicit `assert ... is not None`, accurate annotations, and one named helper instead of casts, ignores, or clever workarounds. |
| III. Extensibility & Modularity | PASS | Production changes are limited to a function contract and a method return annotation; the shared test helper lives in the existing `tests/soup_utils.py` module. No new dependencies or layers. |
| IV. Testability (Test-First) | PASS | Behavior is already covered by the existing suite. Per the user's explicit constraint, no new tests are added; the type-check command itself is the acceptance gate for this type-only change. No tests are removed, skipped, or weakened. |
| V. YAGNI & Simplicity | PASS | Smallest changes that clear each diagnostic; no speculative abstractions, no new packages, no configuration expansion. |
| VI. Framework-First Frontend | PASS (N/A) | No frontend, CSS, JavaScript, or template behavior changes. |
| Security Requirements | PASS | `validate_url` keeps exactly the same accept/reject behavior; only its return representation changes from a truthy string to a boolean. URL validation and escaping semantics are unchanged; no secrets involved. |

**Post-Design Re-check**: PASS — the design introduces no new dependencies, no runtime behavior changes, and no weakened type coverage.

## Project Structure

### Documentation (this feature)

```text
specs/014-fix-pyrefly-errors/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output: per-error decisions and alternatives
├── data-model.md        # Phase 1 output: no persisted data model changes
├── quickstart.md        # Phase 1 output: validation commands and expected outcomes
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created here)
```

`contracts/` is intentionally omitted: this change adds no external API, CLI, or UI contract. The only contracts are internal Python call signatures, captured in `research.md` and `data-model.md`.

### Source Code (repository root)

```text
app/
├── __init__.py          # Unchanged; still registers the Jinja test
├── security.py          # Annotate validate_url and return a real bool
└── config.py            # Add accurate return type to ConfigLoader.get()

tests/
├── soup_utils.py        # Add attr_str() for single-valued HTML attributes
├── contract/
│   └── test_about_modal_html.py       # Assert modal presence before child lookup
├── integration/
│   ├── test_homepage_tiles.py         # Assert group header before child lookup
│   ├── test_mobile_layout.py          # Assert columns; use attr_str for href/src
│   ├── test_navbar.py                 # Assert brand/form; use attr_str for action
│   └── test_visibility_toggles.py     # Normalize optional class attributes
└── unit/
    ├── test_bookmark_icons.py         # Use attr_str for src checks
    ├── test_config_loader.py          # Narrow optional config results
    └── test_views_tiles.py            # Assert tile/image presence before access
```

No files are added to or removed from the type-check project includes. No Makefile or `pyproject.toml` changes are needed because pyrefly is already the configured type checker.

**Structure Decision**: Existing flat Flask layout is retained. Changes are localized to the two production type contracts and the existing test files that contain the diagnostics. The only shared addition is `attr_str()` in the established test-helper module.

## Complexity Tracking

> No Constitution Check violations. No complexity justifications needed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | — | — |

## Validation Strategy

1. `uv run pyrefly check app tests` → 0 errors (warnings may remain).
2. `make typecheck` → 0 errors.
3. `uv run pytest` → full existing suite passes.
4. `uv run ruff check app tests` and `uv run ruff format --check app tests` → clean.
5. `make check` → all project gates pass.
6. Review changed files: no new test files, no exclusions, no blanket suppressions, no new dependencies.

See [quickstart.md](quickstart.md) for the runnable validation guide and [research.md](research.md) for the per-error decisions.
