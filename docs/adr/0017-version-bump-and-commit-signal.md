# ADR-0017 — What a version bump promises, and the commit signal it derives from

**Status**: accepted — 2026-08-10
**Supersedes**: one accepted cost of [0001](0001-distribution-as-plugins.md) — see *Relation to 0001*

## Context

Twelve modules ship from this repository. All twelve are at `0.4.0`, and nothing anywhere
says what moving that number would promise a project that has already adopted one. In
parallel, commits carry a type and nothing defines the vocabulary they draw it from: the
only list in the repository sits inside a consumer, `scrumia-ticket`'s SKILL.md, where it
serves branch names, and it omits a type the repository uses.

These are one question, not two. Under Conventional Commits a bump is *derived* from the
type and the scope, so fixing the semver promise while the signal it reads is undefined
decides half a rule — and deciding what `design:` is worth without knowing what a version
counts decides the other half in the dark.

Measured on `origin/main` at HEAD, **116 commits**:

| Fact | Count |
|---|---|
| Carrying a conventional type prefix | 110 — 38 `docs:`, 36 `fix:`, 24 `feat:`, 5 `design:`, 5 `chore:`, 2 `refactor:` |
| Carrying **no** prefix | 6 |
| Carrying a scope, `type(scope):` | **0** |
| Carrying `!` or a `BREAKING CHANGE:` footer | **0** |
| Carrying a `Refs:` trailer | 7 |
| Carrying `Closes/Fixes/Resolves #<n>` **in the commit message** | 44 |

Two facts follow from that table. The breaking signal has never been emitted, so nothing
in history tells a consumer that anything broke; and the lookup path from a ticket to its
commits does not exist. `git log --grep '#59'` returns five commits — one of the four that
PR #77 delivered, and four belonging to other tickets. Recall 25%, precision 20%, on a
lookup that reads as complete.

### What is already decided, and is not reopened

