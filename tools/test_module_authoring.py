#!/usr/bin/env python3
"""Acceptance tests for the authoring pass (#289).

AC-1, AC-2, AC-7, AC-8, AC-9 and AC-10 of features/business/module-authoring/.

Two halves, because the pass has two halves. AC-1 and AC-9 assert something about an
artefact — a module built the way `scrumia-author` Step 4 orders it is accepted by
`scrumia-module check` on the first run, and carries nothing for what it does not have —
and those run the real checker on a real tree. The refusals are prose an agent executes,
so what is asserted there is that each branch is still stated and, for AC-7, that the
destinations are *not* enumerated: the criterion says the pass chooses through another
feature's tree and enumerates neither itself, and a copy of that list is exactly the
regression worth catching.

Every assertion is written so it can fail. The clean-check ones are paired with a mutation
that must produce a finding, because a check that cannot go red proves nothing about the
tree it was pointed at.

Run from the repo root: python3 tools/test_module_authoring.py
Exit code 0 when everything passes, 1 otherwise.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "plugins" / "scrumia-core" / "bin" / "scrumia-module"
SKILL = ROOT / "plugins" / "scrumia-core" / "skills" / "scrumia-author" / "SKILL.md"

FAILURES: list[str] = []
TMP = Path(tempfile.mkdtemp(prefix="scrumia-authoring-"))


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  ok    {name}")
    else:
        FAILURES.append(f"{name}{' — ' + str(detail) if detail else ''}")
        print(f"  FAIL  {name}{' — ' + str(detail) if detail else ''}")


def verdict(path: Path) -> tuple[int, dict]:
    run = subprocess.run(
        [sys.executable, str(CHECKER), "check", str(path), "--json"],
        capture_output=True, text=True,
    )
    try:
        return run.returncode, json.loads(run.stdout)
    except json.JSONDecodeError:
        return run.returncode, {"state": "unparseable", "findings": [], "stderr": run.stderr}


# --------------------------------------------------------------------- the produced module

MANIFEST = {
    "name": "acme-oncall",
    "description": "The on-call handover: what the outgoing shift states and the incoming confirms.",
    "version": "0.1.0",
    "author": {"name": "acme"},
    "license": "MIT",
}

README = """# acme-oncall

The on-call handover, as a procedure rather than a habit. It states what the outgoing
shift has to have written down before it leaves, and what the incoming shift confirms
before it accepts.

## What it answers

Which of last night's noise the incoming shift actually has to care about — answered from
what the outgoing shift stated, rather than from a channel read backwards.

## What it refuses

- No incident state of its own. What is open lives in the tracker.
- No paging policy. Who is woken and when is a decision this module reads, never makes.

## What it ships

| Skill | Role |
|---|---|
| `acme-handover` | Runs one handover: what is stated, what is confirmed, what is escalated. |
"""

HANDOVER = """---
name: acme-handover
description: Runs one on-call handover — what the outgoing shift states, what the incoming shift confirms, and what is escalated rather than carried into the next shift.
---

# Hand over the shift

A handover is a statement made by the outgoing shift and accepted by the incoming one.

## Step 1 — The outgoing shift states three things

What is still open, what was silenced and when the silence expires, and what nobody got to.

## Step 2 — The incoming shift confirms, or refuses

Confirmation is a decision, not a courtesy.

## Step 3 — What outlives two shifts is escalated

