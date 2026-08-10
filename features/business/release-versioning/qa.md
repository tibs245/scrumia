# Acceptance criteria — release-versioning

One scenario per rule in `business.md`. Each scenario must be able to fail. These are
read from a module's manifest, its changelog and the commits behind it — not from
application code, since nothing computes a version today.

## Nominal

### AC-1 — The bump is read off the commit, not chosen

```gherkin
Given a commit whose type carries a level and whose scope names a module
When the module's next version is decided
Then it is the level that type maps to in the vocabulary's one definition, and the
  person shipping it did not pick a level from an impression of how big the change felt
```

### AC-2 — A patch that moves the published surface is a defect in the module

```gherkin
Given a module released as a patch
When a project that already used it takes the update and one of its config keys, skill
  names, contract keys or invoked script paths no longer works
Then the module is at fault, not the project — the project owed no reading and no action,
  and the release should have been a major
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

### AC-5 — Below `1.0.0`, a breaking change bumps the minor

```gherkin
Given a module at `0.4.0` and a commit carrying the breaking signal
When its next version is derived
Then it is `0.5.0` — the mapping shifted by one — and not `1.0.0`, which is a per-module
  decision nothing about this change makes
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
Then the commit's signal decides the number, and the disagreement is reported as a defect
  to reconcile rather than resolved by preferring whichever was written later
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
  checks. This feature names which category a type proposes; the format is
  `features/business/feature-format/`'s and the modules' own.
