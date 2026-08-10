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
import build_features_index as bfi  # noqa: E402

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


def run_check(root: Path, check_name: str) -> list[str]:
    """Point one validate.py check at a fixture root instead of the repo."""
    v.ROOT = root
    v.ERRORS.clear()
    getattr(v, check_name)()
    return list(v.ERRORS)


def make_template(root: Path) -> None:
    """The index-section template check_feature_index_sections parses its set from."""
    tpl_dir = root / "plugins" / "scrumia-specs" / "skills" / "scrumia-feature" / "assets"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    (tpl_dir / "index.template.md").write_text(
        "# <Feature name>\n\n"
        "## In brief\n\n<...>\n\n"
        "## Links\n\n<...>\n\n"
        "## Files present\n\n<...>\n\n"
        "## Open issues\n\n<...>\n",
        encoding="utf-8",
    )


def write_feature_index(feature: Path, sections: str = "") -> None:
    feature.mkdir(parents=True, exist_ok=True)
    (feature / "index.md").write_text(
        "# Widget\n\n**Status**: active\n\n## In brief\n\nDoes a thing.\n\n" + sections,
        encoding="utf-8",
    )


# --- check_feature_mandatory_files ---

def test_feature_missing_mandatory_file_is_caught() -> None:
    print("a leaf feature missing qa.md is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "business.md").write_text("# Widget rules\n", encoding="utf-8")
        (feature / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
        # qa.md deliberately absent
        errors = run_check(tmp, "check_feature_mandatory_files")
        check("missing qa.md is reported",
              any("missing mandatory file qa.md" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_feature_with_all_mandatory_files_passes() -> None:
    print("a leaf feature carrying index.md, qa.md, CHANGELOG.md, business.md passes")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "qa.md").write_text("# QA\n", encoding="utf-8")
        (feature / "business.md").write_text("# Widget rules\n", encoding="utf-8")
        (feature / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
        errors = run_check(tmp, "check_feature_mandatory_files")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


# --- check_feature_index_sections ---

def test_feature_index_invented_section_is_caught() -> None:
    print("an index.md heading outside the template's set is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        make_template(tmp)
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature, "## Rationale\n\nAn invented section.\n\n")
        errors = run_check(tmp, "check_feature_index_sections")
        check("invented section 'Rationale' is reported",
              any("section 'Rationale'" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_feature_index_conformant_sections_pass() -> None:
    print("an index.md using only the template's headings passes")
    tmp = Path(tempfile.mkdtemp())
    try:
        make_template(tmp)
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(
            feature,
            "## Links\n\n- none\n\n## Files present\n\n| File | Read it when |\n|---|---|\n\n"
            "## Open issues\n\n- none\n",
        )
        errors = run_check(tmp, "check_feature_index_sections")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


# --- check_feature_files_present ---

def test_files_present_table_names_absent_file_is_caught() -> None:
    print("a 'Files present' row naming a file absent from disk is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(
            feature,
            "## Files present\n\n| File | Read it when |\n|---|---|\n| `business.md` | always |\n",
        )
        # business.md is listed but never written to disk
        errors = run_check(tmp, "check_feature_files_present")
        check("listed-but-absent 'business.md' is reported",
              any("lists 'business.md'" in e and "not on disk" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_files_present_table_matches_disk_passes() -> None:
    print("a 'Files present' row matching a real file passes")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(
            feature,
            "## Files present\n\n| File | Read it when |\n|---|---|\n| `business.md` | always |\n",
        )
        (feature / "business.md").write_text("# Widget rules\n", encoding="utf-8")
        errors = run_check(tmp, "check_feature_files_present")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_file_on_disk_missing_from_table_is_caught() -> None:
    print("a file on disk absent from the 'Files present' table is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature, "## Files present\n\n| File | Read it when |\n|---|---|\n")
        (feature / "qa.md").write_text("# QA\n", encoding="utf-8")
        errors = run_check(tmp, "check_feature_files_present")
        check("present-but-unlisted 'qa.md' is reported",
              any("'qa.md'" in e and "missing from" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_absence_idiom_in_prose_is_not_a_table_row() -> None:
    print("prose absence idioms ('No `legal.md`: ...') are not read as table rows")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "app" / "site" / "widget"
        write_feature_index(
            feature,
            "## Files present\n\n| File | Read it when |\n|---|---|\n| `qa.md` | always |\n\n"
            "No `legal.md`: nothing regulated here. No `business.md`: no business parent.\n",
        )
        (feature / "qa.md").write_text("# QA\n", encoding="utf-8")
        errors = run_check(tmp, "check_feature_files_present")
        check("zero findings from the prose absence idiom", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


# --- check_global_index_drift ---

def test_global_index_stale_is_caught() -> None:
    print("a features/index.md that doesn't match the generator's output is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (tmp / "features" / "index.md").write_text("# stale content\n", encoding="utf-8")
        errors = run_check(tmp, "check_global_index_drift")
        check("drift is reported",
              any("drifted from the generator's output" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_global_index_current_passes() -> None:
    print("a features/index.md matching the generator's output passes")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (tmp / "features" / "index.md").write_text(bfi.generate_index(tmp), encoding="utf-8")
        errors = run_check(tmp, "check_global_index_drift")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_index_without_in_brief_yields_empty_brief() -> None:
    print("an index.md with no '## In brief' degrades to an empty brief, no crash")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        feature.mkdir(parents=True)
        (feature / "index.md").write_text("# Widget\n\n**Status**: active\n", encoding="utf-8")
        brief = bfi.parse_brief((feature / "index.md").read_text(encoding="utf-8"))
        check("empty brief", brief == "", repr(brief))
    finally:
        shutil.rmtree(tmp)


def test_global_index_itself_is_not_a_leaf() -> None:
    print("features/index.md is the global index, never a leaf feature")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (tmp / "features" / "index.md").write_text(bfi.generate_index(tmp), encoding="utf-8")
        leaves = bfi.find_leaf_features(tmp)
        check("one leaf only", [d.name for d in leaves] == ["widget"], str(leaves))
    finally:
        shutil.rmtree(tmp)


def main() -> int:
    for test in (test_broken_link_under_features_is_caught,
                 test_valid_link_under_features_passes,
                 test_repo_features_pass_the_real_gate,
                 test_feature_missing_mandatory_file_is_caught,
                 test_feature_with_all_mandatory_files_passes,
                 test_feature_index_invented_section_is_caught,
                 test_feature_index_conformant_sections_pass,
                 test_files_present_table_names_absent_file_is_caught,
                 test_files_present_table_matches_disk_passes,
                 test_file_on_disk_missing_from_table_is_caught,
                 test_absence_idiom_in_prose_is_not_a_table_row,
                 test_global_index_stale_is_caught,
                 test_global_index_current_passes,
                 test_index_without_in_brief_yields_empty_brief,
                 test_global_index_itself_is_not_a_leaf):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
