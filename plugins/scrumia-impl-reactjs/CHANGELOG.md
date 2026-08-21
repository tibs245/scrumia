# Changelog — scrumia-impl-reactjs

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Changed
- **Breaking — the project override moves to `.scrumia/overrides/scrumia-impl-reactjs.md`,
  from `.scrumia/impl/scrumia-impl-reactjs.md`.** `.scrumia/impl/` and
  `.scrumia/practices/` only ever differed by a category of module that no longer
  exists, so they collapse into one directory
  ([ADR-0024](https://github.com/tibs245/scrumia/blob/main/docs/adr/0024-no-category-of-module.md)).
  A project with an override file must move it; left where it is, it is not read.

## [0.1.0] - 2026-08-13
### Added
- The `implementation` slot for React 19, plugged in app by app: Server Components by default, Actions and `useActionState` for mutations and forms, derived state calculated during render, behaviour-first component tests, feature-based structure.
- `scrumia-reactjs` — the routing index; `scrumia-reactjs-audit` — the audit against it.
- Six guides: components-and-props, state-and-derivations, control-flow, data-boundary, project-layout, testing.
- Four refusals (`D-01` through `D-04`) — each cites the React 19 docs passage that grounds it: `useEffect` for derived state, imperative DOM, effects where event handlers belong, unnecessary `"use client"`.
