# Research: Bookmark Group Default State

**Phase 0 output for `/specs/006-bookmark-group-default-state/plan.md`**

Purpose: resolve the technical decisions needed to add a per-group configuration option
that controls whether a bookmark group starts open or closed on page load, working within
the existing Flask/Bootstrap dashboard and the Constitution's principles.

## 1. Where to Put the Config Value

- **Decision**: Add an optional boolean field to each `BookmarkGroup` entry in the YAML
  config, named `collapsed` (e.g., `collapsed: true` means the group starts closed;
  `collapsed: false` or absent means it starts open). Parse it in `app/schema.py`
  `_parse_group` and store it on the `BookmarkGroup` dataclass in `app/model.py` with a
  default of `False`.
- **Rationale**: This mirrors the existing per-group fields (`name`, `icon`, `bookmarks`)
  and the per-service `icon` pattern — the config model is a validated YAML mapping. A
  single optional boolean is the simplest, most discoverable expression of "open or
  closed" (Principle V). A default of `False` (open) preserves the current behavior for
  groups that don't set it (spec FR-002).
- **Alternatives considered**:
  - A top-level global default with per-group overrides: rejected — spec explicitly wants
    per-group configurability; a global adds complexity with no requested benefit.
  - A string like `state: "open"|"closed"`: rejected — a boolean is simpler and less
    error-prone for a binary choice.
  - Inferring from existing data (e.g., bookmark count): rejected — that would be
    surprising and non-deterministic; the user asked for explicit config.

## 2. How the Config Default Reaches the Browser

- **Decision**: Emit the configured default onto the group's toggle button as a data
  attribute, e.g. `data-default-collapsed="true"` or `"false"`, in
  `app/templates/index.html`. The existing client-side JS in `app/static/app.js` reads it
  when no saved preference exists.
- **Rationale**: The app is server-rendered Jinja2; the config is already available at
  render time. Embedding the boolean as a data attribute on the existing toggle is the
  minimal, idiomatic way to pass it to the vanilla JS that already manages collapse
  (feature 002). No new endpoint or server round-trip is needed.
- **Alternatives considered**: a separate JSON config loaded at runtime — rejected (adds a
  fetch and coupling); server-rendering the collapsed CSS class directly (e.g., adding
  `show` or removing it) — rejected because the JS's `apply()` owns the DOM state and the
  persisted choice must win; a data attribute is a clean, single source the JS already
  centralizes.

## 3. Precedence: Saved User Choice vs. Config Default

- **Decision**: A previously saved per-group choice in `localStorage` (feature 002) takes
  precedence over the config default. The JS must distinguish "no saved value" from a
  saved value: if a saved value exists, use it; otherwise fall back to the config default.
  The config default only applies to groups with no saved user choice (spec FR-004/FR-006).
- **Rationale**: This preserves the established behavior where a user's explicit in-session
  action persists across visits. Overriding a user's saved choice with the config default
  would be surprising and is explicitly excluded by FR-004. It is consistent with the
  existing `readPersisted`/`writePersisted` approach in feature 002.
- **Alternatives considered**: config always overrides saved state — rejected (violates
  FR-004 and silently discards the user's explicit choice); saving the config default into
  localStorage on first load — rejected (would lock in the default as if the user chose
  it, breaking later config changes from taking effect per FR-006).

## 4. Validation and Broken-Value Handling

- **Decision**: Validate `collapsed` strictly as a boolean in `_parse_group`. A non-boolean
  value (e.g., a string like `"yes"`) raises the existing `ConfigValidationError`, matching
  how other invalid fields are handled and surfacing a clear message. Absent or `null`
  means `False` (open).
- **Rationale**: The project already validates config strictly via `parse_dashboard` and
  surfaces errors on the page (feature 001). A boolean-valued field is unambiguous, and
  strict validation prevents a typo from silently producing the wrong initial state.
- **Alternatives considered**: lenient coercion (treat any truthy string as true) —
  rejected (silently ambiguous, inconsistent with the project's strict validation).

## 5. Deliverable Scope

- **Decision**: Concrete outputs: (a) tests (written first) for `collapsed` parsing/
  validation/default, the rendered default-state attribute, and the JS precedence logic;
  (b) app changes (model field, schema parse, template data attribute, JS precedence); (c)
  example config + README/quickstart docs. No new endpoints, database, or server state.
- **Rationale**: Test-first (Principle IV) and accurate developer docs (Principle I),
  keeping the implementation small and free of speculative complexity.
- **Alternatives considered**: a schema of per-group settings or a settings management
  subsystem — rejected (YAGNI; a single optional boolean fully satisfies the request).
