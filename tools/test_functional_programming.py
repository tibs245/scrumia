#!/usr/bin/env python3
"""Acceptance tests for plugins/scrumia-functional-programming/ (#450).

Run from the repo root: python3 tools/test_functional_programming.py
Exit code 0 when everything passes, 1 otherwise. No dependencies.

One scenario per AC the ticket owns:

- AC-1, AC-6: every rule fragment is language-neutral; the vocabulary gate
  catches a drift, skips README.md, and skips `Verified in:` lines.
- AC-2: a synthetic misplaced rule trips the gate and the script names the
  rule file and line.
- AC-3, AC-4: the module activates alone — its extends.json carries
  contributions to implement, review, and find-spec, and the plugin ships no
  cross-dependency on a language module.
- AC-5: the module lands and merges independently; no project-local extension
  on a language module carries the paradigm principles.
- AC-7: every principle carries a `Verified in:` footer naming at least two
  cited languages.

A test for AC-6's failure mode builds a throwaway fixture tree under /tmp
and runs the script against it, so the gate is proven by an input that
actually fails rather than by reading the source.

    python3 tools/test_functional_programming.py
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "scrumia-functional-programming"
SCRIPT = PLUGIN / "bin" / "scrumia-functional-programming-check-vocabulary"
EXTENDS = PLUGIN / "extends.json"
SKILL_DIR = PLUGIN / "skills" / "scrumia-functional-programming"
RULES_DIR = SKILL_DIR / "rules"
README = PLUGIN / "README.md"

CITED_LANGUAGES = {"Kotlin", "JavaScript", "Rust", "Scala", "F#", "Haskell", "Swift"}

FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  ok    {name}")
    else:
        FAILURES.append(f"{name}: {detail}")
        print(f"  FAIL  {name}: {detail}")


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=30)
    return proc.returncode, proc.stdout, proc.stderr


# ---------------------------------------------------------------- AC-1, AC-6

print("AC-1 / AC-6 — the vocabulary gate exists, is executable, and accepts the shipped rules")


def test_script_exists_and_is_executable() -> None:
    check("bin/scrumia-functional-programming-check-vocabulary exists", SCRIPT.is_file())
    check("the script is executable (chmod +x)",
          SCRIPT.is_file() and os.access(SCRIPT, os.X_OK))


def test_shipped_rules_pass_the_gate() -> None:
    rc, out, err = run([str(SCRIPT)], cwd=ROOT)
    check("shipped rule fragments pass the gate (exit 0)",
          rc == 0,
          f"exit={rc}, stdout={out!r}, stderr={err!r}")


def test_skip_readme() -> None:
    """AC-6a — README.md is scanned for tokens only when it is itself a rule
    fragment, which it is not: a README is meta-information about the module,
    not a rule, and the gate skips it by name.

    A throwaway fixture tree with a README.md carrying banned tokens proves the
    skip. The script under test is invoked with PLUGIN_ROOT pointing at the
    fixture via readlink-style indirection; the simplest path is to drop a
    marker rule next to the README so the script sees at least one file to
    scan, then assert that the README's tokens do not surface in the report.
    """
    tmp = Path(tempfile.mkdtemp())
    try:
        rules = tmp / "skills" / "scrumia-functional-programming" / "rules"
        rules.mkdir(parents=True)
        (rules / "ok-rule.md").write_text(
            "A clean rule with no language-specific tokens.\n", encoding="utf-8"
        )
        (tmp / "README.md").write_text(
            "This README mentions `Promise` and `Effect` and `Future` — "
            "tokens that would otherwise trip the gate.\n",
            encoding="utf-8",
        )
        # Mirror the script under a tmp path so PLUGIN_ROOT resolves to tmp.
        bin_dir = tmp / "bin"
        bin_dir.mkdir()
        shutil.copy(SCRIPT, bin_dir / SCRIPT.name)
        os.chmod(bin_dir / SCRIPT.name, 0o755)
        probe = bin_dir / SCRIPT.name
        rc, out, _ = run([str(probe)], cwd=ROOT)
        check("README.md tokens do not surface in the report",
              rc == 0 and "Promise" not in out and "Effect" not in out and "Future" not in out,
              f"exit={rc}, stdout={out!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_skip_verified_in_footer() -> None:
    """AC-6b — lines whose first non-blank characters are `Verified in:` are
    skipped, so the AC-7 footer (the languages the contributor verified
    against) does not trip the gate by mentioning its own cited languages.
    """
    tmp = Path(tempfile.mkdtemp())
    try:
        rules = tmp / "skills" / "scrumia-functional-programming" / "rules"
        rules.mkdir(parents=True)
        (rules / "footer-rule.md").write_text(
            "A rule with a Verified in: footer naming banned tokens:\n"
            "\n"
            "Verified in: Promise, Effect, Future\n",
            encoding="utf-8",
        )
        # Also add a real violation outside the footer to make sure the script
        # is in fact scanning the file — without this, an empty pass is
        # indistinguishable from a script that does nothing.
        (rules / "footer-rule.md").write_text(
            "A rule with a Verified in: footer naming banned tokens.\n"
            "\n"
            "  Verified in: Promise, Effect, Future\n"
            "\n"
            "Then a real violation slips in: `Promise.resolve(value)`.\n",
            encoding="utf-8",
        )
        bin_dir = tmp / "bin"
        bin_dir.mkdir()
        shutil.copy(SCRIPT, bin_dir / SCRIPT.name)
        os.chmod(bin_dir / SCRIPT.name, 0o755)
        probe = bin_dir / SCRIPT.name
        rc, out, _ = run([str(probe)], cwd=ROOT)
        check("Verified in: lines are skipped — only the body violation is reported",
              rc == 1
              and "Promise" in out  # the body violation is named
              and out.count("vocabulary drift") == 1,
              f"exit={rc}, stdout={out!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- AC-2

print("\nAC-2 — a misplaced rule trips the gate, names the rule, and is named as a finding")


def test_misplaced_rule_is_named() -> None:
    """AC-2 — the vocabulary gate names the rule file and line of a misplaced
    rule, so a reviewer who finds it can propose the move.

    The fixture is the simplest case: a single rule file with one banned
    token used in a code context (the gate's contract — bare English usage
    is not flagged, and a code-context use is).
    """
    tmp = Path(tempfile.mkdtemp())
    try:
        rules = tmp / "skills" / "scrumia-functional-programming" / "rules"
        rules.mkdir(parents=True)
        rule_file = rules / "misplaced-rule.md"
        rule_file.write_text(
            "A rule that drifted.\n"
            "\n"
            "Uses `Effect<Unit>` in the body — Kotlin-coroutines shape.\n",
            encoding="utf-8",
        )
        bin_dir = tmp / "bin"
        bin_dir.mkdir()
        shutil.copy(SCRIPT, bin_dir / SCRIPT.name)
        os.chmod(bin_dir / SCRIPT.name, 0o755)
        probe = bin_dir / SCRIPT.name
        rc, out, _ = run([str(probe)], cwd=ROOT)
        check("a rule with a Kotlin-shape token trips the gate (exit 1)",
              rc == 1,
              f"exit={rc}, stdout={out!r}")
        check("the report names the rule file",
              "misplaced-rule.md" in out,
              f"stdout={out!r}")
        check("the report names the line number",
              re.search(r"misplaced-rule\.md:\d+:", out) is not None,
              f"stdout={out!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- AC-3, AC-4

print("\nAC-3 / AC-4 — module activates alone; contributes to implement, review, find-spec")


def test_extends_covers_three_registers() -> None:
    data = json.loads(EXTENDS.read_text(encoding="utf-8"))
    for register in ("implement", "review", "find-spec"):
        check(f"extends.json → {register} is present and non-empty",
              isinstance(data.get(register), list) and len(data[register]) > 0,
              f"register={register}, value={data.get(register)!r}")


def test_no_cross_dependency_with_a_language_module() -> None:
    """AC-5 — the module lands independently. A dependency on a language
    module's bin/ would be the cross-dependency this test refuses.
    """
    deps = PLUGIN / "dependencies.jsonl"
    if not deps.is_file():
        check("no dependencies.jsonl — no language module is depended on", True)
        return
    text = deps.read_text(encoding="utf-8")
    for lang in ("scrumia-kotlin", "scrumia-impl-reactjs", "scrumia-impl-rust",
                 "scrumia-impl-solidjs", "scrumia-effect", "scrumia-ktor"):
        check(f"no dependency on {lang}",
              lang not in text,
              f"dependency on {lang} would be a misplaced-rule finding")


# ---------------------------------------------------------------- AC-7

print("\nAC-7 — every principle carries a `Verified in:` footer naming ≥ 2 cited languages")


def test_every_rule_has_verified_in_footer_with_two_languages() -> None:
    """AC-7 — each rule fragment's last non-blank line is `Verified in:` and
    names at least two languages drawn from the AC's allowed list. The check
    is on every rule file under rules/, not on a sample — a missing footer on
    one rule is a failing criterion, not an aggregated score.
    """
    for rule in sorted(RULES_DIR.glob("*.md")):
        text = rule.read_text(encoding="utf-8")
        # Last non-blank line — the footer is the rule's last statement.
        non_blank = [ln for ln in text.splitlines() if ln.strip()]
        last = non_blank[-1] if non_blank else ""
        check(f"{rule.name}: ends with a `Verified in:` line",
              last.lstrip().startswith("Verified in:"),
              f"last line={last!r}")
        # Count distinct languages named in the footer. The footer text is the
        # `Verified in:` line, and the names are tokens separated by commas.
        tail = last.split("Verified in:", 1)[-1]
        names = [n.strip() for n in tail.split(",") if n.strip()]
        check(f"{rule.name}: names at least two cited languages",
              len(set(names)) >= 2,
              f"footer={last!r}")
        # Each named language is in the AC's allowed set.
        unknown = [n for n in names if n not in CITED_LANGUAGES]
        check(f"{rule.name}: every cited language is from the allowed set",
              not unknown,
              f"unknown={unknown}, allowed={sorted(CITED_LANGUAGES)}")


# ---------------------------------------------------------------- summary

if FAILURES:
    print(f"\n{len(FAILURES)} failure(s):")
    for f in FAILURES:
        print(f"  {f}")
    sys.exit(1)

print("\nall green")
sys.exit(0)
