---
name: plugins-cite-features-plus-restate
description: House idiom for a plugin citing this repo's features/ — relative link for authority PLUS an inline operative restatement, because the link cannot resolve in a marketplace install
metadata:
  type: project
---

Skills and agents under `plugins/` cite this repo's specs with a relative link
(`../../../../features/business/<feature>/business.md § *Section*`). Established sites:
`scrumia-manager.md:58`, `scrumia-refine/SKILL.md:92`, `scrumia-project-setup/SKILL.md:66`
(execution-policy), and `scrumia-ticket/SKILL.md:121,137,154,219`, `scrumia-review:42`,
`scrumia-tech.md:38` (dev-flow). It is the convention, not a slip.

**The link does not resolve outside this repo.** In a marketplace install the plugin sits
under `~/.claude/plugins/…`, and `../../../../features/` points at nothing. So the idiom
is really two-part: **cite for authority, restate the operative rule inline** so the text
still works when the link is dead. Apparent duplication of a rule across skills is
therefore often deliberate degraded-mode cover, not drift — judge it on whether the
restatements still agree, not on the copy count.

The `execution-policy` sites carry a portability hedge the `dev-flow` sites omit:
*"or whichever feature owns the axis in the project being set up — substitute that path"*.
That hedge is the more careful form of the idiom.

**Why:** worked out reviewing #31, which added three more dev-flow citations. The
duplication looked like a drift machine until the marketplace-install case explained it.

**How to apply:** do not flag a restatement beside a `features/` citation as redundancy —
check the restatements agree with the source and with each other. Do flag a citation that
carries *no* inline summary: in a consumer install it degrades to nothing. Related:
[[pitfall-cross-skill-claims]].
