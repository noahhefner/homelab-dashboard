# Research: Fix Pyrefly Errors

**Feature**: `014-fix-pyrefly-errors` | **Date**: 2026-11-15

## Baseline

`uv run pyrefly check app tests` reports **23 errors** and **21 warnings**:

| Area | Errors | Files |
|------|--------|-------|
| Application code | 1 | `app/__init__.py` (caused by `app/security.py` contract) |
| Tests | 22 | 1 contract, 4 integration, 3 unit files |

The 21 warnings are all `untyped-import` notices for `yaml`, with pyrefly suggesting `types-PyYAML`. Applying `--min-severity=warn` shows no other warning categories.

`uv run pytest` passes on the baseline, confirming the errors are static-type diagnostics rather than runtime failures.

## Decision 1: Correct the Jinja test-callable contract in `app/security.py`

**Decision**: Rename `validate_url`'s parameter from `url` to `value`, annotate it as `value: object`, annotate the return type as `bool`, and return `bool(parsed.netloc)` instead of the raw netloc string.

**Rationale**: Two separate issues are combined in the reported error:

1. The function returns `Literal[False] | str` because `parsed.netloc` is a string. Jinja tests are typed to return `bool`.
2. Jinja's `Environment.tests` mapping is typed against a union of callable shapes whose one-argument forms name the parameter `value`. A minimal in-repo probe showed that a correctly annotated `(value: object) -> bool` function is accepted, while an otherwise identical `(url: object) -> bool` function is rejected by pyrefly with the same `Callable is missing a positional parameter` diagnostic.

Renaming the parameter is therefore required to satisfy the existing typed contract, not a stylistic choice. Returning `bool(parsed.netloc)` keeps the same truthiness that templates already observe while matching the declared `bool` return. `validate_url` callers in `app/schema.py` use it only in boolean contexts, so accept/reject behavior is unchanged.

**Evidence**: A probe containing the exact revised function and `app.jinja_env.tests["url"] = validate_url` reported 0 errors. A scratch copy with the full remediation also reported 0 errors.

**Alternatives considered**:

- **Keep `url` and add a cast or `# pyrefly: ignore`** — rejected: hides the diagnostic and violates the requirement to preserve type coverage.
- **Annotate the return as `bool` but keep `url`** — rejected: pyrefly still rejects the callable assignment.
- **Wrap the function in a lambda at registration** — rejected: adds indirection and does not improve the contract; the underlying function would remain untyped.
- **Change `validate_url` to raise on invalid URLs** — rejected: changes established behavior and is outside this change.

## Decision 2: Give `ConfigLoader.get()` an accurate optional return type

**Decision**: Import `DashboardConfig` from `app.model` and annotate `ConfigLoader.get()` as `-> tuple[DashboardConfig | None, str | None]`. Add `assert config is not None` (or equivalent) before field access in the four existing test locations that read a returned config.

**Rationale**: `get()` legitimately returns `(None, error)` when the file is missing or invalid, so the accurate contract is optional on both tuple elements. Pyrefly currently infers the returned config as `NoneType` and reports field accesses in `tests/unit/test_config_loader.py`. The annotation states the real contract; the assertions narrow it in the success-path tests and fail fast if the loader unexpectedly returns no config.

**Evidence**: A probe with the annotated getter plus `assert config is not None` reported 0 errors. The scratch-copy dry run confirmed the same for the real file.

**Alternatives considered**:

- **Change `get()` to raise instead of returning an error tuple** — rejected: behavior change; callers depend on the `(config, error)` shape.
- **Cast the result in each test** — rejected: hides the failure mode instead of asserting it.
- **Annotate only the private attributes** — rejected: pyrefly still treats the public return as `NoneType`; the public contract is what callers need.
- **Annotate the return as non-optional** — rejected: incorrect for the missing/invalid config cases.

## Decision 3: Narrow optional BeautifulSoup element lookups in tests

**Decision**: Add explicit `assert element is not None` immediately after `select_one()` in the existing tests before reading attributes or searching descendants.

**Rationale**: `select_one()` returns `Tag | None`. The tests already assume the element exists; making that assumption explicit both clears the diagnostic and produces a clearer failure than an `AttributeError` on `None`. This preserves every assertion and adds no new test cases.

