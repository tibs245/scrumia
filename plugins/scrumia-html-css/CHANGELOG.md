# Changelog — scrumia-html-css

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- The HTML, CSS and accessibility capability — three refusal rules (`semantic-over-aria`, `element-follows-purpose`, `tests-query-by-role`) contributed to the `implement` register, with a review summary on the `review` register.
- `bin/detect-vitest.sh` — the conditional detector that activates the `tests-query-by-role` rule when vitest is present and at least one component test file exists; otherwise the directive contributes nothing.
- `html-css-audit` — the audit skill that measures an interface against the three rules, each finding citing the source the rule is derived from.
- Site entry — `site/modules.json` registers the plugin with an emoji; i18n files for both `en` and `fr` carry the prose the marketplace page reads.
