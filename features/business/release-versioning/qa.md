# Acceptance criteria — release-versioning

One scenario per rule in `business.md`. Each scenario must be able to fail. These are
read from a module's manifest, its changelog and the commits behind it — not from
application code, since nothing computes a version today.

## Nominal

### AC-1 — The type is checked against the published surface, not against the files touched

```gherkin
Given a commit typed as one that moves nothing a consumer reads or runs — prose,
  housekeeping, a reshaping — whose diff changes what one of the module's skills instructs
  an agent to do
When the commit is checked against this feature's rule
Then the type is wrong and the commit is non-conforming, because in a module made of prose
  an instruction is behaviour: the type had to be the one whose level matches what the
  change does to the published surface
```

### AC-2 — A bump that under-states what moved is a defect in the module

```gherkin
Given a module released at a level whose promise is "nothing owed"
When a project that already used it takes the update and one of its config keys, skill
  names, contract keys, invoked script paths, or the instructions one of its skills gives
  no longer holds
Then the module is at fault, not the project — the project owed no reading and no action,
  and the release should have carried the level that obliges one, read through the shift
  that applies below `1.0.0`
```

## Edge cases

### AC-3 — A scope that names no module moves no number

```gherkin
Given a commit typed with a level-bearing type whose scope names an app, a feature under
  the specs root, or the repository itself
When versions are derived from that commit
Then no module's version moves, because none is named — and the absence of a bump is the
  correct outcome rather than a change that went unversioned
```

### AC-4 — A commit naming several modules bumps those, and only those

```gherkin
Given one atomic change across two modules, committed with both named in its scope
When versions are derived
Then exactly those two modules bump, at the same level, and a module that changed only
  because it sits in the same repository does not move
```

### AC-5 — Below `1.0.0`, a breaking change bumps the minor, and the minor obliges

```gherkin
Given a module at `0.4.0` and a commit carrying the breaking signal
When its next version is derived
Then it is `0.5.0` — the mapping shifted by one — and not `1.0.0`, which is a per-module
  decision nothing about this change makes
```

```gherkin
Given a project reading `0.5.0` where it had `0.4.0`, on a module below `1.0.0`
When it decides what it owes
Then it owes what a major obliges — the promise is read one row up below `1.0.0` — and a
  project told it may take that minor without acting has been given the unshifted table
```

### AC-6 — A rename removed before the window closes is refused

```gherkin
Given a module that renamed a published name in release N, both spellings working
When the old spelling is removed in release N+1, or in N itself
Then the removal is refused as premature: the window is two releases, counted, and a
  rename removed inside it is a breaking change wearing a deprecation notice
```

### AC-7 — A deprecation that names no removal version is incomplete

```gherkin
Given a module deprecating a published name in its changelog
When the entry says the name is deprecated without naming the version that removes it
Then the entry is incomplete — a project cannot plan against an adjective, and the window
  is only a window once its end is written down
```

### AC-8 — A project that never updates is told nothing, and that is correct

```gherkin
Given a module that shipped a breaking change, and a project whose marketplace clone and
  installed cache both predate it
When the project runs
Then nothing warns it and nothing breaks, because it never took the change — the notice is
  owed at update and at install, not on a schedule
```

### AC-9 — A skipped release still delivers its notice at install

```gherkin
Given a module that deprecated a name in release N and removed it in release N+2, and a
  project that never took N
When that project installs N+2
Then the changelog it reads at install carries both entries, because it is cumulative —
  the removal is not invisible for having been announced in a release the project skipped
```

### AC-10 — A removed name fails by name at first use, never by default

```gherkin
Given a project whose configuration still uses a published name a module has since removed
When a skill of that module reads it for the first time
Then it fails with a message naming the module, the version that removed the name and the
  replacement — it does not fall back to a default, which would hide the removal until
  something downstream broke for an unrelated-looking reason
```

### AC-11 — Where the changelog and the commit disagree about breakage, the commit decides

```gherkin
Given a change whose specs changelog entry says `Breaking: yes` while no commit behind it
  carries the breaking signal — or the reverse
When the module's version is derived
Then the commit's signal decides the number, and whoever notices the disagreement — the
  reviewer at gate 2, or whoever prepares the release — reconciles the two rather than
  preferring whichever was written later
```

### AC-12 — A change a project must act on carries the breaking signal, whatever its type

```gherkin
Given a commit that renames or removes something on the published surface, or changes what
  a skill instructs in a way a project must adapt to — typed as anything at all
When it is written without `!` on its type and without a `BREAKING CHANGE:` footer
Then it is non-conforming: the signal is owed by the change, not offered by the type, and a
  version derived from a commit that withheld it under-states what the project must do
```

## Out of scope

- **What a commit message must carry, and who may rewrite a branch** — the mandatory type
  and scope, the reference to a work item, the rewriting boundary. Specified by
  `features/business/dev-flow/`, which owns the code cycle; this feature says what the
  type and scope are worth, not that they are written.
- **The GitHub spellings** of a commit's reference and of the single close —
  `features/business/github-tracking/`'s, since neither survives a tracker with no issues.
- **Whether a `release` slot exists**, which module would fill it, and whether the
  derivation is ever automated — open, and deliberately not decided by the ADR behind this
  feature.
- **The changelog file format** — the categories, the required fields, and what the gate
  checks. A commit type proposes a category, and that mapping sits in the same table as the
  type's level; the format itself is `features/business/feature-format/`'s and the modules'
  own, and a module's six categories are not a spec changelog's four.
