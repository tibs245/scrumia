# Modular composition — business rules

## Value

For whoever adopts or extends ScrumIA — a project declaring which modules it runs, and
the modules themselves, written to be pluggable. It brings one flat declaration
(`extends`) a project edits to take exactly the capability it needs, so adopting one
module never requires taking the whole method. It matters because a project that forks
a monolithic method to adapt one part of it stops receiving updates to the rest;
`extends` is what lets the reference answers change without breaking a project's own
choices. Not instrumented today: nothing counts how many projects run with a given
action uncovered versus covered; the composition's shape is read from
`.scrumia/config.yaml`, not aggregated.

## `extends` is a routing mechanism first

An agent is effective when it reads the minimum it needs — but to read little it must
know **where** the essential of its task is. `extends` exists to answer that, across
projects with disjoint contexts served by the same set of modules: a team inside a
large company, a for-profit monorepo, this plugin repository. Extension — a project
customising or adding to a module's behaviour — is a consequence of that routing, not
its object.

## `extends`

A flat list of plugged modules in `.scrumia/config.yaml`, ESLint-shaped, replacing the
former `composition:` key:

```yaml
extends:
  - scrumia-specs
  - scrumia-github-project
  - scrumia-teams
  - scrumia-discovery
  - scrumia-design
apps:
  - name: api
    path: apps/api
    extends: [scrumia-impl-rust, scrumia-practice-tdd, scrumia-practice-solid]
```

**The list is not ordered.** ESLint's own `extends` carries last-wins semantics; this
one does not — arbitration between two modules that could both provide the same
decision (below) is explicit, never positional. Any reader brings the ESLint reflex
uninvited; this rule exists to contradict it on first read.

The project declares its **steps**; **actions** follow from the steps; plugins **bid**
on the actions they provide; `.scrumia/config.yaml` carries only arbitrations and
exclusions — never the full step → action → provider table, which is generated, not
authored.

## Two kinds of action

A **decision** has exactly one provider: who moves a card, which model runs a ticket,
who settles a business rule. `features/business/execution-policy/business.md` § *One
reader, one decision* already states the "one" rule about decisions — this reuses it
rather than restating a second version of it.

A **contribution** legitimately has several: reviewing a PR, applying a practice to a
Build. Three roles reviewing the same PR, two practice modules applying to the same
app's Build, an implementation module per app — all contributions, all already true of
the project before this feature existed. A model that forbade multiple providers on
day one would forbid what already works.

## Three absence states

A given action, for a given step, is in exactly one of three states:

| State | Meaning | Effect on coverage |
|---|---|---|
| **Key absent** | Nobody has decided who covers this | Warned once, counted as a hole |
| `not-applicable` | The step does not exist for this project | Removed from the denominator |
| `human` | The step exists; a person covers it, no tool | Counted as covered |

`not-applicable` is spelled exactly that way — not `NA`, `none`, `null`. Two YAML
parsers already coexist in this project's own tooling (`pick-model.sh`'s
`load_config()` reads with yq if present, else PyYAML), and they disagree on
two-letter uppercase tokens under YAML 1.1 (`NO` reads `False` under PyYAML, the
string `"NO"` under yq) — the exact shape a short absence token risks colliding with.
A fourth spelling of absence, on top of the ones already tracked for `auto_merge`, is
a defect this feature refuses to add.

Without this distinction, a project-wide coverage claim ("N of M steps covered")
answers on an undefined M: a step this project doesn't run and a step nobody has
gotten to yet would count the same, and the claim would be arithmetically false the
day a step that is genuinely invocable-at-any-moment (`status`, `next`, `standup`) gets
counted in the same denominator as an ordered step with a before and an after. Reads
belong to coverage, never to the step denominator.

## Four recipient sets

Coverage is computed against one of four sets an action's caller belongs to, named so
`extends` is never asked to answer for more than the one it configures:

| Set | What it covers | Configured by `extends`? |
|---|---|---|
| **run** | The project's own declared steps | Yes — this is the only one |
| **kernel** | `init`, `compose` — non-configurable by construction | No |
| **adoption** | The five `*-setup` skills, plus the two contract audits | No |
| **authoring** | `rules` — outside the product | No |

A coverage claim that does not name which of these four it measures answers on half
the system and silently drops the rest. `run` is the axis a project configures; the
other three exist so an agent — or a human reading a coverage report — never mistakes
one for the whole.

## Coverage is derived, not declared

