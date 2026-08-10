# Changelog — scrumia-practice-tanstack-query

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.4.0] - 2026-08-10
### Added
- The `practices` slot for TanStack Query, applied app by app and adapter-agnostic: query keys, the `queryOptions()` factory, `useQuery` through testing.
- `scrumia-tanstack-query` — the reference; `scrumia-tanstack-query-scaffold` — the step-by-step scaffold.
- A query-key vocabulary reference in `01-query-keys.md`, and a migration guide
  (`10-migrating-an-existing-codebase.md`) for a codebase written against the older names.
- Decision records `D-12` (`as const` on the outer object only) and `D-13` (the `all` / `list` /
  `detail` / `search` naming vocabulary, with the rejected `_root` alternative recorded).

### Changed
- Query keys take a single `as const` on the outer object rather than one per line.
- The key vocabulary is closed to `all`, `list`, `detail` and `search`; `byUser`, `byId`,
  `byResource` and `listByCategory` are gone from every guide.
- `list` and `detail` spread directly from `all`; invalidation targets `all`.
- The guides reference `queryKeys.*` instead of inlining key arrays.

### Removed
- The `lists()` and `details()` scope functions — indirection with no practical benefit.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
