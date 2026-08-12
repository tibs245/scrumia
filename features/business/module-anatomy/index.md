# Module anatomy

**Status**: draft

## In brief

The shape a ScrumIA module takes inside itself, and what says whether a given module has
it. One concern per file, an index that routes rather than carries, a README addressed to
whoever is choosing the module rather than to the agent running it — and a verdict
something other than a careful reader can produce. One authority, applied through two
surfaces split on what a program can decide without reading for meaning: a procedural
check for the decidable half, a cheap agent answering a closed checklist for the judged
one. The standard applies to every module the marketplace ships, the one owning the two
surfaces included.

## Links

- Implemented by: no App feature. The procedural check is `scrumia-module check`, a name
  `scrumia-core` publishes on `PATH` like `scrumia-extends`; the audit is a skill in the
  same module. `tools/validate.py` becomes a consumer of the first and keeps only what
  neither surface can see.
- Defers to: `features/business/modular-composition/` for what a module owes to be
  **pluggable** — that list is closed at three items on the test of silent breakage
  across compositions, and this feature adds nothing to it. It answers a different
  question, on a different test: whether a module can be navigated and verified.
- Defers to: `features/business/release-versioning/` for what a change to a module costs
  a project that has adopted it. This feature says what a module must look like, not what
  moving it promises.
- Consumed beyond this feature: `features/business/module-authoring/` produces modules
  against this standard; `features/business/local-extension/` states that a module
  resolved outside the marketplace is held to it unchanged.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding what a module must contain, what it must not, and who owns the verdict |
| `tech.md` | Understanding what the checker reads, what it reports, and what it refuses to do |
| `qa.md` | Checking this feature's acceptance criteria |
| `CHANGELOG.md` | History of changes to this spec |

No `ux.md`, `legal.md` or `security.md`: a checker that writes nothing and reads only a
module's own tree has no interface, no personal data and no privileged surface.

