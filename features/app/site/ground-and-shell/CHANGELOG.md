# Changelog — Ground and shell

Reverse-chronological. Short. The reasoning is in the issues, not here.

## 2026-08-10 — index sheds its rules, ux.md is born, tech.md gains three
- Issue: #193
- PR: #NN (filled at merge)
- Breaking: no. `index.md` drops its "The rules this feature owns" section — six
  rules move to `tech.md` (three cited from `design/tokens.css` and
  `design/identity.md` rather than restated, three new), one moves to a new
  `ux.md`. `index.md` now carries exactly the template's four sections, and its
  Files present table stops listing `tools/check_contrast.py`, which lives
  outside this feature — it is now an Authority line under Links instead.

## 2026-08-09 — `check_contrast.py` gates CI, `qa.md` names who feeds it
- Issue: #95
- PR: (filled at merge)
- Breaking: no. `python3 tools/check_contrast.py` now runs as its own step in
  `.github/workflows/validate.yml`, so AC-6 is an enforced gate rather than a
  criterion nothing runs. `qa.md` AC-6 gains the maintenance rule the tool
  cannot enforce itself: whoever introduces a new token-on-token pair in
  `site/assets/style.css` adds the matching row to `PAIRS`, in the same PR.

## 2026-08-09 — The rail ships
- Issue: #112
- PR: (filled at merge)
- Breaking: no. Implements `design/components/site-header/spec.md` → "The rail",
  decided in #74. `site/assets/style.css` no longer lights the hover
  underline — only `aria-current` does, in the baseline — and a new
  `site/assets/header.js` slides a rail under the pointed-at or focused nav
  link for hover-capable pointers, home to the current page at rest. Touch
  and no-JS keep the static underline #59 shipped, unchanged.

## 2026-08-09 — The site-header candidate is settled: the rail
- Issue: #74
- PR: (filled at merge)
- Breaking: no — spec-only. `design/components/site-header/spec.md` now
  records the rail (C) as the decided pointer treatment and the delivered
  baseline #59 shipped; A (assembly) and B (scanline) are removed from the
  file. The rail itself is not yet implemented — tracked in #112 — so nothing
  in `site/assets/style.css` or `site/templates/partials/header.html` changed.

## 2026-08-09 — The two actor colours swap jobs; the ground gets its own base
- Issue: #52
- Breaking: no — `--human` and `--agent` keep their names, so every consumer was
  already correct. `--human-ink` is gone (unspent), `--sky` is new.

## 2026-08-09 — `legal.md` records the trademark/affiliation risk and its acceptance
- Issue: #67
- PR: (filled at merge)
- Breaking: no

## 2026-08-08 — First version: the orbit ground, the shell, and one palette per theme
- Issue: #59
- PR: #77
- Breaking: no
