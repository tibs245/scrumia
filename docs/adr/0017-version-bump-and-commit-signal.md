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

The promise is about **the module's published surface**:

- the config keys it reads under `settings.<slot>`
- the contract block it writes into `CLAUDE.md`
- the names of the skills and commands it ships, and the scripts other modules invoke by
  path
- **what its skills instruct an agent to do, and the artefacts they produce**

The fourth item is the one a repository of prose cannot leave out. Here the deliverable
*is* the instruction, so a module that rewrites what a skill tells an agent has changed
what a project gets, exactly as surely as one that renames a key — and a surface listing
only names, keys and paths would let it ship under a bump promising nothing moved.

Not about the content of a project's own specs, which the module never owns, and not about
the module's internals, which it may reshape freely.

| Bump | Promise | What the project owes |
|---|---|---|
| **patch** | Nothing on the published surface moved. A defect was fixed or prose was corrected | nothing — take it without reading |
| **minor** | Something is available that was not, or something the project sees changed — and nothing it already does stops working | nothing — read the changelog to learn what moved |
| **major** | Something the project depends on changed shape: a key renamed, a skill removed, a contract's vocabulary changed | act. The changelog names the change and its replacement |

A project that takes a patch or a minor and then breaks has found a defect in the module,
not a consequence it should have anticipated.

**A release is a version published to the marketplace** — a manifest whose number moved,
reachable by a project running `/plugin marketplace update`. Not a commit, not a merge:
several merges can land between two releases, and none of them is one. The windows counted
below are counted in these.

### 2. The signal: `<type>(<scope>): <subject>`

**The scope is mandatory.** This is a house constraint on top of Conventional Commits
v1.0.0, which makes it optional, and it exists for one reason: per-module bumps must be
derivable from history without reading a diff.

The scope is **one token**, from one of four namespaces:

| Namespace | Token | Example |
|---|---|---|
| a module | its plugin name with `scrumia-` dropped | `core`, `teams`, `specs`, `github-project`, `design`, `discovery`, `rules`, `impl-rust`, `impl-solidjs`, `tdd`, `solid-principles`, `tanstack-query` |
| an app | its name in `apps[]` of `.scrumia/config.yaml` | `site`, `tools` |
| a feature | the name of the directory holding its `index.md` | `dev-flow`, `github-tracking`, `release-versioning` |
| everything else | the literal `repo` | `CLAUDE.md`, `.github/`, root `docs/`, root `design/`, the marketplace manifest |

The module column states a **rule** — plugin name, `scrumia-` dropped — and its examples
are today's twelve, not the list. The thirteenth module needs no ADR.

**Feature tokens name the directory that holds an `index.md`, not any directory under the
specs root.** `features/app/site/` and `features/app/tools/` are grouping directories, not
features, so `site` and `tools` stay app tokens and the namespaces do not overlap there.
Within what remains, the four are disjoint today and must stay so: a new feature named
after a module is a naming defect to fix, not a scope to disambiguate. `features/index.md`
belongs to no feature and is scoped with whatever change regenerated it.

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
| `docs` | prose that describes without instructing — a README, a rationale | patch | `Changed` |
| `chore` | tooling, CI, housekeeping — nothing a consumer reads or runs | patch | none |
| `design` | what a user sees changes — a token, a component, a page | **minor** | `Changed` |
| `specs` | a rule under the specs root changes | none — see below | the spec changelog's, not a module's |

Three rules govern the whole table:

- **A bump happens only where the scope names a module.** A commit scoped to an app, a
  feature or `repo` moves no number, whatever its type, because there is no number to
  move. `docs(site):` bumps nothing; `docs(github-project):` bumps a patch. This is what
  makes `specs` a type with no version consequence: a feature carries no version, and a
  spec never lives inside a module.
- **The type is chosen against §1's published surface, not against the files touched.**
  This is what makes the type checkable rather than a mood. A change that adds something a
  project can use is `feat`; one that makes existing behaviour do what it was already meant
  to do is `fix`; `refactor`, `chore` and `docs` are for changes that alter **nothing** a
  consumer reads or runs. The trap in this repository is `docs`: prose that *instructs an
  agent* is the module's behaviour, so editing it is `feat` or `fix`, never `docs`. `docs`
  is for prose that describes without instructing — a README, a rationale, a changelog.
  Where the scope names no module there is no published surface to check against and the
  type is simply descriptive; nothing rides on it, because no number moves.
- **A change to the published surface that a project must act on carries `!`, or a
  `BREAKING CHANGE:` footer, whatever its type.** Not only `feat` and `fix` may carry it,
  and it is **owed**, not offered: this is the sentence that turns §7's "the commit's signal
  is authoritative" into an authority over a signal someone is actually told to send. Its
  absence is why zero of 116 commits have ever emitted one.

`design` sits at **minor** and not at patch because a patch promises a project it may take
the update without reading, and a change to what a user sees is never that. This is the
ticket's option B taken for `design` specifically, at the cost the *Rejected alternatives*
section prices: a stock parser, which ignores the type entirely, computes a lower number
than we do.

