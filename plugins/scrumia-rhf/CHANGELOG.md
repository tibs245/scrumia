# Changelog — scrumia-rhf

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `extends.json` — the three refusals (`form-has-resolver`,
  `inputs-are-registered`, `state-through-library`) are contributed to
  the `implement` and `review` registers, so a skill applies them
  without naming this module.
- `rules/` — one file per refusal, citing `https://react-hook-form.com`
  pinned to v7.
- `skills/rhf-audit/SKILL.md` — the audit against the three refusals.
- The capability the plugin carries: declarative form management for
  React implementations, paired with schema-driven validation through
  a resolver.
