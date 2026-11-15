# Data Model: Fix Pyrefly Errors

**Feature**: `014-fix-pyrefly-errors` | **Date**: 2026-11-15

## Summary

This change introduces **no new data entities, fields, relationships, persistence, or config schema changes**. It corrects static type information only.

The existing dashboard domain model (`Tile`, `Bookmark`, `BookmarkGroup`, `TileGroup`, `DashboardConfig` in `app/model.py`) and the YAML config schema are unchanged. Existing behavior for loading, reloading, validating, and rendering config data is preserved.

## Type Contracts Affected

Although no data model changes are introduced, two internal Python contracts become more precise and are the focus of the implementation:

| Contract | Current effective type | Corrected type | Behavior impact |
|----------|------------------------|----------------|-----------------|
| `validate_url(value)` | Untyped parameter; returns `Literal[False] \| str` | `(value: object) -> bool` | None; truthiness returned to Jinja and callers is unchanged |
| `ConfigLoader.get()` | Inferred `(None, None)` by pyrefly | `() -> tuple[DashboardConfig \| None, str \| None]` | None; the same `(config, error)` tuple is returned for success and failure paths |
| `tests.soup_utils.attr_str(tag, name)` | Does not exist | `(Tag, str) -> str \| None` | Test-only helper; returns a string for single-valued attributes and `None` otherwise |

## Validation Rules

- `validate_url` MUST accept only absolute `http`/`https` URLs, exactly as before. The change from returning a netloc string to `True` MUST NOT alter any accept/reject decision.
- `ConfigLoader.get()` MUST continue to return `(None, error_message)` for missing or invalid files and `(config, None)` for a successfully loaded config.
- `attr_str` MUST NOT coerce multi-valued attributes into strings; it returns `None` for absent or list-valued attributes so tests retain their existing comparison behavior.

## State Transitions

No state transitions are added or modified. `ConfigLoader` keeps its existing load-on-demand behavior: an unchanged file returns the cached config, a changed file re-parses, and a forced reload discards the stat cache.