- **The unit that bumps is the module** (#129, human decision). A version number promises
  that *this module* changed, not that the repository published. Lockstep was rejected:
  a project pinning `scrumia-specs` would take a bump caused by `scrumia-impl-rust`.
- **Conventional Commits v1.0.0 is the adopted standard.** This ADR cites it rather than
  inventing a house list, and states every place it adds a constraint on top.
- **Migration is forward-only.** Counters start where they stand; the commits already on
  `main` are never re-attributed. A convention that ships wrong is wrong for every commit
  written under it, and no later pass repairs them.

## Decision

### 1. What a bump promises a project already using the module

The promise is about **the module's published surface** — the config keys it reads under
`settings.<slot>`, the contract block it writes into `CLAUDE.md`, the names of the skills
and commands it ships, the scripts other modules invoke by path. Not about the content of
a project's own specs, which the module never owns.

| Bump | Promise | What the project owes |
|---|---|---|
| **patch** | Nothing on the published surface moved. A defect was fixed or prose was corrected | nothing — take it without reading |
| **minor** | Something is available that was not, and nothing the project already does stops working | nothing — read the changelog to learn what you gained |
| **major** | Something the project depends on changed shape: a key renamed, a skill removed, a contract's vocabulary changed | act. The changelog names the change and its replacement |

A project that takes a patch or a minor and then breaks has found a defect in the module,
not a consequence it should have anticipated.

### 2. The signal: `<type>(<scope>): <subject>`

**The scope is mandatory.** This is a house constraint on top of Conventional Commits
v1.0.0, which makes it optional, and it exists for one reason: per-module bumps must be
derivable from history without reading a diff.

The scope is **one token**, from one of four namespaces:

| Namespace | Token | Example |
|---|---|---|
| a module | its plugin name with `scrumia-` dropped | `core`, `teams`, `specs`, `github-project`, `design`, `discovery`, `rules`, `impl-rust`, `impl-solidjs`, `practice-tdd`, `practice-solid`, `practice-tanstack-query` |
| an app | its name in `apps[]` of `.scrumia/config.yaml` | `site`, `tools` |
| a feature | its directory name under the specs root | `dev-flow`, `github-tracking`, `release-versioning` |
| everything else | the literal `repo` | `CLAUDE.md`, `.github/`, root `docs/`, the marketplace manifest |

The four namespaces are disjoint today and must stay so. A new feature named after a
module is a naming defect to fix, not a scope to disambiguate.

**A commit touching several modules is split into one commit per module.** Where the
change is genuinely atomic across them — the two sides of one contract, which cannot be
delivered by halves — the scope carries them comma-separated (`feat(specs,core): …`) and
**every module it names bumps, at the same level and no other**. Nothing but that case may
carry more than one token. This is what #129's counter-example demands: `821e19c`, a
single `fix:`, produced a minor across twelve modules, eight of which changed only their
own version line.

### 3. The type vocabulary, its version consequence, and its changelog category

**This table is the vocabulary's one definition.** Every other surface — `scrumia-ticket`'s
branch and PR steps, `CLAUDE.md`, the specs — cites it and enumerates nothing.

| Type | Means | Version consequence | Changelog category |
|---|---|---|---|
| `feat` | a capability the module did not have | **minor** | `Added` |
| `fix` | a defect in behaviour that already existed | **patch** | `Fixed` |
| `refactor` | shape changed, behaviour did not | patch | `Changed` |
| `docs` | prose a consumer reads | patch | `Changed` |
| `chore` | tooling, CI, housekeeping | patch | none, normally |
| `design` | what a user sees changes — a token, a component, a page | patch | `Changed` |
| `specs` | a rule under the specs root changes | none — see below | the spec changelog's, not a module's |

Two rules govern the whole table:

- **`!` on the type, or a `BREAKING CHANGE:` footer, overrides the row and bumps a major.**
  Available on every type, not only `feat` and `fix`.
- **A bump happens only where the scope names a module.** A commit scoped to an app, a
  feature or `repo` moves no number, whatever its type, because there is no number to
  move. `docs(site):` bumps nothing; `docs(github-project):` bumps a patch. This is what
  makes `specs` a type with no version consequence: a feature carries no version, and a
  spec never lives inside a module.

**`design` and `specs` are admitted, not rejected.** `design` because five commits on
`main` already use it for user-visible change and the repository ships a design module
whose tokens are a consumer's surface; `specs` because the specs branch prefix at
`docs/dev-flow.md` already uses it and rejecting it would leave a form in daily use
outside every list.

**The same vocabulary serves the branch prefix and the PR title.** One list, three uses.
That is what makes the specs branch prefix conforming rather than an orphan.

`Deprecated`, `Removed` and `Security` are nobody's type. No commit type implies them, and
they stay what a human writes when they judge a change deserves one.

### 4. Below `1.0.0`, the mapping shifts by one

Every module is at `0.4.0`, where semver promises nothing. Rather than pretend otherwise
or let a doc rename ship `1.0.0`:

| The mapping says | Below `1.0.0`, it is |
|---|---|
| major | minor — `0.4.0` → `0.5.0` |
| minor | patch |
| patch | patch |

Reaching `1.0.0` is what lifts the shift, and is a decision per module, not a release-wide
event.

### 5. The deprecation window, in releases

A module may rename or remove anything it does not publish. What it publishes — §1's list
— it must keep reading in the old spelling for a stated window:

**Release N** renames. Both spellings work; the module prefers the new one; its changelog
carries the old one under `Deprecated`, **naming the version that removes it**.
**Removal ships no earlier than release N+2** — so at least one whole release beyond the
rename carries both.

Not "for a while", not "until the next major": two releases, counted.

### 6. When a project finds out, across both staleness layers

Two independent lags, and refreshing one does not refresh the other:

| Layer | What is stale | When the project finds out |
|---|---|---|
| the marketplace clone behind the repo | `/plugin marketplace update` has not run | **at update.** Nothing polls, and nothing should: a project that never updates is never broken by a change it never took. What it reads at that moment is the module's changelog |
| the installed cache behind the clone | the plugin runs from an older clone | **at install.** `/plugin install` replaces the cache, and the same changelog is the notice |

And a third moment, which is the one that catches a project that skipped a release:
**at first use**, a skill reading a published name the module has since renamed **fails
with a named message** — the module, the version that removed it, the replacement —
rather than falling back to a default. Silent degradation is what makes the second layer
invisible, and `features/business/modular-composition/` already requires a named message
for the analogous absent-module case.

**"Never" is refused as an answer for a major.** A breaking change a project can take
without ever being told is exactly the failure this ADR answers. Reading the changelog is
a step of taking the update, not a courtesy.

Worked on the example the criteria name — a module renames `settings.tracker.board.flow`
to `settings.tracker.flow`. Release N reads both and deprecates the old, naming `N+2`.
A project updating at N sees it in the changelog it reads to take the update. A project
that never updates sees nothing and breaks on nothing. A project that skips N and installs
N+2 still reads the removal at install, because the changelog is cumulative — and if it
missed that too, its first run names the missing key and the version that removed it
instead of quietly using a default.

### 7. Which assertion of breakage is authoritative

**The commit's `!` or `BREAKING CHANGE:` footer.** The version is derived from history, so
the signal that moves the number must be the one *in* history; a line typed into a
changelog cannot be it.

The specs changelog's `Breaking:` field is not a competitor. It describes a different
object — a rule under the specs root, which carries no version at all — and answers a
different reader. Where one change touches both a module and a spec, both are written and
they must agree about the same change: a `Breaking: yes` with no `!` behind it, or a `!`
with no entry, is a defect to reconcile, not a second authority to weigh.

### 8. The commit's reference to its ticket, and the single close

Two different jobs, and conflating them is what produced the 25%-recall lookup above.

- **Every commit of a branch carries a reference to its work item.** Redundant is fine;
  incomplete is not. A lookup returning some of a ticket's commits is worse than one
  returning none, because it reads complete.
- **Exactly one closing keyword, in the pull request body.** GitHub performs the close;
  no skill calls `gh issue close` for a ticket a pull request delivers.

**GitHub acts on a closing keyword wherever it appears** — a commit message reaching the
default branch closes just as a pull request body does. That is why repeating it per
commit is a defect rather than harmless redundancy: several artefacts each claim the
close, which one performed it stops being answerable, and a commit cherry-picked or merged
outside its pull request closes a ticket its change does not deliver. Conversely a
reference trailer closes nothing, and must not be written as though it might.

The GitHub spellings of both are `features/business/github-tracking/`'s to state; the
abstract rule — one reference per commit, one close per change — is
`features/business/dev-flow/`'s.

### 9. `git commit --fixup` with `rebase --autosquash`

**Blessed on epic and ticket branches. Banned on the default branch** (human ruling,
2026-08-09). Who may run it: the executor that owns the branch, and only it.

The cost is stated rather than assumed: autosquash rewrites commits that are already
pushed and needs a force push to land. During a sprint, several worktrees share one `.git`
and a sibling may already have fetched the branch — so a force push on anything a sibling
reads destroys work that was committed precisely so it could not be lost. The branch
boundary is what keeps that contained.

### Where these rules live

By the replacement test in `features/business/dev-flow/business.md` — restate the rule for
a tracker with no pull request and no board, and see whether it survives:

| Rule | Feature |
|---|---|
| what a bump promises, the bump unit, the `0.x` shift, type → bump, the scope alphabet, the deprecation window, the two staleness layers, breakage authority | **new** — `features/business/release-versioning/` |
| every commit carries a type, a scope, and a reference to its work item; `--fixup`'s branch boundary | `features/business/dev-flow/` |
| the reference trailer's spelling, one close in the pull request body, GitHub's closing keywords, closing left to GitHub | `features/business/github-tracking/` |

The versioning half gets its own feature rather than joining `modular-composition`,
because that feature's own out-of-scope bullet already argues the split: it establishes
that a module exists and can be composed, not how it evolves once adopted.

### Relation to 0001

[ADR-0001](0001-distribution-as-plugins.md) accepted, as a cost: *"Versioning is coarser
than per-module npm semver. We pin by tag and by commit, which is enough."* That is no
longer true. #129 made the module the unit that bumps, and this ADR gives the number a
promise a tag cannot carry.

This ADR **supersedes that clause and only that clause**. 0001's decision — distribution
as native Claude Code plugins — stands, and 0001 is not modified, per `README.md`. Pinning
by tag and by commit remains available and remains what a project pinning the marketplace
does; what changed is that it is no longer *enough*.

### Boundary with the release module

This ADR decides what a version promises and what signal moves it. It **does not decide
whether a `release` slot exists**, which module would fill it, or whether the derivation is
ever automated. That decision is #86's and is left open here on purpose.

Today nothing derives anything: **the convention ships documented and gated by nothing.**
No `tools/validate.py` check reads a commit message. That asymmetry with the changelog
gate, which does gate, is deliberate and named here rather than discovered later.

## Consequences

**What we gain**

- A version number answers a question. A project reading `0.5.0` where it had `0.4.2`
  knows it owes an action, and reading `0.4.2` where it had `0.4.1` knows it owes none —
  without opening a diff.
- The bump is computable from history alone. The scope names the module, the type names
  the level; nothing has to be inferred from which files a commit happened to touch,
  which is the inference that produced twelve bumps for one change.
- One vocabulary for three surfaces — commit type, branch prefix, pull request title —
  defined once, so the next disagreement between them is impossible rather than merely
  unlikely.
- A ticket's commits become findable. One reference per commit is the lookup path that
  today returns one commit in four.

**What we accept**

- *The vocabulary is frozen in a document that is never modified.* The branch not taken
  was to let a spec carry the live list, the way `features/business/execution-policy/`
  carries the scope axis: cheaper to extend, and wrong here, because a version derivation
  has to read a list that cannot quietly change under a number already published.
  Admitting a ninth type therefore takes a superseding ADR — deliberate, but it makes a
  small change expensive, and the tempting shortcut is to mistype a commit rather than
  open one.
- *Our number and an off-the-shelf tool's disagree.* A stock Conventional Commits parser
  computes from `feat`, `fix` and `!` alone and ignores `docs`, `chore`, `design` and
  `refactor`; here those bump a patch when they name a module. Anyone deriving a version
  must use this rule, not a stock parser — and the `0.x` shift in §4 is a second
  divergence in the same direction.
- *The mandatory scope is a constraint on a standard that makes it optional.* Muscle
  memory writes `feat: …`, and nothing rejects it today.
- *Zero of 116 commits conform, and none will be repaired.* Every count in the Context is
  measured on history written before this rule. `git log --grep` stays unreliable for
  every ticket delivered before it; the first fully conforming ticket is the one that
  lands this ADR.
- *The convention ships unenforced.* Stated here rather than found later. Until a gate
  exists, conformance is a habit.
- *Below `1.0.0` the number says less than it will.* A feature and a fix are the same
  patch bump until a module reaches `1.0.0`, so a consumer below it reads the changelog
  for anything finer than "something moved".
- *A fifth business feature about process joins the specs root.* `release-versioning` sits
  beside `dev-flow`, `github-tracking`, `execution-policy` and `ceremonies`, and a reader
  filing a process rule now has one more door to try. The replacement test and each
  feature's Links section are what keep that answerable.

## Rejected alternatives

**Types outside `feat`/`fix`/`!` bump nothing.** Cleanest against the standard and
cheapest to tool. Rejected because a module's content can then change with its number
frozen: the five `design:` commits on `main` would have shipped under no release note, and
a consumer comparing `0.4.0` to `0.4.0` correctly concludes nothing changed when something
did. That staleness is silent, and silence is the failure mode this ADR exists to answer.

**Rejecting `design:` and `specs:` as types**, folding them into `feat`/`fix` and `docs`.
Rejected: it discards expressiveness already in use — five commits and a branch prefix —
and, under forward-only migration, converts them into permanently non-conforming history
that nothing repairs. Admitting a type in use costs a table row; rejecting one costs a
permanent exception.

**Lockstep versioning**, one number for the repository. Already rejected by #129 and not
reopened here: a project pinning one module would take bumps caused by every other.

**Enforcing the convention with a `tools/validate.py` gate now.** Rejected for scope, and
named rather than left as a silent omission: a gate must either reject the 116 commits
already on `main` or carry a cutoff date, and that choice belongs to the ticket that has
the hook in front of it (#87, #86).

**Leaving versioning in `modular-composition`.** Rejected on that feature's own argument:
it establishes that a module exists and can be composed, not how it evolves once adopted.
Folding evolution back in would put two units of value in one feature, against ADR-0004.
