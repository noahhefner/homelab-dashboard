<!--
  Sync Impact Report
  Version change: 1.0.0 -> 1.1.0
  Modified principles: n/a
  Added sections:
    - Framework-First Frontend
  Removed sections: none
  Templates requiring updates:
    - .specify/templates/plan-template.md        (used as referenced; no change needed)
    - .specify/templates/spec-template.md        (no mandatory-section changes; no change)
    - .specify/templates/tasks-template.md       (test task types align; no change)
    - .specify/templates/checklist-template.md   (no change)
    - .specify/templates/commands/               (no commands directory present; n/a)
  Follow-up TODOs: none
-->

# homelab-dashboard Constitution

## Core Principles

### I. Developer Experience First
Developer experience (DX) is a first-class requirement, not an afterthought. Every
feature, interface, and workflow MUST optimize for the experience of the developers
who read, run, and extend this codebase. Local development MUST be one command away:
deterministic, reproducible, and fast to iterate on.

Changes MUST NOT add friction to the common developer loop (edit → run → verify).
Diagnostics MUST be actionable: errors MUST surface the cause, the affected component,
and where to look next rather than a bare failure. Tooling, scripts, and documentation
are part of the product and MUST be maintained to the same standard as application code.

Rationale: A homelab dashboard is long-lived and typically maintained by a small
number of people over years. High DX keeps context-switch cost low and makes the
project sustainable to maintain and hand off.

### II. Readability Over Cleverness
Code MUST be written for the next reader, not for the author. Clarity and
intentionality take precedence over brevity, cleverness, or micro-optimization.
Expressive, self-documenting identifiers MUST be preferred over cryptic shorthand.

New functionality in existing code MUST match the surrounding structure and
conventions so the codebase reads as one coherent body. Comments MUST explain why,
never restate what the code already says. Where a concept is non-obvious, the
rationale MUST be captured at the point of the code (or a referenced spec), not lost
in an external discussion.

Rationale: Readable code reduces the cost of every future change and review. In a
project maintained opportunistically, readability is the primary guard against
knowledge loss and regressions.

### III. Extensibility & Modularity
The dashboard MUST be built as a set of small, clearly bounded modules rather than a
monolith of intertwined concerns. New capabilities MUST be addable without modifying
existing modules wherever the architecture allows (open/closed).

Each module MUST expose a minimal, stable contract and MUST keep its implementation
details private behind that contract. Dependencies between modules MUST be explicit and
acyclic; implicit coupling through shared mutable state is forbidden. Adding a widget,
data source, or integration SHOULD follow an extension point rather than a fork-and-edit
of existing code.

Rationale: Extensibility is what lets the dashboard grow to cover new homelab
integrations cheaply and safely. Explicit boundaries keep that growth from degrading
into an untestable, coupled tangle.

### IV. Testability (Test-First, NON-NEGOTIABLE)
Tests MUST be written before or alongside the code they validate and MUST be approved
as part of the change. A change is not complete until its tests pass in a clean run. The
red-green-refactor cycle MUST be followed: write a failing test, confirm it fails for the
expected reason, then make it pass.

Module contracts and shared schemas MUST have contract tests. Any communication across
module boundaries, and any behavior that a future extension could break, requires an
integration test. Environments and third-party services MUST be mockable so tests are
deterministic and runnable anywhere. Tests MUST run in CI and locally with a single command.

Rationale: A self-hosted dashboard with many optional integrations depends on tests to
prove that adding or removing a module does not silently break the rest. Test-first is
the only reliable way to keep that promise.

### V. YAGNI & Simplicity
Build only what is needed now. Features, abstractions, and configuration MUST be deferred
until a concrete requirement justifies them. The simplest design that satisfies the
current requirements and is still extensible under Principle III MUST be chosen.

Complexity MUST be justified. Introducing a new framework, dependency, pattern, or
conceptual layer beyond what the problem demands is a governance violation unless it
eliminates greater complexity elsewhere. Unused code paths, dead configuration, and
redundant abstractions MUST be removed rather than preserved "in case."