An item carried through two handovers is not being handled, and saying so is the escalation.
"""


def produce(root: Path) -> Path:
    """The module `scrumia-author` Step 4 produces for a need that opens no register,
    reads no setting and publishes no name: the manifest, the README, and what the module
    actually does. Nothing for the three it does not have."""
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps(MANIFEST, indent=2))
    (root / "README.md").write_text(README, encoding="utf-8")
    skill = root / "skills" / "acme-handover"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(HANDOVER, encoding="utf-8")
    return root


# ------------------------------------------------------------------------------- AC-1

print("AC-1 — what the pass produces passes the checker on the first run")

module = produce(TMP / "ac1")
code, envelope = verdict(module)
check("the produced module is accepted, with nothing edited in between",
      code == 0 and envelope["state"] == "clean", envelope.get("findings") or envelope)

# The clean verdict above is only evidence if this tree can go red at all.
stripped = produce(TMP / "ac1-red")
(stripped / "README.md").unlink()
code, envelope = verdict(stripped)
check("…and the same check reports findings on a module missing a required part",
      code == 3 and envelope["state"] == "findings" and envelope["findings"], envelope)

# ------------------------------------------------------------------------------- AC-9

print("AC-9 — the pass writes no placeholder")

module = produce(TMP / "ac9")
absent = {
    "registers.json": not (module / "registers.json").exists(),
    "extends.json": not (module / "extends.json").exists(),
    "bin/": not (module / "bin").exists(),
}
check("no declaration for a register it opens none of, nor for a name it publishes none of",
      all(absent.values()), absent)
check("no settings section in the README for settings it reads none of",
      "settings" not in (module / "README.md").read_text().lower())
check("and the module is clean with all three absent", verdict(module)[1]["state"] == "clean")
# The three above judge the fixture, which is this file's own construction.
check("the pass states all three absences, and forbids the marker",
      all(s in SKILL.read_text().lower() for s in
          ("gets no declaration", "gets no section", "gets no `bin/`",
           "no marker to be filled in later")))

# An empty heading is the placeholder the criterion forbids, and it must be visible.
placeholder = produce(TMP / "ac9-red")
readme = placeholder / "README.md"
readme.write_text(readme.read_text() + "\n## Settings it reads\n\n## Decisions\n")
code, envelope = verdict(placeholder)
check("a heading with nothing under it is a finding, so the criterion can fail",
      code == 3 and any("nothing under it" in f["message"] for f in envelope["findings"]),
      envelope)

# The outcome a pass inverted into a scaffolder produces, and what makes the absence rule
# enforceable rather than advisory.
scaffolded = produce(TMP / "ac9-scaffold")
(scaffolded / "registers.json").write_text(
    '{"handover": {"skill": "acme-handover", "purpose": "Run one handover"}}')
code, envelope = verdict(scaffolded)
check("a register declared and never consulted is a finding, so a scaffold cannot pass",
      code == 3 and any(f["rule"] == "modular-composition/BR-11" for f in envelope["findings"]),
      envelope)

# ------------------------------------------------------------------------- the pass itself

print("The pass — the branches each refusal criterion requires")

pass_text = SKILL.read_text(encoding="utf-8")
lower = pass_text.lower()

# AC-2 — the three reaches, and the marketplace's two obligations stated before creating.
check("AC-2 names all three reaches",
      all(reach in lower for reach in
          ("this project's alone", "across their projects", "anyone's who runs scrumia")))
check("AC-2 names the version obligation, and sends the bump to release-versioning",
      "features/business/release-versioning/" in pass_text and "bumps" in lower)
check("AC-2 names the deprecation window before a renamed thing disappears",
      "deprecation window" in lower)
# A literal path here is what the third reach's criterion forbids.
check("AC-2 reaches the shared checkout through local-extension, naming no path itself",
      "features/business/local-extension/" in pass_text
      and "never something to write into a file" in lower
      and not re.search(r"[~$][\w/.]*shared|/shared[\w/.]*", pass_text, re.I))

# AC-7 — refuses, routes, and enumerates nothing. The negative is the load-bearing half:
# a copy of local-extension's three shapes here is the drift the criterion forbids.
check("AC-7 refuses below the threshold and creates nothing",
      "create nothing" in lower and "three distinct concerns" in lower)
check("AC-7 refuses the whole band, not only the single rule",
      "two concerns" in lower and "commonest input" in lower)
check("AC-7 routes through the tree rather than choosing",
      "scrumia-place" in pass_text)
# The leak takes the shape of a gloss on the link, so each list is guarded by one of its
# distinctive items rather than by a list-shaped pattern.
check("AC-7 enumerates none of local-extension's shapes itself",
      "rules section" not in lower and "ships to itself" not in lower)
check("AC-7 enumerates none of knowledge-placement's destinations itself",
      "agent memory" not in lower and "the change itself" not in lower)

# AC-8 — the slot test, and the two accepted alternatives rather than a slot with a caveat.
check("AC-8 states the slot test as a project that would fill it differently",
      "fill this slot with a different" in lower)
check("AC-8 offers both accepted alternatives",
      "capability in a module" in lower and "fills no slot" in lower)

# AC-10 — creating nothing is a completed pass, reported in the same shape.
check("AC-10 reports a pass that created nothing as a completed pass",
      "completed pass" in lower and "whether or not a module exists" in lower)

# BR-1's other half: the pass defers the standard rather than carrying a copy of it, which
# is what makes AC-1's checker run the authority instead of a second opinion.
check("the pass carries no copy of the anatomy standard's README sections",
      not any(s in pass_text for s in ("## What it answers", "## What it refuses", "## What it ships")))
check("the pass ends on the checker, reached by the name it is published under",
      "scrumia-module check" in pass_text)

shutil.rmtree(TMP, ignore_errors=True)

print()
if FAILURES:
    print(f"{len(FAILURES)} failure(s)")
    sys.exit(1)
print("all module-authoring criteria hold")
