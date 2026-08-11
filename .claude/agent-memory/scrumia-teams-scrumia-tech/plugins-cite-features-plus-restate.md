---
name: plugins-cite-features-plus-restate
description: House idiom for a plugin citing this repo's features/ — relative link for authority PLUS an inline operative restatement, because the link cannot resolve in a marketplace install
metadata:
  type: project
---

Skills and agents under `plugins/` cite this repo's specs with a relative link
(`../../../../features/business/<feature>/business.md § *Section*`). Established across
`scrumia-manager.md`, `scrumia-refine/SKILL.md`, `scrumia-project-setup/SKILL.md`
(execution-policy citations), and `scrumia-ticket/SKILL.md`, `scrumia-review`,
`scrumia-tech.md` (dev-flow citations). It is the convention, not a slip.

**The link does not resolve outside this repo.** In a marketplace install the plugin sits
under `~/.claude/plugins/…`, and `../../../../features/` points at nothing. So the idiom
is really two-part: **cite for authority, restate the operative rule inline** so the text
still works when the link is dead. Apparent duplication of a rule across skills is
therefore often deliberate degraded-mode cover, not drift — judge it on whether the
restatements still agree, not on the copy count.

The `execution-policy` sites carry a portability hedge the `dev-flow` sites omit:
*"or whichever feature owns the axis in the project being set up — substitute that path"*.
That hedge is the more careful form of the idiom.

**Why this trips reviews up:** the duplication reads like a drift machine until the
marketplace-install case explains it.

**How to apply:** do not flag a restatement beside a `features/` citation as redundancy —
check the restatements agree with the source and with each other. Do flag a citation that
carries *no* inline summary: in a consumer install it degrades to nothing. Related:
[[pitfall-cross-skill-claims]].