Rationale: Every extra piece of complexity is future maintenance and future confusion.
Simplicity keeps the dashboard approachable for new contributors and keeps the
developer experience (Principle I) fast.

### VI. Framework-First Frontend
All frontend code MUST leverage the project's chosen framework (Bootstrap) for
styling, layout, and interactive behavior whenever it provides a suitable class,
component, or utility. Custom CSS and JavaScript MUST only be written when the
framework demonstrably lacks the needed capability, and that custom code SHOULD be
minimal and confined to the narrowest possible scope.

- Bootstrap utility classes (spacing, display, flex, text, borders, etc.) MUST be
  preferred over hand-written CSS for the same effect.
- Bootstrap components (cards, modals, navbars, buttons, alerts, etc.) MUST be used
  as the starting point rather than building equivalent structures from scratch.
- Custom CSS SHOULD target only what Bootstrap cannot express; overrides and
  extensions of Bootstrap defaults MUST be documented with a rationale.
- Custom JavaScript SHOULD be limited to behavior not provided by Bootstrap's JS
  plugins or the project's existing interaction patterns.

Rationale: Reusing the framework reduces duplicated styling effort, keeps the UI
consistent, and prevents the accumulation of one-off CSS that becomes difficult to
maintain. It aligns with Principle V (Simplicity) and Principle III (Modularity) by
letting a shared, well-tested foundation do the heavy lifting.

## Security Requirements

This dashboard runs in a homelab and may expose services beyond the local network.
Security MUST be considered at every change.

- Secrets (API keys, tokens, credentials) MUST NEVER be committed or logged. Secrets
  MUST be injected via environment variables or a supported secrets manager.
- Any screen or endpoint that renders user- or third-party-controlled content MUST
  escape/encode output to prevent injection. External URLs MUST be validated.
- Access controls MUST follow least privilege: a reason to expose something is required,
  and default-deny is preferred.
- Changes that touch authentication, authorization, network exposure, or data handling
  MUST be called out in review so the security impact is explicitly assessed.
- Existing external integrations MUST be contacted over HTTPS/TLS and with timeouts and
  error handling so a bad upstream cannot hang the dashboard.

Rationale: Homelab deployments often rely on a single device and a self-managed
network. A compromise of the dashboard can expose the whole lab, so security is treated
as a correctness requirement, not a remote-team concern.

## Development Workflow

- Changes MUST be developed in feature branches and merged via reviewed pull requests.
- Every pull request MUST satisfy the quality gates: lint clean, tests pass (including
  any new contract/integration tests), and no secrets introduced.
- A change MAY be rejected if it violates a Core Principle; complexity added without
  justification is a review-blocking issue.
- Commit messages MUST be concise and descriptive, matching the project's style, and
  each commit MUST represent a coherent unit of change.
- README and quickstart documentation MUST be kept accurate and updated when developer
  workflows or commands change (Principle I).
- Candidate changes to governance, architecture boundaries, or shared contracts MUST be
  discussed before implementation to avoid rework.
- Code MUST be formatted using the appropriate formatting tooling after each change.

## Governance

This Constitution supersedes all other ad-hoc practices and informal conventions. All
development MUST comply with the Core Principles above.

- **Amendments**: Changing or adding a Principle is a constitutional amendment. It MUST
  be documented here, justified with rationale, and reflected in this file's version and
  date line before it takes effect.
- **Versioning**: Semantic versioning governs this document.
  - MAJOR: removal or redefinition of a Principle, or a backward-incompatible governance
    change.
  - MINOR: a new Principle or section added, or materially expanded guidance.
  - PATCH: clarification, wording, or typo refinements without semantic change.
- **Compliance review**: Every plan includes a Constitution Check gate (see
  `.specify/templates/plan-template.md`) that MUST pass before and after design. PR
  reviewers MUST verify changes remain compliant. Use the governance-grounded guidance
  in the current plan for day-to-day development decisions.
- **Deviations**: Any deviation from a Principle is permitted only with explicit,
  documented justification, and the added complexity MUST be logged in the plan's
  Complexity Tracking table.

**Version**: 1.1.0 | **Ratified**: 2026-08-28 | **Last Amended**: 2026-09-03
