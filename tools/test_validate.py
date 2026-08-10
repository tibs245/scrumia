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


def main() -> int:
    for test in (test_broken_link_under_features_is_caught,
                 test_valid_link_under_features_passes,
                 test_repo_features_pass_the_real_gate):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
