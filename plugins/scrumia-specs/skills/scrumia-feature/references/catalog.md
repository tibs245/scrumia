# Catalog of feature angles

An **angle** is one way of interrogating a feature. Each angle owns one file, and
ships three things in `angles/<angle>/`:

| File | What it is for |
|---|---|
| `context.md` | what the angle answers, when it activates, the questions that explore it, its boundary |
| `template.md` | the file to copy and fill |
| `checklist.md` | the review guard-rails — the defects this angle actually produces |

Read the `context.md` of an angle before writing its file, and its `checklist.md`
before calling it done. Nothing else in this catalog restates what an angle's own
directory says.

## The angles

| Angle | File | Stratum | Activates |
|---|---|---|---|
| [`index`](angles/index/context.md) | `index.md` | both | always — written **last** |
| [`business`](angles/business/context.md) | `business.md` | both | always |
| [`qa`](angles/qa/context.md) | `qa.md` | both | always |
| [`changelog`](angles/changelog/context.md) | `CHANGELOG.md` | both | always |
| [`ux`](angles/ux/context.md) | `ux.md` | App | a person looks at what this produces |
| [`tech`](angles/tech/context.md) | `tech.md` | App | a choice the code cannot explain itself |
| [`api-contract`](angles/api-contract/context.md) | `api-contract.md` | both | something outside the feature parses it |
| [`archi`](angles/archi/context.md) | `archi.md` | Business | the EPIC touches ≥2 apps |
| [`legal`](angles/legal/context.md) | `legal.md` | both | personal data, payment, user content, minors, regulated sector, named legal risk |
| [`security`](angles/security/context.md) | `security.md` | both | a meaningful risk surface on any of four axes |
| [`devx`](angles/devx/context.md) | `devx.md` | App | it exposes something others consume |

The "Activates" column is a reminder, not the rule. Each angle's `context.md`
carries the closed questions that decide, with the default answer when unsure —
that is what a writer applies.

## The two existence categories

**Mandatory in every feature** — `index.md`, `qa.md`, `CHANGELOG.md`,
`business.md`. A feature has to be findable, has to be possible to follow over
time, has to be possible to test — and has to be worth building: every feature
states its value, so `business.md` exists at both strata. Their absence asserts
nothing; it is a gap.

**Content-tested** — everything else. A file is created only when it has content;
its absence is the assertion "nothing to say on this subject", not an oversight and
not a placeholder. This is what lets an agent decide what to read without reading
everything.

These categories are **this module's** declaration, not a property of the format as
such: whichever module fills the `specs` slot declares its own set, and this file is
where `scrumia-specs` declares its own. Do not read the set out of `CLAUDE.md`'s
`## Specs contract` block instead — that block names the files a module uses so
consumers need not hard-code them, and marks none of them required
(`docs/adr/0012-specs-contract.md`).

## Switching an angle on or off by configuration

A content-tested angle answers to its own questions by default. A project can
override that under this module's `params` in `.scrumia/config.yaml`:

```yaml
modules:
  "<source>:scrumia-specs":
    params:
      angles:
        security: always
        legal: always
        devx: never
```

| Value | Effect |
|---|---|
| `always` | the file is written in every feature, questions or not — a feature with nothing to state says so explicitly, with a date, rather than leaving the file empty |
| `context` | the default, and the behaviour when the key is absent: the angle's own questions decide |
| `never` | the angle is off; the file is not written, and its absence asserts nothing |

The four mandatory angles ignore this key. A project that wants features without a
value statement or without criteria wants a different specs module, not a setting.

Read the effective value through `scrumia-extends --settings`, never out of the
file: that is the one call that applies all three configuration layers.

## Disposition on disk

Two dispositions exist, and picking the wrong one is not cosmetic — it decides
whether a reader finds the second feature at all.

```
features/
  business/
    <feature>/                 a Business feature
      <child>/                 a child feature — one answer to the question the parent poses
  app/
    <app>/
      <feature>/               an App feature
        <child>/               same rule, same stratum
```

**Nest** when the parent states what any answer to its question is held to, and the
child is one such answer. The parent keeps its own value, rules and criteria; the
child states only what is specific to being *this* answer, and restates none of the
general rules.

**Place side by side** — two directories at the same level — in every other case:
two features that depend on each other, that share a subject, or that one merely
mentions. Dependency is a `Consumes:` link, not a directory.

The decisive test, in this order:

1. Would the parent still be true and worth reading if the child were deleted?
   **No → they are one feature**, not two.
2. Does the child mean anything without the parent? **Yes → they are siblings**,
   linked but not nested.
3. Does the parent constrain the child, rather than depend on it? **Yes → nest.**

Three constraints travel with nesting:

- **A parent is a full feature.** It carries its four mandatory files with content
  of its own. A directory that exists only to group children is not a feature, and
  this format has no grouping directory — flatten it. The same holds at every
  level: a node at any depth is either a feature or it does not exist.
- **Bounded by structure, not by a number.** A child of a child is legitimate when
  every node in the chain is a feature in its own right, the relationship is
  declared on both sides, and each level expresses a constraint the level above
  does not. A directory with no content of its own is a grouping directory
  regardless of its depth — flatten it. The depth at which a feature sits does
  not, by itself, make the nesting wrong.
