# Changelog — scrumia-tanstack-query

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `extends.json` — the query-key contract, `queryOptions` and the no-duplication refusal
  are contributed to the `implement` and `review` registers.

### Changed
- **Breaking — this module is now `scrumia-tanstack-query`, renamed from `scrumia-practice-tanstack-query`.**
  There is no category of module and no vocabulary naming one, so the prefix that
  named one is gone ([ADR-0024](https://github.com/tibs245/scrumia/blob/main/docs/adr/0024-no-category-of-module.md)).
  A project that installed the old name has an unresolved key until it updates
  `.scrumia/config.yaml` and reinstalls; the marketplace carries no redirect.
- Its configuration is read from this module's own `params:`, through
  `scrumia-extends --settings`, like every other module's.
- `README.md` brought into the module-anatomy template: "What it refuses" was missing
  entirely and is now stated; "Skills" is renamed "What it ships"; "Settings" is renamed
  "Settings it reads" and no longer reproduces the YAML schema `scrumia-tanstack-query`'s
  own contract already carries; "Project override" folds into "What it expects to find".
  No content dropped, sections reordered to the required reading order.

### Deprecated
- `settings.practices.scrumia-tanstack-query` and `.scrumia/practices/scrumia-tanstack-query.md` — read for now.
  Use this module's own `params:` and `.scrumia/overrides/scrumia-tanstack-query.md`; both retired
  names go in the release that closes the window
  [`release-versioning`](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md) fixes.

## [0.4.0] - 2026-08-10
### Added
- TanStack Query, applied app by app and adapter-agnostic: query keys, the `queryOptions()` factory, `useQuery` through testing.
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