**Affected locations**:

- `tests/contract/test_about_modal_html.py` — modal before finding its link
- `tests/integration/test_homepage_tiles.py` — group header before icon/monogram lookup
- `tests/integration/test_mobile_layout.py` — tiles and bookmarks columns
- `tests/integration/test_navbar.py` — navbar brand
- `tests/unit/test_views_tiles.py` — tile anchor and image

**Alternatives considered**:

- **`cast(Tag, ...)`** — rejected: asserts a type without proving presence and hides real absence failures.
- **Ignore comments** — rejected: violates the no-suppression requirement.
- **Change the tests to re-query after asserting** — rejected: redundant; the existing variable is already the object under test.

## Decision 4: Add a single-valued attribute helper to `tests/soup_utils.py`

**Decision**: Add `attr_str(tag: Tag, name: str) -> str | None`, which returns the attribute only when BeautifulSoup provides a string. Use it for `href`, `src`, and `action` checks that currently call string methods on `AttributeValueList | str | None`.

**Rationale**: BeautifulSoup types attributes that may be multi-valued (such as `class`, `rel`) as `AttributeValueList`, even when a particular attribute like `href` is single-valued. Calling `.startswith()` directly is therefore not type-safe. The helper centralizes the narrowing, is reusable across three existing test files, and preserves the original comparison logic. It is test tooling, not a new test.

**Affected locations**:

- `tests/integration/test_mobile_layout.py` — remote CSS `href` and script `src` filtering
- `tests/integration/test_navbar.py` — search form `action`
- `tests/unit/test_bookmark_icons.py` — image `src` safety check

**Alternatives considered**:

- **Inline `isinstance(value, str)` at every call site** — rejected: repeated boilerplate with no clarity gain.
- **`cast(str, ...)`** — rejected: unsafe for genuinely multi-valued attributes and hides the distinction.
- **Normalize all attributes to strings** — rejected: changes the data model the tests assert on.

## Decision 5: Keep multi-valued class checks in their existing list form

**Decision**: Use `(element.get("class") or [])` consistently for `class` membership checks, matching the pattern already used elsewhere in the suite.

**Rationale**: `class` is legitimately multi-valued, and membership checks are valid on a list. The existing `or []` fallback handles the `None` case without a cast. Three assertions in `tests/integration/test_visibility_toggles.py` are missing this fallback and are the only required edits in that file.

**Alternatives considered**:

- **Convert classes to a space-separated string** — rejected: changes assertion behavior and loses exact-token matching.
- **Cast to `AttributeValueList`** — rejected: does not handle the `None` case and is less readable.

## Decision 6: Scope and test policy

**Decision**: Modify existing tests only. Do not create new test files, test cases, fixtures, or parameterizations. Validate with the existing pytest suite plus the type-check command.

**Rationale**: The user explicitly requested no new unit tests and only changes that correct pyrefly errors. This is a static-type remediation with no new behavior, so the existing suite already provides the behavior contract. The type-check gate directly tests the requested outcome.

**Alternatives considered**:

- **Add a regression test that runs pyrefly** — rejected by the explicit no-new-tests constraint.
- **Add tests for the newly annotated contracts** — rejected: no behavior change and out of scope.

## Decision 7: Leave warning-level YAML import notices alone

**Decision**: Do not add `types-PyYAML` or suppress the `untyped-import` warnings. The 21-warning baseline may remain.

**Rationale**: The request is to fix all errors, warnings do not fail the gate, and adding a stub package would introduce a new development dependency without eliminating a runtime defect. Leaving them untouched also satisfies the requirement not to introduce new warnings.

**Alternatives considered**:

- **Add `types-PyYAML`** — rejected: out of scope and adds a dependency.
- **Add blanket `# pyrefly: ignore` comments** — rejected: hides signals and violates the spirit of the change.

## Validation Note

The complete remediation described above was dry-run in a scratch copy of the repository. Results:

- `uv run pyrefly check app tests` → `0 errors` (21 warnings unchanged)
- `uv run pytest -q` → full suite passes
- `uv run ruff check app tests` → clean
- `uv run ruff format --check app tests` → 33 files already formatted

The implementation phase should reproduce these changes in the working tree and run the same checks, plus `make check`.
