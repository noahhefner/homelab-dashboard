# Feature Specification: Fix Pyrefly Errors

**Feature Branch**: `014-fix-pyrefly-errors`

**Created**: 2026-11-15

**Status**: Draft

**Input**: User description: "I need to fix all the pyrefly errors in this project."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clean Type-Check Gate Across the Whole Project (Priority: P1)

As a maintainer, I want the project's static type check to report zero errors for both application code and tests, so the type-check quality gate passes and I can trust a green result.

**Why this priority**: The project recently standardized on pyrefly for type checking, and the existing gate currently fails. A failing gate blocks the normal `make check` workflow and makes it impossible to tell new type regressions from the existing backlog.

**Independent Test**: From a clean checkout, run the project's type-check command against the application and test sources and confirm it reports zero errors and exits successfully.

**Acceptance Scenarios**:

1. **Given** the repository as-is, **When** the maintainer runs the type-check target, **Then** it reports zero error-level diagnostics and exits successfully.
2. **Given** the repository as-is, **When** the maintainer runs the underlying type-check command directly against the application and test sources, **Then** it reports zero error-level diagnostics and exits successfully.
3. **Given** all type errors are fixed, **When** the maintainer runs the full project check target, **Then** every gate (linting, formatting, type checking, template checking, and frontend formatting) passes.

---

### User Story 2 - Preserve Runtime and Test Behavior (Priority: P2)

As a dashboard owner, I want the type fixes to change only static type information, so the dashboard behaves exactly as it did before and all existing tests still pass.

**Why this priority**: Type remediation must not become a behavior change. The existing test suite is the contract that proves the dashboard, config loading, URL validation, and rendered pages remain correct.

**Independent Test**: Run the full existing test suite after the type fixes and confirm every test passes without removing, skipping, or weakening assertions.

**Acceptance Scenarios**:

1. **Given** the type fixes are applied, **When** the full test suite runs, **Then** all pre-existing tests pass.
2. **Given** the type fixes are applied, **When** the dashboard renders the homepage and config editor, **Then** the pages and their interactive behavior are unchanged.
3. **Given** the type fixes are applied, **When** configuration is loaded, reloaded, or rejected as invalid, **Then** the observed outcomes are unchanged.
4. **Given** the type fixes are applied, **When** a configured URL is validated or escaped, **Then** the observed outcomes are unchanged.

---

### User Story 3 - Keep Type Coverage and Diagnostics Trustworthy (Priority: P3)

As a maintainer, I want the errors fixed at their source without blanket suppressions or exclusions, so future type regressions in the same areas are still caught and diagnostics remain actionable.

**Why this priority**: Silencing diagnostics would make the gate green while losing its value. The fix must increase confidence in the codebase, not just hide the current backlog.

**Independent Test**: Review the resulting type-check configuration and the changed code to confirm that no files were removed from type checking, no project-wide suppression was added, and no broad untyped escape hatch replaced a previously checked value.

**Acceptance Scenarios**:

1. **Given** the remediation is complete, **When** the type-check configuration is reviewed, **Then** the same application and test sources remain included as before.
2. **Given** the remediation is complete, **When** the changed code is reviewed, **Then** each fix uses accurate type information or explicit narrowing rather than suppressing the diagnostic across a file or module.
3. **Given** a new type error is intentionally introduced into previously affected code, **When** the type check runs, **Then** the new error is reported rather than hidden.
4. **Given** a third-party boundary genuinely cannot be typed, **When** a narrowly scoped accommodation is necessary, **Then** it is limited to that specific boundary, documented with a reason, and does not hide errors elsewhere in project code.

---

### Edge Cases

