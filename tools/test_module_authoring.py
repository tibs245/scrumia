#!/usr/bin/env python3
"""Acceptance tests for the authoring pass (#289, #290).

AC-1 through AC-10 of features/business/module-authoring/.

Two halves, because the pass has two halves. AC-1 and AC-9 assert something about an
artefact — a module built the way `scrumia-author` Step 4 orders it is accepted by
`scrumia-module check` on the first run, and carries nothing for what it does not have —
and those run the real checker on a real tree. The refusals are prose an agent executes,
so what is asserted there is that each branch is still stated and, for AC-7, that the
destinations are *not* enumerated: the criterion says the pass chooses through another
feature's tree and enumerates neither itself, and a copy of that list is exactly the
regression worth catching.

AC-3 and AC-4 perform the move rather than reading the pass, and it is worth being exact
about which of their assertions carry weight. Comparing a tree to itself across a
`shutil.move` proves a property of the standard library, not of promotion; what it does
buy is a guard on the instrument, since a `digest()` returning nothing — or keying on
absolute paths — passes that comparison and fails the paired case that completes the
manifest on the way out. The two assertions that actually carry AC-3 are the ones about
the world the move happens in: that `scrumia-module check` returns the same verdict from
either location, findings and all, and that the rekeyed declaration re-resolves through
the real `scrumia-extends --modules` to the new location.

Every assertion is written so it can fail. The clean-check ones are paired with a mutation
that must produce a finding, because a check that cannot go red proves nothing about the
tree it was pointed at.

What is *not* covered, stated so it is not read as coverage. A substring assertion cannot
catch a polarity flip, and three of the guards below are substring assertions wearing a
criterion's name:

- **AC-6** — the level guard requires both level words to fall inside the prohibition's
  own character range, so a level named in another step goes red. One written *into* the
  prohibition's sentences does not.
- **AC-4** — the refusal clause is matched by the phrases that state it. Appending an
  instruction to open an issue on every adopting project leaves those phrases intact and
  stays green.
- **AC-5** — the ordering guard matches the heading and the preamble, not the operative
  body. Rewriting that body to run the check *after* the edit stays green.

Deleting any of the three goes red; inverting any of the three does not. Nor can
`scrumia-module check` be leaned on for the refusals — it accepts a one-concern module and
an invented slot without complaint, which is why AC-7 and AC-8 assert prose and nothing
more.

Run from the repo root: python3 tools/test_module_authoring.py
Exit code 0 when everything passes, 1 otherwise.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "plugins" / "scrumia-core" / "bin" / "scrumia-module"
RESOLVER = ROOT / "plugins" / "scrumia-core" / "bin" / "scrumia-extends"
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


def digest(root: Path) -> dict[str, str]:
    """Every file the module ships, keyed by its path inside the module.

    Keyed relatively on purpose: an absolute path changes with every move, and comparing
    those would make the criterion fail on the one thing it is supposed to allow.
    """
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*")) if p.is_file()
    }


def declare(project: Path, key: str) -> Path:
    """A project declaring exactly one module, by the source it comes from."""
    (project / ".scrumia").mkdir(parents=True, exist_ok=True)
    config = project / ".scrumia" / "config.yaml"
    config.write_text(
        f'project:\n  name: "acme"\n\nmodules:\n  "{key}": {{}}\n', encoding="utf-8")
    return config


def resolved(config: Path, shared: Path | None = None) -> dict:
    """The one row `scrumia-extends --modules` returns for that declaration.

    $SCRUMIA_SHARED_DIR is pinned on every call, empty unless a test names one: a
    developer's own machine may carry it, and a test that inherited it would pass or fail
    on whose machine it ran.
    """
    env = {**os.environ, "NO_COLOR": "1", "SCRUMIA_MODULE_DIR": "plugins",
           "SCRUMIA_CONFIG": str(config), "SCRUMIA_SHARED_DIR": str(shared or ""),
           "SCRUMIA_CONFIG_LOCAL": "/nonexistent/config.local.yaml"}
    run = subprocess.run([str(RESOLVER), "--modules", "--json"],
                         cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
    try:
        return json.loads(run.stdout)[0]
    except (json.JSONDecodeError, IndexError):
        return {"state": "unparseable", "stdout": run.stdout, "stderr": run.stderr}


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

# ------------------------------------------------------------------------------- AC-3

print("AC-3 — promotion changes the location and the declaration, and rewrites no file")

project = TMP / "ac3"
inside = project / ".scrumia" / "modules" / "acme-oncall"
produce(inside)
config = declare(project, "local:acme-oncall")

before_files, before_verdict = digest(inside), verdict(inside)
row = resolved(config)
check("before the move, the declaration resolves from inside the project",
      row["state"] == "resolved" and row["location"] == "local", row)

checkout = TMP / "ac3-checkout"
checkout.mkdir()
outside = checkout / "acme-oncall"
shutil.move(str(inside), str(outside))
declare(project, "shared:acme-oncall")

after_files = digest(outside)
check("every file the module ships is byte-identical after the promotion",
      before_files == after_files,
      {k: (before_files.get(k), after_files.get(k)) for k in before_files.keys() | after_files.keys()
       if before_files.get(k) != after_files.get(k)})
check("its own manifest included — the one file both shipped and tempting to complete",
      before_files.get(".claude-plugin/plugin.json") == after_files.get(".claude-plugin/plugin.json"))
check("and the checker's verdict is the same after as before",
      verdict(outside) == before_verdict, verdict(outside))
row = resolved(config, shared=checkout)
check("what changed instead is the declaration, which now resolves from the checkout",
      row["state"] == "resolved" and row["location"] == "shared"
      and row["roots"][0]["root"].startswith(str(checkout.resolve())), row)

# Without this pairing the criterion above would also pass on a promotion that reshaped
# the module, which is the failure BR-3 names.
red_project = TMP / "ac3-red"
red_inside = red_project / ".scrumia" / "modules" / "acme-oncall"
produce(red_inside)
red_before = digest(red_inside)
red_outside = TMP / "ac3-red-checkout" / "acme-oncall"
red_outside.parent.mkdir()
shutil.move(str(red_inside), str(red_outside))
completed = json.loads((red_outside / ".claude-plugin" / "plugin.json").read_text())
completed["homepage"] = "https://github.com/acme/acme-oncall"
completed["repository"] = "https://github.com/acme/acme-oncall"
(red_outside / ".claude-plugin" / "plugin.json").write_text(json.dumps(completed, indent=2))
red_after = digest(red_outside)
check("a promotion that completes the manifest on the way out fails the same comparison",
      red_before != red_after
      and red_before[".claude-plugin/plugin.json"] != red_after[".claude-plugin/plugin.json"])
check("…while the checker still calls it clean, so the verdict alone would not catch it",
      verdict(red_outside)[1]["state"] == "clean", verdict(red_outside))

# ------------------------------------------------------------------------------- AC-4

print("AC-4 — demotion is the same move, unceremonious")

back = project / ".scrumia" / "modules" / "acme-oncall"
back.parent.mkdir(parents=True, exist_ok=True)
shutil.move(str(outside), str(back))
declare(project, "local:acme-oncall")

check("moving back rewrites nothing either", digest(back) == before_files)
check("and the verdict is still the one the module had before it ever moved",
      verdict(back) == before_verdict, verdict(back))
row = resolved(config)
check("the declaration resolves from inside the project again",
      row["state"] == "resolved" and row["location"] == "local", row)

# ------------------------------------------------------------------------------- AC-5

print("AC-5 — editing runs the same check as creating")

edited = produce(TMP / "ac5")
check("a module that currently passes the checker", verdict(edited)[1]["state"] == "clean")
readme = edited / "README.md"
readme.write_text(readme.read_text().replace("## What it refuses", "## What it declines"))
code, envelope = verdict(edited)
check("a change that introduces a finding is reported by the same check",
      code == 3 and envelope["findings"], envelope)

# Only a run taken before the edit tells a module's own findings from the pass's.
inherited = produce(TMP / "ac5-inherited")
(inherited / "README.md").write_text("# acme-oncall\n\nWhat it is, and nothing else yet.\n")
pre_existing = {f["message"] for f in verdict(inherited)[1]["findings"]}
check("the module carries findings before the pass opens it", bool(pre_existing))

(inherited / "registers.json").write_text(
    '{"handover": {"skill": "acme-handover", "purpose": "Run one handover"}}')
after_edit = {f["message"] for f in verdict(inherited)[1]["findings"]}
check("the edit's own finding is isolated by subtracting the run taken first",
      pre_existing < after_edit and len(after_edit - pre_existing) >= 1,
      sorted(after_edit - pre_existing))
check("…and reporting only the second run would attribute the module's own findings to the pass",
      len(after_edit) > len(after_edit - pre_existing))

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

# Anchored to the step rather than to a bare substring: the deferral section names the same
# command, so a grep for it alone stays green with Step 5 deleted.
step5 = pass_text.partition("## Step 5")[2]
check("AC-1 ends the pass on the checker, in a step of its own",
      "scrumia-module check" in step5)
check("AC-1 makes a clean check the finishing condition, not a report line",
      "has not finished while the module" in step5.lower())
check("AC-2 states the inferred reach out loud before anything is created",
      "state the reach you inferred" in lower)
check("AC-1 counts the concerns before the refusal reads the count",
      "distinct concerns" in pass_text.partition("## Step 2")[0].lower())
# What ties produce() to the pass: the fixture's manifest path is the one Step 4 orders first.
check("the fixture is built on the manifest path Step 4 names",
      ".claude-plugin/plugin.json" in pass_text
      and (TMP / "ac1" / ".claude-plugin" / "plugin.json").exists())

# ------------------------------------------------------ the pass, on a module that exists

print("Step 0 — what a change and a move owe, as the pass states them")

step0 = pass_text.partition("## Step 0")[2].partition("## Step 1")[0]
# Prose wraps, so every phrase below is matched against the text with its line breaks
# collapsed — otherwise a reflow breaks an assertion that nothing about the rule changed.
step0_lower = " ".join(step0.lower().split())
check("the pass carries a step for a module that already exists", bool(step0.strip()))
check("AC-5 orders the check before anything is touched",
      "before you touch it" in step0_lower and "before** anything is touched" in step0_lower)
check("the steps after it are scoped, so a move is never told to clear a finding it inherited",
      "asked of what the change adds" in step0_lower
      and "about what this pass wrote" in step0_lower
      and "step 4 has nothing to do" in step0_lower)
check("AC-5 keeps the two runs apart rather than merging them",
      "difference between the two" in step0_lower and "step 5" in step0_lower)
check("AC-3 states the two things a move changes, and that both are outside the module",
      "outside the module" in step0_lower and "byte-identical" in step0_lower)
check("AC-3 names the manifest as inside the boundary, on business.md's decision",
      "manifest included" in step0_lower)
check("AC-3 asks for the diff rather than for the claim",
      "diff -r" in step0_lower and "is not evidence" in step0_lower)
check("AC-4 sends the withdrawal to release-versioning, names the gap, and invents nothing",
      "release-versioning" in step0_lower and "today it does not" in step0_lower
      and "do not open an issue" in step0_lower and "notify through" in step0_lower)
check("AC-6 names the type and the scope and sends the level to release-versioning",
      "**type**" in step0_lower and "**scope**" in step0_lower
      and "features/business/release-versioning/" in step0)
# The polarity guard, and the limit named in this file's docstring: it catches a level
# named outside the prohibition, not one written into it.
check("AC-6 forbids announcing a level rather than merely omitting one",
      "do not announce one" in step0_lower)
# Offsets rather than membership: a level word named in another step is often a substring
# of the prohibition too, so only its position tells the two apart.
opens = pass_text.index("### Name the commit")
closes = pass_text.index("## Step 1", opens)
levels = [m.start() for m in re.finditer(r"\bminor\b|\bmajor\b", pass_text, re.I)]
stray = [pass_text[max(0, i - 70):i + 15] for i in levels if not opens < i < closes]
check("and neither level word appears anywhere outside that prohibition",
      bool(levels) and not stray, stray)

frontmatter = pass_text.partition("---")[2].partition("---")[0].lower()
check("the description routes a change and a move here, or none of the above is reached",
      "to change one" in frontmatter and "move one between locations" in frontmatter,
      frontmatter.strip())

report = " ".join(pass_text.partition("## What the pass reports")[2].lower().split())
check("the report carries the pre-existing findings, the move and the commit signal",
      "before** step 0" in report and "the location it left" in report
      and "type and the scope" in report and "no level" in report)

shutil.rmtree(TMP, ignore_errors=True)

print()
if FAILURES:
    print(f"{len(FAILURES)} failure(s)")
    sys.exit(1)
print("all module-authoring criteria hold")
