# Quickstart: Fix Pyrefly Errors

**Feature**: `014-fix-pyrefly-errors` | **Date**: 2026-11-15

This guide validates the type-check remediation end to end. It assumes the working tree contains the implementation described in [plan.md](plan.md) and [research.md](research.md).

## Prerequisites

- `uv` installed (see the project README)
- Python 3.15 available through `uv`
- For the full `make check` gate: Node.js and pnpm dependencies already installed (`pnpm install`, and `pnpm build` if frontend assets are not yet present)

No new dependencies are needed. The existing development environment is sufficient.

## 1. Verify the type-check gate

```sh
uv run pyrefly check app tests
```

**Expected**: `0 errors`. The 21 pre-existing `untyped-import` warnings for `yaml` may still be reported; they do not fail the command.

```sh
make typecheck
```

**Expected**: command exits successfully with `0 errors`.

## 2. Verify behavior is unchanged

```sh
uv run pytest
```

or:

```sh
make test
```

**Expected**: the full existing suite passes (205 tests at the baseline). No tests are added, removed, skipped, or marked expected-to-fail by this change.

## 3. Verify code quality

```sh
uv run ruff check app tests
uv run ruff format --check app tests
```

**Expected**: lint clean and all Python files already formatted.

## 4. Verify the full project gate

```sh
make check
```

**Expected**: linting, formatting, type checking, template checking with djlint, and frontend formatting with Prettier all pass.

## 5. Confirm the change stayed in scope

Review the working tree:

```sh
git status --short
git diff --stat
```

**Expected**:

- Only `app/security.py`, `app/config.py`, `tests/soup_utils.py`, and the eight existing test files listed in the plan are modified.
- No new test files, no deleted tests, and no new runtime dependencies.
- No changes to `[tool.pyrefly]`, no `project-includes` exclusions, and no file-wide or project-wide suppression directives.
- The warning count remains at the pre-existing 21; no new warning categories appear.

## 6. Confirm the errors are actually caught

A quick sanity check that type coverage was not weakened: temporarily introduce a deliberate type error into a previously failing test expression (for example, assign a string where an integer is expected), run `uv run pyrefly check app tests`, confirm it is reported, then revert the temporary edit.

**Expected**: the deliberate error is reported, proving the fixes narrowed types rather than disabling checking.

## Related Artifacts

- [spec.md](spec.md) — requirements and success criteria
- [plan.md](plan.md) — technical approach and constitution check
- [research.md](research.md) — per-error decisions and alternatives
- [data-model.md](data-model.md) — confirmation that no data model changes are involved
