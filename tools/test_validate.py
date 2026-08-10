#!/usr/bin/env python3
"""Tests for tools/validate.py's link gate (#22).

Run from anywhere: python3 tools/test_validate.py
Exit code 0 when everything passes, 1 otherwise. No dependencies.

check_doc_links used to only walk docs/, plugins/ and README.md: a broken
relative link inside features/**/*.md passed with 0 errors. These checks run
the real function against a throwaway fixture tree, so the gate is proven by
a link that actually fails, not by reading the glob list.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as v  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ok   {name}")
    else:
        FAILURES.append(f"{name}{': ' + detail if detail else ''}")
        print(f"  FAIL {name}{': ' + detail if detail else ''}")


def run_doc_links(root: Path) -> list[str]:
    """Point check_doc_links at a fixture root instead of the repo.

    check_doc_links reads ROOT / "README.md" unconditionally (no glob, no
    existence check) — a fixture without one crashes the function it is
    trying to test rather than reporting a finding.
    """
    readme = root / "README.md"
    if not readme.exists():
        readme.write_text("# fixture\n", encoding="utf-8")
    v.ROOT = root
    v.ERRORS.clear()
    v.check_doc_links()
    return list(v.ERRORS)


def test_broken_link_under_features_is_caught() -> None:
    print("a broken relative link under features/ is now an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        feature.mkdir(parents=True)
        (feature / "business.md").write_text(
            "See [the ADR](../../../docs/adr/0000-does-not-exist.md).\n", encoding="utf-8"
        )
        errors = run_doc_links(tmp)
        check("features/**/*.md is walked and the dangling link is reported",
              any("business.md" in e and "broken link" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_valid_link_under_features_passes() -> None:
    print("a relative link under features/ that resolves is not flagged")
    tmp = Path(tempfile.mkdtemp())
    try:
        docs = tmp / "docs" / "adr"
        docs.mkdir(parents=True)
        (docs / "0001-real.md").write_text("# Real ADR\n", encoding="utf-8")
        feature = tmp / "features" / "business" / "widget"
        feature.mkdir(parents=True)
        (feature / "business.md").write_text(
            "See [the ADR](../../../docs/adr/0001-real.md).\n", encoding="utf-8"
        )
        errors = run_doc_links(tmp)
        check("no false positive on a link that resolves", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_repo_features_pass_the_real_gate() -> None:
    print("the repo's own features/**/*.md pass check_doc_links as it runs today")
    errors = run_doc_links(REPO)
    check("no broken link under the real features/ tree", errors == [], str(errors))


REAL_ROOT, REAL_MEMORY = v.ROOT, v.MEMORY_ROOT


def run_memory(root: Path) -> tuple[list[str], list[str]]:
    """Point check_memory_channel at a fixture tree instead of the repo's own."""
    v.ROOT, v.MEMORY_ROOT = root, root / ".claude" / "agent-memory"
    v.ERRORS.clear()
    v.WARNINGS.clear()
    try:
        v.check_memory_channel()
        return list(v.ERRORS), list(v.WARNINGS)
    finally:
        v.ROOT, v.MEMORY_ROOT = REAL_ROOT, REAL_MEMORY


def memory_fixture(tmp: Path, role: str, entries: dict[str, str], index: str) -> Path:
    d = tmp / ".claude" / "agent-memory" / role
    d.mkdir(parents=True, exist_ok=True)
    for name, body in entries.items():
        (d / name).write_text(body, encoding="utf-8")
    (d / "MEMORY.md").write_text(index, encoding="utf-8")
    return d


def entry(topic="t", source="agent", stale_when="never, in practice") -> str:
    lines = ["---", "name: e", "description: d", "metadata:", "  type: project"]
    for key, value in (("topic", topic), ("source", source), ("stale_when", stale_when)):
        if value is not None:
            lines.append(f"  {key}: {value}")
    return "\n".join(lines) + "\n---\n\nbody\n"


