#!/usr/bin/env python3
"""Tests that the role-consultation rule stated in #121 is wired into the spec and the skills.

    python3 tools/test_role_consultation.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def fail(label: str, msg: str) -> None:
    FAILURES.append(f"{label}: {msg}")


def read(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        fail(rel, "missing")
        return ""
    return p.read_text(encoding="utf-8")


BUSINESS = read("features/business/agent-team/business.md")
QA = read("features/business/agent-team/qa.md")
CHANGELOG = read("features/business/agent-team/CHANGELOG.md")
REFINE = read("plugins/scrumia-github-project/skills/scrumia-refine/SKILL.md")
TICKET = read("plugins/scrumia-github-project/skills/scrumia-ticket/SKILL.md")
REVIEW = read("plugins/scrumia-github-project/skills/scrumia-review/SKILL.md")


def assert_in(needle: str, haystack: str, label: str) -> None:
    if needle not in haystack:
        fail(label, f"missing — {needle!r}")


def assert_not_in(needle: str, haystack: str, label: str) -> None:
    if needle in haystack:
        fail(label, f"present — {needle!r}")


SPEC_PATH = "features/business/agent-team/business.md"
for label, text in (("scrumia-refine", REFINE), ("scrumia-ticket", TICKET), ("scrumia-review", REVIEW)):
    if SPEC_PATH not in text and "agent-team/business.md" not in text:
        fail(f"AC-4 / {label} cites spec", f"no citation of {SPEC_PATH}")
    if "When a role must be consulted" not in text:
        fail(f"AC-4 / {label} cites section", "no citation of 'When a role must be consulted'")


assert_not_in("Call on the roles when it's useful", REFINE, "AC-1 / refine heading")
assert_in("## Step 4 — Call on the roles whose domain owns the blocker", REFINE, "AC-1 / refine step")
assert_in("agent-team/business.md", REFINE, "AC-1 / refine cites spec")
assert_in("When a role must be consulted", REFINE, "AC-1 / refine cites section")
assert_in("The report names the roles consulted", REFINE, "AC-2 / refine report obligation")
assert_in("### AC-18", QA, "AC-2 / qa.md scenario")
assert_in("When a role must be consulted", TICKET, "AC-3 / ticket cites spec")
assert_in("AC-19", TICKET, "AC-3 / ticket references AC-19")
assert_in("The description names the roles consulted", TICKET, "AC-3 / ticket PR description")
assert_in("When a role must be consulted", REVIEW, "AC-3 / review cites spec")
assert_in("AC-20", REVIEW, "AC-3 / review references AC-20")
assert_in("Name which role ran", REVIEW, "AC-3 / review names role that ran")


for ac in ("AC-17", "AC-18", "AC-19", "AC-20", "AC-21"):
    if not re.search(rf"### {ac} — ", QA):
        fail(f"AC-5 / qa.md scenario {ac}", "missing scenario heading")
    body = QA.split(f"### {ac}", 1)[1].split("### ", 1)[0]
    for keyword in ("Given", "When", "Then"):
        if keyword not in body:
            fail(f"AC-5 / qa.md scenario {ac}", f"missing {keyword} clause")


assert_in("### AC-21", QA, "AC-6 / qa.md scenario")
assert_in("convened once across the pass", QA, "AC-6 / qa.md wording")
assert_in("asked once", BUSINESS, "AC-6 / business.md wording")
assert_in("referenced by all of them", BUSINESS, "AC-6 / business.md wording")
assert_in("## When a role must be consulted", BUSINESS, "spec / section")
assert_in("A role is consulted when any of the following holds", BUSINESS, "spec / condition")
for trigger in (
    "ambiguous, missing, or contradicted",
    "reaches beyond one feature",
    "An interface contract changes",
    "blocks several tickets",
):
    if trigger not in BUSINESS:
        fail("spec / trigger", f"missing — {trigger!r}")
assert_in("### Unreachable roles", BUSINESS, "spec / unreachable roles")
for needle in (
    "states **which roles were consulted",
    "or states that no role was needed",
):
    if needle not in BUSINESS:
        fail("spec / report obligation", f"missing — {needle!r}")
assert_in("## 2026-08-17", CHANGELOG, "changelog / heading")
assert_in("#121", CHANGELOG, "changelog / ticket reference")
assert_in("Role consultation becomes a reflex", CHANGELOG, "changelog / subject")


if FAILURES:
    print(f"{len(FAILURES)} failure(s):", file=sys.stderr)
    for f in FAILURES:
        print(f"  - {f}", file=sys.stderr)
    sys.exit(1)

print("All role-consultation checks pass.")
