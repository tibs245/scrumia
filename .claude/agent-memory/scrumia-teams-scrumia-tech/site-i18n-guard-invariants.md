---
name: site-i18n-guard-invariants
description: Why the build_site.py unused-key guard is scoped to page-level i18n keys and must not be naively extended to common.json — programmatic string reads are invisible to it
metadata:
  type: project
---

`tools/build_site.py`'s anti-divergence guard fails the build on a key a template
needs and a language lacks, **and** (since #114) on a page-level key no template
reads. Two invariants govern any future change to it:

1. **The unused-key half is deliberately scoped to `site/i18n/<lang>/<page>.json`,
   never `common.json`.** Chrome keys are shared across pages, so per-page
   unused-ness is meaningless for them — but the deeper reason is that a string can
   be read **programmatically**, with no `{{token}}` anywhere. `mod_no_slot` is the
   live example: `module_specials()` reads it out of `labels` directly. Extending
   the guard to chrome keys without first inventorying the programmatic reads turns
   the repo's own build red on a false positive.

2. **The `page_keys` reparse in `render_page` must stay non-raising.** It reads a
   file `load_strings` already parsed under a `try`; the `JSONDecodeError` fallback
   to an empty set is what keeps a malformed file reported once as a clean
   `error:` line instead of a traceback (AC-6 of `features/app/site/module-pages`).
   Promoting the check from warning to error did not change this — an empty
   `page_keys` silently disables the unused half for that file, which is correct
   because the file is already failing the build for another reason.

The guard has real teeth: `.github/workflows/validate.yml` runs
`python3 tools/build_site.py` and then `git diff --exit-code site/`, so both a
guard failure and a stale committed page break CI.

**Why:** established reviewing #114, which promoted the unused-key warning to an
error. The `mod_no_slot` trap is only visible by tracing `module_specials`, not by
reading the guard.
**How to apply:** when a change touches the i18n guard or proposes widening it,
check for programmatic string reads before assuming a key is dead, and keep the
reparse's except-branch intact.