The changelog column **proposes** a category; it does not fix one. The entry is a human's
sentence to a consumer, and the type only says which category the change usually lands in.
`Changed`, `Deprecated`, `Removed` and `Security` are in nobody's row for that reason: a
correction to what a skill instructs is typed `fix` and filed under `Changed` as often as
under `Fixed`, and no type implies the other three at all.

The column names **a module's** six categories. A commit changing a rule under the specs
root writes a spec changelog instead, whose four are the specs module's own
(`plugins/scrumia-specs/skills/scrumia-feature/references/catalog.md`) and exclude `Fixed`
— a rule that turns out wrong is a `Changed` there.

**Both `design` and `specs` are admitted, not rejected.** `design` because the repository
ships a design module whose tokens are a consumer's surface, so `design(design):` is a real
and recurring case; `specs` because the specs branch prefix at `docs/dev-flow.md` already
uses it and rejecting it would leave a form in daily use outside every list. The five
`design:` commits on `main` are *not* evidence for either: every one of them touches root
`design/` and `site/assets/`, so under §2 they scope to `repo` and `site` and move no
number under this ADR either. They are what makes the type worth admitting as vocabulary,
not what makes it worth a bump.

**A `specs`-typed commit is scoped to a feature or to `repo`, never to a module** — which
is what keeps `specs(specs):` from being both a bump and no bump. The module token `specs`
and the type `specs` are different words in different positions.

**The same vocabulary serves the branch prefix and the PR title.** One list, three uses.
That is what makes the specs branch prefix conforming rather than an orphan.

### 4. Below `1.0.0`, the mapping shifts by one

Every module is at `0.4.0`, where semver promises nothing. Rather than pretend otherwise
or let a doc rename ship `1.0.0`:

| The mapping says | Below `1.0.0`, the number moves | and the promise a project reads is |
|---|---|---|
| major | minor — `0.4.0` → `0.5.0` | major's: **act** |
| minor | patch | minor's: nothing owed, read what you gained |
| patch | patch | patch's: nothing owed |

**The obligation shifts with the number**, and it shifts one level more severe — not
uniformly, which is why the third column is spelled out rather than summarised. Below
`1.0.0`: a **minor** means act; a **patch** means anything from a fix to a feature, so read
the changelog. That is the whole point of writing the shift down — a project reading the
unshifted table would take a minor "without acting" and break on a rename that shipped
inside it. Below `1.0.0`, a minor is where breakage lives, and the changelog is not
optional reading at either level, because the number alone no longer separates them.

Reaching `1.0.0` is what lifts the shift, and is a decision per module, not a release-wide
event.

### 5. The deprecation window, in releases

A module may rename or remove anything it does not publish. What it publishes — §1's list
— it must keep reading in the old spelling for a stated window:

**Release N** renames. Both spellings work; the module prefers the new one; its changelog
carries the old one under `Deprecated`, **naming the release that removes it** — "removed
no earlier than the second release after this one". The *release* and not the version
number, which at N is unknowable: §7 derives the number from the commits that have not been
written yet. **Removal ships no earlier than release N+2**, so at least one whole release
beyond the rename carries both.

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
| what a bump promises, the bump unit, the `0.x` shift, how a type is chosen and which bump it earns, the deprecation window, the two staleness layers, breakage authority | **new** — `features/business/release-versioning/` |
| every commit carries a type, a scope, and a reference to its work item; `--fixup`'s branch boundary | `features/business/dev-flow/` |
| the reference trailer's spelling, one close in the pull request body, GitHub's closing keywords, closing left to GitHub | `features/business/github-tracking/` |

The type table itself is nobody's spec: it stays here, per the bet priced under *What we
accept*, and both features cite it.

The **replacement test** separates the third row from the first two — it survives a tracker
swap or it does not. It cannot separate the first from the second, since both survive it
word for word; what separates those is ADR-0004's one-unit-of-value criterion, and the
argument for a new feature rather than an amendment of `modular-composition` is that
feature's own out-of-scope bullet: it establishes that a module exists and can be composed,
not how it evolves once adopted.

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
- *A consuming project cannot read this vocabulary.* AC-3's "one definition" puts the list
  here, and a marketplace install cannot follow a repository-relative link out of a plugin
  — so `scrumia-ticket` now names five types to a foreign project where it used to name
  five, and tells it to read its own history instead. The scope's four namespaces were
  inlined in the skill for exactly that reason; the type list was not, because inlining it
  would be the second definition AC-3 forbids. A module that ships a convention its
  consumers cannot read is shipping a convention for this repository only, and that is the
  trade taken.
- *Below `1.0.0` the number says less than it will, and says it one row out.* A feature and
  a fix are the same patch bump until a module reaches `1.0.0`; worse, the level a project
  reads is not the level it owes, so every twelve modules shipping today require the shift
  in §4 to be read alongside the promise in §1. Two tables to hold at once is a real cost,
  and the alternative — leaving the promise table to read false for every module in
  existence — is not one.
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
