# Module authoring — business rules

## Value

For someone who has a procedure, a standing rule or a capability worth running in more
than one place, and no stated way to turn it into a module. It brings one guided pass
from nothing to a module that already meets the anatomy standard, the same pass for
changing an existing one, and a promotion that moves a module between locations without
rewriting it. It matters because extending ScrumIA today means either forking the
marketplace or reading three paragraphs inside a diagnostic skill and improvising the
rest — and an improvised module is one nothing will ever check. Measurable: the count of
findings the anatomy checker returns on a module this pass produced, which is expected to
be zero, and the count of files a promotion rewrites, which is expected to be none.

## A module is created where it is first used

The location is not a preference. A module lives where the need it answers lives, and
moves only when the need turns out to be somewhere else too:

| The need is | The module lives |
|---|---|
| this project's alone | inside the project |
| this person's, across their projects | in a directory shared between them |
| anyone's who runs ScrumIA | in a marketplace |

Starting at the marketplace is the expensive mistake, because a module published before
its second use has adopters before it has evidence, and `release-versioning` then makes
every correction cost a bump and a window. Starting inside the project costs nothing and
loses nothing: the places are `local-extension`'s to define, and a module is the same
artefact in all three.

## Promotion moves a module, it never reshapes one

A module written for one project is publishable without a file being rewritten. This is
the whole reason the anatomy standard has no local tier: had a local module been allowed
a looser shape, promotion would mean a rewrite, and a rewrite is what nobody does.

Promotion changes two things and nothing else: where the module sits, and what declares
it. What it contains is already correct or was never correct.

The reverse direction is legitimate and carries no ceremony. A module that turned out to
serve one project moves back in, and the projects that had adopted it are told through
the mechanism `release-versioning` owns.

## Editing a module goes through the same pass as creating one

There is no lighter path for a change. An edit that skips the check is how a module that
passed once stops passing without anyone noticing — which is the failure the checker
exists to catch, arriving through the one door left open.

What an edit adds over a creation is the question a creation cannot ask: **what does this
change cost a project that has already adopted the module?** Authoring names the change's
**type and scope** — the commit signal — and stops. The level follows from them, and
`release-versioning` is explicit that it is read off the commit rather than chosen; a pass
announcing "this is a minor" asserts a conclusion from inputs that are not written yet, and
below `1.0.0` — where every module still sits — "minor" names two different things at once.

## Two refusals

**A module is never created for a need below the threshold.** One standing rule is the
clearest case and not the only one: everything between one rule and roughly three distinct
concerns falls here too, and a two-concern need is the commonest input the pass gets. What
is refused is not a module — it is one of the shapes
`features/business/local-extension/` lists, and `knowledge-placement`'s tree chooses
between them. This feature enumerates neither: a list restated here is the one that
drifts. A module built below the threshold is a wrapper whose only content is the ceremony
of being a module, and it will be installed, versioned and maintained for that.

The threshold is the one the anatomy standard already implies: below roughly three
distinct concerns, the structure costs more than it carries. Reaching for a module before
that is reaching for the most expensive container available.

**A new slot is never invented to hold a new module.** A slot is justified only when a
real project would fill it differently; otherwise what is being described is one more
capability in an existing module, or a module that fills no slot at all — which is
permitted and is what `scrumia-core` and `scrumia-rules` already do. What a slot is, and
when a new one is justified, is `modular-composition`'s.

Both refusals are stated as refusals rather than as guidance because the pass is run by
an agent, and an agent asked to create a module will create one.

## What the pass produces

A module that the checker accepts on its first run. Not a scaffold to be completed, not a
tree of files with headings and nothing under them: the anatomy standard makes an empty
file worse than an absent one, and a pass that emits placeholders is a pass that produced
findings and called them a starting point.

Where the pass has nothing to write — a register the module opens nothing on, a setting it
reads none of — it writes nothing, and the absence is the statement.

## Business rules

- **BR-1** — What authoring produces meets the anatomy standard on its first check. A
  pass whose output has findings against it did not finish.
- **BR-2** — A module is created in the location matching the reach of the need it
  answers, and the default is the narrowest one that covers it.
- **BR-3** — Promotion changes a module's location and what declares it, and rewrites no
  file it contains. Demotion is the same move in the other direction and carries no extra
  ceremony.
- **BR-4** — Editing a module runs the same pass and the same check as creating one.
  There is no lighter path.
- **BR-5** — An edit names the type and scope its commit carries. The level the bump takes
  is derived from them by `release-versioning`, never announced here.
- **BR-6** — A module is not created for a need below the threshold: one standing rule,
  and everything between that and roughly three distinct concerns. The pass names the
  destination that fits instead, and creates nothing.
- **BR-7** — A new slot is not invented to hold a new module. A module filling no slot is
  the accepted answer where a slot is not justified.
- **BR-8** — The pass writes no placeholder. Where it has nothing to write, it writes
  nothing.

## Vocabulary

- **Pass** — the guided sequence that produces or changes a module. Named to make clear
  it is not a template expansion: it asks, it refuses, and it can end having created
  nothing.
- **Promotion** — a change of a module's location toward wider reach. Not a release, and
  not a version bump; either may follow it.
