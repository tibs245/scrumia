# Changelog format

Two kinds of thing in this repository keep a changelog, and they answer to different
readers. Both take [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/); only
one of them takes its versions.

| | `features/*/CHANGELOG.md` | `plugins/*/CHANGELOG.md` |
|---|---|---|
| Reader | someone working on the spec | someone deciding whether to take the version |
| Versions | none — a spec is never released | one section per version |
| Categories | four | all six |
| Stated in | [`scrumia-feature`'s catalog](../plugins/scrumia-specs/skills/scrumia-feature/references/catalog.md) | here |

The spec half is the specs module's own business, and its catalog is the authority on it.
This file states the plugin half, and the one rule both share.

## The rule both share — a human writes the entry

The commit says what was done. The entry says what it means for whoever reads it. Those
are different sentences, and only the second is a changelog.

So **entries are never generated from the commit log**, however good the commit convention
gets. Keep a Changelog names this as the practice it exists to replace: a commit log is a
list of every change, noise included, ordered for the person who made them. A changelog is
a short list of the ones that matter, written for the person deciding whether to take
them.

Conventional Commits still earns its place on the other side of the boundary: the commit
type decides the **version bump** and suggests the category. It does not write the line.

## The plugin half

One file per module, `plugins/<module>/CHANGELOG.md`:

```markdown
# Changelog — scrumia-specs

## [Unreleased]

## [0.4.0] - 2026-08-10
### Added
- ...
### Changed
- ...
```

Six categories, Keep a Changelog's own: `Added`, `Changed`, `Deprecated`, `Removed`,
`Fixed`, `Security`. `Deprecated` carries the most weight here — it is how a consumer
learns a config key is going away *before* it does, which is the only warning a version
number cannot give.

**A `Deprecated` entry names the release that removes the deprecated name** — the release,
not a version number, which is not yet derivable at the release that deprecates. That
release is not the module's to pick freely: `features/business/release-versioning/` owns
the window itself; this file only says the entry must name where it ends.

**Versions move per module.** A number here promises that *this* module changed, not that
the repository published — a project pinning one module should never take a bump caused by
another it does not use.

**`plugin.json` is the single authority on a module's version.** `marketplace.json` and
the changelog's newest section cite it. Where two files disagree, `plugin.json` is right
and the other is the one to fix.

`marketplace.json` also carries a top-level `version`. It numbers **the marketplace
listing itself**, not any module in it, and no module is expected to match it — that
expectation was the lockstep this repo dropped. Nothing derives a module's version from
it.

## What enforces this

`tools/validate.py` — a changelog whose entries drift is what an unchecked convention
produces, and this one drifted for months before anyone counted. It errors on a missing
file, on a `PR:` line, on an unfilled `#NN`, on a heading that is not a date and a title,
and on a category outside its half's set. The deprecation-window obligation above is not
among them — whether it should be is #87's question, not this file's.
