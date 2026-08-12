# Changelog — scrumia-github-project

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `registers.json` and `dependencies.jsonl` — this module opens the `refine`,
  `implement`, `review` and `audit` registers, and declares the published names it runs,
  qualified by their source. Its four main skills now ask `scrumia-extends` what governs
  the work instead of restating another module's rules.
- `scrumia-review` checks the worktree's `HEAD` against `origin/<branch>` and any SHA a
  review brief names before judging, runs a negative control against any `gh search`
  command a diff writes into a spec, skill or script, flags a restated rule beside a
  `features/` citation that duplicates a trigger or obligation rather than a reason,
  flags a cross-cutting rule newly nested under a SKILL.md step past an earlier yield
  point, greps for stale cross-skill behavior claims on a `plugins/` change, and checks
  that a reservation's issue carries a board card before calling it handled.
### Changed
- `scrumia-board` resolves its settings through `scrumia-extends --settings`, the
  composition's three-layer cascade, instead of reading `settings.tracker` out of
  `.scrumia/config.yaml`. A value set in `.scrumia/config.local.yaml` now actually reaches
  it, and a project that has moved those keys into this module's `params:` keeps working —
  both shapes are read and merged key by key while the migration is in flight, the migrated
  key winning. The key its `params:` sit under comes from the project's own declaration, so
  a `local:` or `shared:` source resolves like a marketplace one.
- `scrumia-board` stops with a named error when its settings cannot be resolved at all —
  `scrumia-core` absent from the session, or no layer carrying the board's ids — rather
  than continuing on defaults. `scrumia-board doctor` is the exception and reports it as a
  fourth check, `settings_resolved`: the command you run to find out what is broken has to
  survive the breakage. `scrumia-board move` also re-emits the error its card lookup
  produced instead of exiting 1 with nothing on stdout.
- `scrumia-core` is now load-bearing for this module: `scrumia-extends` was already declared
  in `dependencies.jsonl`, but a project that ran the tracker without it used to reach the
  board anyway. It now stops. Nothing that composes correctly is affected; a composition
  that was quietly incomplete finds out.
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
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.

### Deprecated
- `settings.tracker` in `.scrumia/config.yaml` — this module's keys move into its own
  `params:` under the `modules:` mapping (ADR-0021). Both shapes are read and merged key by
  key, so a project migrates one key at a time; the retired nest is removed at the second
  release after the one shipping this.
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
