# scrumia-specs

The specs slot: one feature, one directory, a catalog of **angles** instead of a fixed
template — `qa.md` is TDD-central, its acceptance criteria written before the code that
satisfies them. Its own contract is written verbatim into a consuming project's
`CLAUDE.md` by `scrumia-init`, so every other skill reads the contract there rather than
this module's file names directly.

An angle is one way of interrogating a feature, and it ships three things: the questions
that explore it and what activates it, the template to fill, and the guard-rails a
reviewer runs against the result. Eleven of them, four mandatory.

## What it answers

Where a rule lives before it becomes code, and how to find it again without reading the
whole tree: which file in a feature answers which question, and the minimum context a
ticket or a review actually needs.

## What it refuses

- No fixed template. A feature carries only the files its activated angles demand —
  `index.md`, `qa.md`, `CHANGELOG.md` and `business.md` are the only mandatory four.
- No judgment left implicit. Whether a content-tested angle applies is decided by that
  angle's closed questions, each with the answer to take when unsure — and what was
  declined is reported, because an absence nobody can see was considered asserts nothing.
- No invented link vocabulary. An index's `Links` section uses nine fixed keys; four of
  them are structural and validated on both sides.
- No history inside a spec. A spec states current truth; what it used to say lives in git
  and the changelog, never narrated in the file itself.
- No loading the whole `features/` tree to answer one question. `scrumia-specs-find`
  exists so a ticket or a review reads the minimum instead.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-feature` | Creates, updates or audits one feature — the angle catalog, not a fixed template. Ships eleven angles, each with its questions, template and checklist. |
| `scrumia-specs-find` | Finds the feature that owns a rule, traces dependencies between features, or loads the minimal context a ticket needs. |
| `scrumia-specs-setup` | Installs the `features/business` and `features/app/<app>` tree, and hands `scrumia-init` this module's composition line. |
| `/feature` | Slash command — loads `scrumia-feature` and passes its argument through. |

## Settings it reads

Under `settings.specs` in `.scrumia/config.yaml`: `root` and `strates`, read once by
`scrumia-specs-setup` at install time — no other skill in this module reads them back.

Under this module's own `params.angles`: one key per content-tested angle, valued
`always`, `context` (the default) or `never`. It overrides that angle's activation
questions for the whole project; the mandatory four ignore it.

## What it expects to find

Specs living in-repo, next to the code, not in a separate repository. A global index at
the root of `specs_root` — `scrumia-specs-find` falls back to walking the tree and reports
the gap if it is missing.
