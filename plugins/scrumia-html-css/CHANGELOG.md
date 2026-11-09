# Changelog — scrumia-html-css

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.0] - 2026-11-09
### Added
- `rules/contrast-incomplete-is-unmeasured.md` — text an automated contrast measure leaves
  `incomplete` because its background is a gradient or an image (axe-core's `bgGradient` /
  `bgImage`) has not been measured; each case is recomputed against the lowest-contrast
  colour actually painted behind it, at 4.5:1 or 3:1 for large text, and reported with
  its ratio and pair. Contributed to `review`.

### Changed
- `skills/html-css-audit/SKILL.md` — Step 4 refuses a "0 violations" contrast verdict while
  such cases remain open, and points to the new rule.
- `README.md` — the new refusal is listed.

## [0.1.0] - 2026-08-16
### Added
- The HTML, CSS and accessibility capability — three refusal rules (`semantic-over-aria`, `element-follows-purpose`, `tests-query-by-role`) contributed to the `implement` register, with a review summary on the `review` register.
- `bin/detect-vitest.sh` — the conditional detector that activates the `tests-query-by-role` rule when vitest is present and at least one component test file exists; otherwise the directive contributes nothing.
- `html-css-audit` — the audit skill that measures an interface against the three rules, each finding citing the source the rule is derived from.
- Site entry — `site/modules.json` registers the plugin with an emoji; i18n files for both `en` and `fr` carry the prose the marketplace page reads.
