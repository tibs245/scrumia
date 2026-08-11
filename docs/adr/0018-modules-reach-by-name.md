# ADR-0018 — A module reaches another by a published name, never by a path

**Status**: accepted — 2026-08-11

## Context

A module is installed at a path it does not choose. In this repository it sits at
`plugins/<name>/`. Installed from the marketplace it sits at
`~/.claude/plugins/cache/<marketplace>/<name>/<version>/` — one segment deeper, under a
version.

Every reference written inside a module is resolved against that root, so a relative
path that climbs out of it lands in a different place in each layout:

```
repo        plugins/scrumia-teams/skills/scrumia-sprint/
installed   ~/.claude/plugins/cache/scrumia/scrumia-teams/0.4.0/skills/scrumia-sprint/
```

`${CLAUDE_SKILL_DIR}/../../../scrumia-github-project/scripts/board.sh` therefore reaches
`plugins/scrumia-github-project/` in the repository and
`~/.claude/plugins/cache/scrumia/scrumia-github-project/` — a directory that does not
exist, because the version segment is missing — once installed.

**Adding a `..` does not fix it.** The correct path would name the callee's installed
version, which is not knowable when the reference is written and is not unique either:
`0.3.0` and `0.4.0` sit side by side in one cache, and only
`~/.claude/plugins/installed_plugins.json` says which one this project runs.

Two executable calls were in this shape, both mandated by `CLAUDE.md`, and eighteen more
sites were markdown links into this repository's `docs/` and `features/` — files a
consuming project has never had. `tools/validate.py` passed green on all twenty, because
it resolves them from this repository, where they all exist. The measured failure:
`/scrumia-teams:sprint` step 1 could not run `board.sh ready --milestone`, and the
skill's written fallback covers *"another tracker module fills the slot"*, not *"the path
is wrong with this very tracker"* — so the agent read the board by hand, unfiltered,
which is the silent-truncation case `CLAUDE.md` forbids.

`${CLAUDE_PLUGIN_ROOT}` is not an escape hatch: it is substituted in `hooks.json` and MCP
configs only, never in skill content, which is why `tools/validate.py` already rejects it
there.

## Decision

**A reference written inside a module resolves inside that module.** Two mechanisms, and
only two, for what lies outside it:

1. **A file another module ships is reached by a name.** The owning module publishes it
   as an executable under its own `bin/`, and the caller runs that name with no path at
   all. Claude Code prepends `<pluginRoot>/bin` to the session PATH for every enabled
   plugin, with the install path — version segment included — already resolved by the
   harness. The names carry the `scrumia-` prefix because that PATH is one flat namespace
   shared with every other enabled plugin.

2. **A document belonging to no module is inlined, or cited by absolute URL** —
   `https://github.com/tibs245/scrumia/blob/main/...`. This repository's ADRs and features
   are not part of any module and cannot be reached from one.

`tools/validate.py` enforces both: a reference whose resolved target leaves the plugin
root is an error, and an absolute URL into this repository must name a file that exists.
The rule shipped as prose is the rule that was already being broken.

**Running a published name is not the dynamic slot resolution [ADR-0009](0009-documented-composition.md)
rejected.** What 0009 refused is a registry that decides, at call time, *which module*
answers a verb. Here the caller names one specific file that one specific module
publishes; the name is constant, written into the skill, and greppable — which a relative
path never was. Nothing is looked up but the file's location on disk, and that is the
harness's job, not a resolution the agent holds in mind. 0009's stated cost — "replacing
a module requires checking the others that mention it" — is *cheaper* under this decision,
not dearer: a name greps, a `../../../` does not. BR-4 stands untouched, and this is
recorded in `features/business/modular-composition/` as BR-7, beside it.

## Consequences

**What we gain**

- The two executable calls work in an installed session, which is where they had never
  worked.
- The eighteen documentation links resolve for any reader, in any layout.
- A module's dependency on another is greppable by a constant string, which is what makes
  "an action a module provides but nobody calls" measurable at all.
- The check is mechanical for the two shapes it sees, so those cannot come back silently.

**What we accept**

- **The harness's PATH behaviour is observed, not contracted.** Verified on Claude Code
  2.1.227, by running a probe executable dropped into each layout in turn: every enabled
  plugin's `<root>/bin` is on PATH, whether or not the directory existed when the session
  started, in the repository layout and in the versioned cache
  (`~/.claude/plugins/cache/<marketplace>/<name>/<version>/bin`) alike. Nothing published
  promises it will stay. If it changes, the callers break loudly — the name is not found —
  rather than silently, which is strictly better than what they did before.
- **A bare name only resolves for an enabled plugin.** That is the same precondition the
  skill already had by being read at all, and it keeps `features/business/modular-composition/`'s
  BR-3 intact: a caller that cannot find the name says so, it does not guess a path.
- **`bin/` must exist when the plugin is installed**, which the existing
  restart-after-install rule already covers (`docs/agents.md`).
- **The old script paths stay readable for two releases.** `scripts/board.sh` and
  `scripts/pick-model.sh` are published surface under
  `features/business/release-versioning/`, so they remain as shims that warn and delegate,
  and the modules' changelogs name the release that removes them.
- **A URL is not checked against the branch it names.** The validator checks that
  `blob/main/<path>` exists in the working tree, not that `main` currently carries it.
  A file renamed and the link not updated is caught; a link correct here but stale on
  `main` is not.
- **Only link-shaped and `${CLAUDE_SKILL_DIR}` references are gated.** A bare path written
  in prose — "run `tools/build_features_index.py`", or an inline-code citation of a
  `docs/adr/` file — matches neither syntax and stays a review matter. The decision binds
  those too; the validator does not yet see them, and live ones remain.
- **One script stays where it is.** `scrumia-core`'s `scripts/compose-status.sh` is only
  ever called from inside its own plugin, so it breaks nothing and is deliberately left
  alone — this decision moves what escapes, not everything that could move.

## Rejected alternatives

**Deepen the relative path.** Rejected: it requires one module to name another module's
installed version, which is unknowable at authoring time and ambiguous at run time.

**Read `installed_plugins.json` to find the callee's root.** Rejected: this *is* the
capability registry ADR-0009 refused, rebuilt by hand — an indirection the agent pays on
every call, and one that breaks the moment the harness changes a private file's shape.

**Duplicate the needed scripts and documents into every module that reaches them.**
Rejected: the copies drift, and the divergence is invisible until two modules disagree
about a rule each believes it is quoting.

**Leave the documentation links relative and accept them being broken outside this
repository.** Rejected: a link an agent is told to read and cannot open is
indistinguishable from one it read, which is how this defect stayed green for months.