- **Optional HTML element lookups**: Tests that query rendered HTML may legitimately find no matching element. The fix must fail fast with a clear test failure instead of accessing attributes on a missing element.
- **Single-valued versus multi-valued HTML attributes**: Attributes such as links and sources are single strings, while attributes such as CSS classes are lists. The fix must treat each according to its actual type without changing assertions.
- **Configuration may be unavailable**: Loading a missing or invalid configuration intentionally yields no configuration plus an error. Tests must distinguish the failure case from the success case before reading configuration details.
- **Template callable registration**: A custom template helper must satisfy the template engine's expected callable contract without changing what templates observe.
- **Genuine defects versus false positives**: A reported error may reveal a real bug rather than a typing gap. Real defects must be fixed in behavior-preserving ways; false positives must be narrowed or documented narrowly, never globally disabled.
- **Warnings versus errors**: Type-checker warnings that are not errors do not fail the gate. They must not be silenced as a side effect of this work, but they are not required to reach zero.
- **Command parity**: Running the type check through the project's make target and running the underlying command directly must produce the same error count.
- **Supported Python version**: All fixes must remain valid under the project's supported Python version and must not require a different interpreter.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project's type-check command, when run against the application and test sources, MUST report zero error-level diagnostics.
- **FR-002**: The project's type-check make target MUST complete successfully with zero error-level diagnostics.
- **FR-003**: Every error-level diagnostic reported at the start of this work MUST be resolved; the baseline is 23 errors (1 in application code and 22 in tests).
- **FR-004**: The full project check target MUST pass end to end once the remediation is complete.
- **FR-005**: The full existing test suite MUST pass without deleting, skipping, or weakening tests to achieve a passing result.
- **FR-006**: The fixes MUST NOT change the runtime behavior of the web application, configuration loading and reloading, URL validation or escaping, or rendered pages.
- **FR-007**: The fixes MUST preserve the project's existing type-check coverage: no previously checked source file or directory may be excluded, and no project-wide or file-wide diagnostic suppression may be introduced.
- **FR-008**: Fixes MUST retain or improve the precision of the affected types. Replacing a checked value with a broadly untyped value solely to silence a diagnostic is not acceptable.
- **FR-009**: Where a narrowly scoped accommodation for an untyped third-party boundary is unavoidable, it MUST be limited to that boundary and documented with the reason it is needed.
- **FR-010**: The remediation MUST NOT add a new runtime dependency or require a different Python interpreter.
- **FR-011**: Warning-level diagnostics present before this work MAY remain, but the remediation MUST NOT introduce new warning-level diagnostics.
- **FR-012**: The type-check workflow MUST remain a single, documented command that gives a clear pass/fail result for developers.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The type-check command reports 0 errors and exits successfully.
- **SC-002**: 100% of the 23 baseline errors are resolved (1 application error and 22 test errors).
- **SC-003**: 100% of the pre-existing test suite passes, with zero tests removed, skipped, or weakened.
- **SC-004**: 0 source files are removed from type-check coverage and 0 project-wide suppressions are added.
- **SC-005**: The full project check target completes successfully in a clean run.
- **SC-006**: The type-check make target and the underlying command report the same error count (0) on the same revision.
- **SC-007**: No new warning-level diagnostics are introduced relative to the 21-warning baseline.
- **SC-008**: Dashboard behavior is unchanged as verified by the existing acceptance tests for the homepage, config editor, URL validation, and configuration loading/reloading.
- **SC-009**: The runtime dependency set is unchanged; no new production package is introduced.

## Assumptions

- The project's configured type checker is pyrefly 1.4.1, invoked through the existing make target and project configuration; the supported interpreter is Python 3.15.
- The baseline is the 23 error-level diagnostics observed on the current revision: 1 in application code related to template helper registration and 22 in test code related to optional HTML lookups, HTML attribute value types, and optional configuration results.
- "All pyrefly errors" means all error-level diagnostics. The 21 warning-level notices about missing third-party YAML type information are out of scope; adding third-party stub packages or otherwise eliminating warnings is not required.
- Application and test sources are both in scope. Test code may be edited to add accurate narrowing or explicit assertions, provided the tests still verify the same behavior.
- Behavior preservation is established by the existing test suite; no new user-facing behavior is being requested.
- No CI pipeline change is required because the project's canonical quality gate is the local check target.
- The project configuration already includes all Python sources and test files; remediation will work within that configuration rather than expanding or shrinking it.