A module that bids on an action still **declares** — "I provide this action" is no
less a declaration than "I fill this slot" was. What changes is the grain: coverage is
computed by counting **incoming edges by name** against what was declared, so a
declared action nobody ever reaches from becomes visible as a hole instead of reading
as covered. `scrumia-specs-find`, `scrumia-design-system`, `scrumia-design-sync` and
`scrumia-review` each declare a step and are called by nothing today; `scrumia-brainstorm`
covers Brief while writing no file. Coverage-by-declaration alone would have called all
of them green.

This is only measurable if **a module reaches another by a name the harness resolves,
never by a relative path** — a name greps, a path does not (see BR-4). The resolution
rule's real yield is this measurability, not portability for its own sake.

## `practices` is retired as a named slot

`implementation` and `practices` were always two answers to the same question — how an
app is built — at two granularities, both contributions on that app's Build. `practices`
does not survive as its own key: a practice module is declared through `extends`, per
app, alongside the implementation module:

```yaml
apps:
  - name: api
    path: apps/api
    extends: [scrumia-impl-rust, scrumia-practice-tdd]
  - name: prototype
    path: apps/prototype
    extends: [scrumia-impl-solidjs]
```

TDD applies to `api`, not to `prototype` next to it, because each app's `extends` list
is its own — the per-app axis the former `practices` slot carried is what makes this
declaration and not a single project-wide list.

**The one precedence rule the retired slot carried is unchanged: specific beats
generic.** An implementation module wins over a practice module where they contradict
each other on the same app; a project override
(`.scrumia/impl/<module>.md`, `.scrumia/practices/<module>.md`) beats both. This stays
written in prose — deliberately not encoded as `extends` list order, since the list
carries no positional meaning (see § *`extends`*, above).

Every other rule a practice module owes is unchanged: it refines a named point of the
implementation contract, it works on its own even without an implementation module
present, it ships a reference/audit/refactor skill trio, it documents its settings
under `settings.practices.<module>`.

## What a module owes to be pluggable

Three things, no more:

1. **A `SKILL.md`** — the module's own entry point, and the place it documents its
   contract with the rest of the composition: the settings it reads, the actions it
   bids on, and the one sentence (`CLAUDE.md` line) that tells an agent what it must
   know about the module without opening it. A module with no `SKILL.md` cannot be
   composed — there is nothing for `scrumia-init` to point an agent to.
2. **The actions it provides** — declared from the kernel's closed vocabulary (below),
   never a name the module invents. A module's authority stops at what it declared: it
   does not decide what another module's declared action covers.
3. **The rule that it never assumes another module is present.** If a module needs a
   capability that another module would provide, it checks for it rather than assuming
   it, and if nothing provides it, it names the gap and proposes the next step instead
   of failing outright or guessing a substitute behaviour.

A module that skips any of the three still runs, until the day a project composes it
with a different set of modules than the one it was written against — at which point it
breaks silently, which is the failure this rule exists to prevent.

## The action vocabulary is closed by the kernel

A plugin cannot bid on an action name it does not know — the same constraint
`docs/adr/0016-global-feature-index.md` already imposes on the specs contract: this
exact vocabulary and no other. This bounds the customisation promise: a project chooses
**which steps** it runs and **who covers what**, never **what the actions are called**.
A project or third-party module needing a genuinely new action name is a `scrumia-core`
release, not a config change — a structural ceiling this feature accepts rather than
works around (see `docs/adr/0019-extends-replaces-composition-and-practices.md` §
*What we accept*).

## Distribution is what makes composition cheap

A project adopts a module by declaring it, not by copying it. Two keys in a project's
own `.claude/settings.json` — `extraKnownMarketplaces` and `enabledPlugins` — are
enough; nothing is duplicated into the project repo. This rides on Claude Code's native
plugin marketplace rather than a bespoke installer, because ScrumIA deliberately targets
Claude Code alone (ADR-0001).

All of ScrumIA's own modules live in this one repo, which is also the marketplace
(ADR-0007). A cross-cutting change to the composition — this feature is one — fits in
a single, atomic PR instead of coordinating releases across several repos. A
third-party module remains possible without changing this structure: `marketplace.json`
accepts external sources (`github`, `git-subdir`, `npm`, `archive`) alongside the
relative paths used for ScrumIA's own plugins.

A module may also ship the **standing role** that guards its capability, rather than
that role living in the team module. `scrumia-design` is the first to do so: a design
role in a project with no design system would have nothing to judge but taste. The role
registers in the same `settings.team.roles` list, so routing stays single-sourced — see
[ADR-0014](../../../docs/adr/0014-roles-ship-with-their-capability.md) and the
`agent-team` feature.

## How modules connect to each other

