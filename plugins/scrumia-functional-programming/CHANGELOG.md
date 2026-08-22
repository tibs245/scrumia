# Changelog — scrumia-functional-programming

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-08-22
### Added
- `extends.json` — the six paradigm principles (purity, totality, referential
  transparency, immutability, composition over inheritance, effect discipline) and
  the misplaced-rule finding are contributed to the `implement`, `review` and
  `find-spec` registers.
- `bin/scrumia-functional-programming-check-vocabulary` — the vocabulary gate
  (CI refuses a PR whose check exits non-zero). Auto-discovered by
  `tools/validate.py`, which scans `plugins/*/bin/*`.
- `README.md` — addressed to whoever is deciding whether to run this module,
  not to the agent that already does: what it answers, what it refuses, what it
  ships, what it expects to find.
