# Changelog — scrumia-github-project

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `composition.json` and `scrumia-github-project-manifest` — this module declares the actions it
  provides, the fragment to open for each, and how a person reaches it, so the
  composed assemblies are built from it rather than from prose about it.
### Changed
- The board tool is published as the name `scrumia-board`, which the harness puts on the
  session's PATH, and every skill and command runs that name instead of a path. Reaching it
  by path only ever worked in this module's own repository: installed, the module sits one
  version segment deeper and the path resolved to nothing at all.
- `scrumia-sprint`'s call into this module — and any other module's — is now a name, so this
  module can be installed anywhere without its callers knowing where.
- Every link into this repository's ADRs and specs is an absolute URL: a relative one assumed
  a consuming project had files it has never had.

- `scrumia-ticket` step 3 now asks for a line under a shipped module's `[Unreleased]`
  when the ticket changes that module, not only for the spec changelog entry.
- `scrumia-ticket` Step 3 now routes an executor to the specs module's own authoring
  checklist before writing a spec, not only to which file to open — naming
  `scrumia-feature`'s must/must-not checklist when that module fills the `specs` slot.
- `scrumia-ticket` no longer carries its own list of branch/commit types: it cites the
  project's one vocabulary. A project whose composition decides no vocabulary falls back
  to the prefixes its own history already uses.
- `scrumia-ticket` writes commits as `<type>(<scope>): …` with a `Refs: #<n>` trailer on
  every commit, and `Closes #<n>` exactly once in the PR body. Adopting this changes what
  a project's history looks like from the first ticket run after the update; nothing
  rewrites the commits already written. The scope's four namespaces are stated in the
  skill itself, so a project reaches no repository-relative file to write one.
- `scrumia-ticket`'s commit-scope paragraph now matches the generalized comma form: a
  commit atomic across several scopes names them all regardless of namespace, not modules
  only, and `<type>(*):` covers a commit spanning more scopes than are worth naming
  individually.
- `scrumia-project-setup`'s label table now names `scrumia-manager` as a reader of
  `scope/*`, alongside `pick-model.sh`, so the row no longer implies a single reader.

### Deprecated
- `scripts/board.sh` — kept as a shim that warns and delegates. It is removed at the second
  release after the one shipping this; run `scrumia-board`.

## [0.4.0] - 2026-08-10
### Added
- The `tracker` slot on GitHub Projects: issues, native sub-issues, columns, branches and PRs — no project state in the repository.
- `scrumia-refine`, `scrumia-ticket`, `scrumia-review`, `scrumia-status` — and their `/refine`, `/ticket`, `/review`, `/status` commands.
- `scrumia-project-setup` — seeds columns, labels and issue templates.
- `board.sh` — the only supported way to talk to the board: a `gh project` read without a filter is silently truncated at 30 items.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