def test_index_omitting_a_present_file_is_caught() -> None:
    print("a memory file the index does not name is reported (AC-22)")
    tmp = Path(tempfile.mkdtemp())
    try:
        memory_fixture(tmp, "role-a", {"one.md": entry(), "two.md": entry()},
                       "- [one](one.md)\n")
        errors, _ = run_memory(tmp)
        check("the unnamed entry is flagged as invisible",
              any("two.md" in e and "does not name" in e for e in errors), str(errors))
        check("the named entry is not flagged",
              not any("names one.md" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_index_naming_an_absent_file_is_caught() -> None:
    print("an index naming a file that is not there is reported (AC-22)")
    tmp = Path(tempfile.mkdtemp())
    try:
        memory_fixture(tmp, "role-a", {"one.md": entry()},
                       "- [one](one.md)\n- [gone](gone.md)\n")
        errors, _ = run_memory(tmp)
        check("the dangling name is flagged",
              any("gone.md" in e and "not there" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_entry_without_an_expiry_condition_is_caught() -> None:
    print("an entry no stated condition can invalidate is reported (AC-19)")
    tmp = Path(tempfile.mkdtemp())
    try:
        memory_fixture(tmp, "role-a", {"one.md": entry(stale_when=None)},
                       "- [one](one.md)\n")
        errors, _ = run_memory(tmp)
        check("metadata.stale_when is required",
              any("one.md" in e and "stale_when" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_unattributable_human_ruling_is_caught() -> None:
    print("'human' with no handle and no date is not a provenance (AC-20)")
    tmp = Path(tempfile.mkdtemp())
    try:
        memory_fixture(tmp, "role-a",
                       {"bare.md": entry(source="human"), "ok.md": entry(source="human @tibs245 2026-08-09")},
                       "- [bare](bare.md)\n- [ok](ok.md)\n")
        errors, _ = run_memory(tmp)
        check("a bare 'human' is rejected",
              any("bare.md" in e and "source" in e for e in errors), str(errors))
        check("a handle and a date are accepted",
              not any("ok.md" in e and "source" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_two_roles_on_one_topic_are_reported() -> None:
    print("the same topic in two roles is surfaced, not refused (AC-21)")
    tmp = Path(tempfile.mkdtemp())
    try:
        memory_fixture(tmp, "role-a", {"one.md": entry(topic="scope-axis")}, "- [one](one.md)\n")
        memory_fixture(tmp, "role-b", {"two.md": entry(topic="scope-axis")}, "- [two](two.md)\n")
        errors, warnings = run_memory(tmp)
        check("the pair is reported as a warning",
              any("scope-axis" in w and "role-a" in w and "role-b" in w for w in warnings), str(warnings))
        check("holding one topic in two roles is not itself an error",
              errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_a_partially_tracked_channel_is_caught() -> None:
    print("one role's memory tracked while another's is not is a failure (AC-18)")
    tmp = Path(tempfile.mkdtemp())
    try:
        subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
        memory_fixture(tmp, "role-a", {"one.md": entry()}, "- [one](one.md)\n")
        memory_fixture(tmp, "role-b", {"two.md": entry()}, "- [two](two.md)\n")
        subprocess.run(["git", "add", ".claude/agent-memory/role-a"], cwd=tmp, check=True)
        errors, _ = run_memory(tmp)
        check("the untracked half is reported",
              any("two.md" in e and "untracked" in e for e in errors), str(errors))
        check("the tracked half is not",
              not any("one.md" in e and "untracked" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_repo_memory_channel_passes() -> None:
    print("the repo's own .claude/agent-memory/ passes the gate as it runs today")
    v.ERRORS.clear()
    v.WARNINGS.clear()
    v.check_memory_channel()
    check("no error in the real memory channel", v.ERRORS == [], str(v.ERRORS))
    v.ERRORS.clear()
    v.WARNINGS.clear()


def main() -> int:
    for test in (test_broken_link_under_features_is_caught,
                 test_valid_link_under_features_passes,
                 test_repo_features_pass_the_real_gate,
                 test_index_omitting_a_present_file_is_caught,
                 test_index_naming_an_absent_file_is_caught,
                 test_entry_without_an_expiry_condition_is_caught,
                 test_unattributable_human_ruling_is_caught,
                 test_two_roles_on_one_topic_are_reported,
                 test_a_partially_tracked_channel_is_caught,
                 test_repo_memory_channel_passes):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
