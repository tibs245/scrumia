# Session mods

**Status**: draft

## In brief

What a session mod is and what each one promises the person driving a session. A session
mod is a Claude Code mod — function hooks, not a skill module — that changes what a
long session shows or does while it runs: a place for the model to park what is the
person's to decide, a view of the tracker, a view of the roadmap. This feature holds one
section per mod, so that each is specified in the same place and a new one adds a section
without touching another's. Today one is written, the questions inbox; the two others
hold a placeholder until their own specification lands.

## Links

- Implemented by: no App feature. Each mod is a plugin under `plugins/`; the questions
  inbox is `plugins/scrumia-questions/`.
- Defers to: `features/business/module-anatomy/` for the shape of the module that ships a
  mod and for what its manifest may carry.
- Defers to: `features/business/release-versioning/` for what a change to a mod costs a
  project that adopted it.
- Authority: `docs/adr/0026-session-mods-are-plugins-of-their-own.md` — where a session
  mod lives.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding what a session mod is, or what the questions inbox promises: the shape of a question, how an answer is given and returned, what it refuses |
| `qa.md` | Checking the acceptance criteria of a mod, each mapped to the test that proves it |
| `CHANGELOG.md` | History of changes to this spec |

No `archi.md`: a session mod touches no second app, and where it lives is an ADR, not a
feature file. No `ux.md`: the pane's layout is described by the plugin's README and
re-read against the running mod, not frozen here. No `legal.md`, `security.md`: the
inbox stores the person's own answers on their own machine and reads nothing outside the
session. No `api-contract.md`, `tech.md`, `devx.md`: the public contract of a mod is its
README's, a plugin's own.
