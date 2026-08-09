# Changelog — Ground and shell

Reverse-chronological. Short. The reasoning is in the issues, not here.

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