- **Both sides declare it.** The parent carries `Children:`, the child carries
  `Parent:`. A child's stratum is its parent's; a child of a Business feature is a
  Business feature.

A child feature is a leaf of the tree like any other: it appears in the global
index on its own line, and its own `index.md` is what a reader lands on.

## No ticket in a spec

A spec cites no issue and no PR. Tracker state lives in the tracker; a spec that
carries a ticket number is caching state that goes stale the day the ticket closes —
fourteen stale references were measured across twelve indexes before this rule.
**`CHANGELOG.md` is the one exception**: history's job is to point at the tickets
that carry the why. Everywhere else, state the fact or the open question in words —
"not automated today", "who counts, and at what threshold, is open" — and let the
tracker be searched for the ticket that tracks it. `tools/validate.py` enforces this.

## The membership tests

Four boundaries carry most of the collisions. Each has one test, stated here once
and cited — never restated — by the angles it separates.

- **business vs ux, on the journey.** A step stated as actor intent and the value
  delivered, naming no screen, no control, no click path → `business.md`. The moment
  it names one → `ux.md`. Same journey, two altitudes: `business.md` says why the
  steps exist, `ux.md` says what the user sees at each one.
- **tech vs archi, on data flow.** Flow that never leaves the app's own boundary →
  `tech.md`. Flow that crosses apps, scoped to an EPIC → `archi.md`.
- **business vs tech, on mechanisms.** A rule that constrains what the product
  promises — whatever tool enacts it — → `business.md`. How a tool, command or flag
  achieves it, and what happens when it is misused → `tech.md`. "Reads are filtered
  or they lie" is business; the flag that does the filtering is tech.
- **ux vs qa, on accessibility.** A property the journey must have, stated in prose
  ("this control is reachable by keyboard") → `ux.md`. Anything testable against a
  named technical criterion (a contrast ratio, a keyboard-trap check, an
  announcement) → a tagged `qa.md` criterion. Identity-level rules (contrast
  minimums, the accent hue-distance rule) live in `design/` and are cited, never
  restated.

## The worked examples

Two real features, kept conformant with this catalog and its templates, serve as the
copy source: `features/business/github-tracking/` for the Business stratum,
`features/app/site/hero/` for the App stratum. For the nested disposition,
`features/business/work-item-format/` and its child `standard/`. When this catalog
and an example disagree, the catalog is right and the example has drifted — file it
as a finding.

## Extending the catalog

The catalog is open. `perf.md`, `i18n.md`, `analytics.md` are legitimate additions.

Three rules to keep it from sprawling:

1. **A new angle must have a distinct reader.** If the same people already read
   another file of the feature, it is a section, not an angle.
2. **It ships the full directory** — `context.md`, `template.md`, `checklist.md`.
   An angle with no checklist is an angle nobody can review; an angle with no
   activation questions is one every writer decides differently.
3. **It is listed in the table above**, and in the contract's `catalog:` key.
   Otherwise the next feature will invent another name for the same thing, and the
   catalog will lose the only thing that makes it useful: its predictability.

## Where a format rule is restated

A rule about the feature format lives here first, but it is restated at other sites — a
sweep that stops at the obvious ones leaves a retired rule live somewhere an agent still
runs it. Five of the six ship with this module; the sixth ships with `scrumia-discovery`
and applies only where that module is installed. Ordered by how much damage a stale copy
does:

1. `scrumia-specs-setup/SKILL.md` Step 3 — the composition line handed to `scrumia-init`
   for a **consumer project's** `CLAUDE.md`. Always loaded, and the only statement of the
   rule a project gets without opening this file.
2. `scrumia-specs/commands/feature.md` — restates the rule as an instruction; the front
   door for `/feature`.
3. `scrumia-feature/SKILL.md` — the procedure, the angle table, and "Updating an
   existing feature"'s step on deleting a file that became meaningless, which a
   mandatory-file rule must carve out of.
4. `angles/<angle>/template.md` — the note in the template of the angle concerned;
   `angles/index/template.md` carries the one under the "Files present" sample table.
5. [`../docs/format-feature.md`](../docs/format-feature.md) — the **why**, ships beside
   this catalog so it stays the version of the module a project actually has installed.
6. `scrumia-discovery/skills/scrumia-split/SKILL.md` Step 2 — enumerates which files to
   create for a new feature, in contract-key terms. A consumer in another module, easy to
   miss, and the place a mandatory-file rule gets silently re-derived.

Grep the rule's **phrasing** across these, not the file list — the wording differs by
site, and a rename here doesn't announce itself anywhere else.

This repository additionally restates the rule at two sites of its own, neither shipped
to a consumer project: `docs/architecture.md`, in prose, and
`site/i18n/{en,fr}/modules/scrumia-specs.json` (`refusals`, `philosophy`), for
`site/**/modules/*.html` — **generated** from that JSON by `tools/build_site.py`, edit
and rebuild both languages. Sweep these two in addition to the six above, but only when
working in this repository itself.