**Through generated documentation, never through dynamic resolution.** `scrumia-init`
reads `.scrumia/config.yaml` and writes, between markers in `CLAUDE.md`, a table naming
which module provides which action and what an agent must know about it before reading
the module itself — now **derived** from declared actions rather than retyped from
named slots, but resolved the same way: once, at composition time, never at call time.
Agents read that table like any other project context.

The rejected alternative is still the capability registry: each module declaring verbs
that a core resolves to whichever module is plugged in. It would decouple modules
completely, at a cost paid on **every** call — the agent holding an indirection in mind
for something that changes a handful of times in a project's life. Documented
composition pays that cost once, at context load, instead (ADR-0009, amended on one
point — what gets derived, not when or where resolution happens — by
[ADR-0019](../../../docs/adr/0019-extends-replaces-composition-and-practices.md)).

The rule that follows: **a module cites another by name in prose**, in its own
`SKILL.md` or `CLAUDE.md` line, never through a runtime lookup — and that name must be
one the harness resolves, never a relative path (§ *Coverage is derived*, above).
Replacing a module means checking the others that name it; that check is a few minutes
of grep, done rarely, not a per-call cost.

## How the composition is reported

A composition an agent retypes is a composition that drifts, and the drift is invisible
because the prose still reads plausibly. So the skills that present the composition —
`scrumia-init` and `scrumia-compose` — end by running `scrumia-core`'s
`scripts/compose-status.sh`, which reads `.scrumia/config.yaml` and prints the derived
coverage itself: which action each declared step's requirement resolves to, and, worded
differently from one another, the steps marked `not-applicable`, the ones covered by a
`human`, and the ones with no declared provider at all. What a human reads is the file,
every time, rather than what one session remembered of it.

This is reporting, not resolution. Nothing calls the script to find out who provides an
action; it resolves nothing on any agent's behalf, and BR-4 stands untouched. It makes
the answer BR-4 already documents legible in a terminal, which is a different job from
looking that answer up at runtime.

It stops there deliberately. It reads the config and only the config, so it cannot tell
whether a module named there is actually enabled, or whether `CLAUDE.md` has gone stale
against it. Those are diagnoses `scrumia-compose` runs and reports around the script's
output — a status printer that guessed at them would be the least trustworthy output in
the composition.

## Business rules

- **BR-1** — An action is a question, not a module. A step's required actions exist
  independently of whether any module currently provides them.
- **BR-2** — An unprovided action is declared, not omitted. `.scrumia/config.yaml`
  reports it as a hole rather than staying silent; a missing report is a tooling
  defect, not "no gap".
- **BR-3** — A module never assumes another module's capability is present. It checks,
  and on finding the capability unprovided, it names the gap in a message a human or an
  agent can act on, and proposes the next step, rather than failing or silently
  changing behaviour.
- **BR-4** — A module cites another by name where the sentence needs the specific one,
  and that name is one the harness resolves, never a relative path. Nothing resolves a
  name to a module at runtime; the resolution is the `CLAUDE.md` table, generated once
  and re-read on every session.
- **BR-5** — ScrumIA's own modules ship from a single repo, which is also the
  marketplace. A third-party module is not required to: it declares its own source in
  `marketplace.json`, at the adopting project's discretion.
- **BR-6** — The composition is reported by reading `.scrumia/config.yaml`, never from
  memory. A skill that presents the composition closes by running the kernel's status
  script and does not paraphrase the table it prints. Reporting the composition is not
  resolving it: BR-4 still forbids resolving a name to a module at runtime.
- **BR-7** — A decision action has exactly one provider; a contribution action may have
  several. A module that bids on a decision action already provided by another module
  is a conflict named at composition time, not silently arbitrated by list order —
  `extends` carries no order to arbitrate by.
- **BR-8** — Coverage is computed against exactly one of the four recipient sets (run,
  kernel, adoption, authoring) at a time, and a coverage claim states which. `extends`
  configures `run` only; the other three exist so a claim never silently answers for
  half the system while presenting itself as the whole.

## Vocabulary

**"Slot" names the question a project answers when composing** — it survives as the
word the human-facing composer uses to ask "which module fills this need", because
that is what a person actually answers, one question at a time. **"Action" names the
mechanism's own unit** — what a module declares providing, what coverage is computed
against, what `extends` ultimately resolves to underneath the composer's questions. The
composer keeps asking questions shaped like slots; the config and the generated
`CLAUDE.md` table beneath it speak in actions. Using "slot" for the mechanism's unit or
"action" for what the composer asks a visitor is the drift this section exists to
prevent — write the one the sentence is actually about.

"Area" appears nowhere in this composition's vocabulary as a synonym for either word:
it reads as a section heading and loses what both "slot" and "action" carry — a
question, or a unit of work, that exists whether or not anything currently answers it.
