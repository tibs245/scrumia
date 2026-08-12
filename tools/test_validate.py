#!/usr/bin/env python3
"""Tests for tools/validate.py — the gate's own rules, and what it delegates.

Run from anywhere: python3 tools/test_validate.py
Exit code 0 when everything passes, 1 otherwise. No dependencies.

Every check runs against a throwaway fixture tree, so it is proven by an input that
actually fails rather than by reading the glob list. The delegation is held to the same
bar from both sides: a rule this gate stopped applying is shown coming back through
`scrumia-module`, and one it kept is shown not being asked twice.
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


# --- containment: a plugin reaches nothing outside itself (ADR-0018), through the
# procedural check now rather than through this gate's own code ---

def write_plugin_skill(root: Path, body: str, plugin: str = "scrumia-widget") -> Path:
    skill = root / "plugins" / plugin / "skills" / "scrumia-do"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(body, encoding="utf-8")
    return skill


def install_checker(root: Path) -> None:
    """The real scrumia-module, where check_module_anatomy looks for it in a fixture root.

    Copied rather than stubbed: a fixture checker would test this gate against a verdict
    nothing else produces, which is the failure delegating was meant to end.
    """
    bin_dir = root / "plugins" / "scrumia-core" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO / "plugins" / "scrumia-core" / "bin" / "scrumia-module", bin_dir)


CONFORMANT_README = (
    "# scrumia-widget\n\nDoes the one thing its name says.\n\n"
    "## What it answers\n\nWhether the widget is on.\n\n"
    "## What it refuses\n\nTurning it off.\n\n"
    "## What it ships\n\n| Skill | Does |\n|---|---|\n| `scrumia-do` | it |\n"
)


def write_module(root: Path, name: str = "scrumia-widget") -> Path:
    """A directory the procedural check will accept as a module and find nothing wrong with."""
    plugin = root / "plugins" / name
    write_manifest(plugin, "0.4.0")
    (plugin / "README.md").write_text(CONFORMANT_README, encoding="utf-8")
    return plugin


def test_doc_links_leaves_plugins_to_the_procedural_check() -> None:
    print("check_doc_links no longer resolves inside plugins/ — one rule, one place (AC-5)")
    tmp = Path(tempfile.mkdtemp())
    try:
        (tmp / "docs").mkdir(parents=True)
        (tmp / "docs" / "agents.md").write_text("# Agents\n", encoding="utf-8")
        write_plugin_skill(tmp, "See [the roles](../../../../docs/agents.md) and "
                                "[nothing](references/gone.md).\n")
        errors = run_doc_links(tmp)
        check("neither the escaping link nor the dangling one is reported twice",
              errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_delegation_still_catches_what_the_gate_stopped_checking() -> None:
    print("the rules this gate deleted come back through scrumia-module, not from nowhere")
    tmp = Path(tempfile.mkdtemp())
    try:
        install_checker(tmp)
        plugin = write_module(tmp)
        write_plugin_skill(tmp, "See [the other](../../../scrumia-other/README.md).\n")
        (plugin / "bin").mkdir()
        (plugin / "bin" / "scrumia-widget-tool").write_text("#!/bin/sh\n", encoding="utf-8")
        errors = run_check(tmp, "check_module_anatomy")
        check("the sibling reach is reported, qualified by the feature owning the rule",
              any("modular-composition/BR-7" in e and "outside the module" in e for e in errors),
              str(errors))
        check("the name on PATH that cannot run is reported",
              any("scrumia-widget-tool" in e and "not executable" in e for e in errors),
              str(errors))
        check("each finding names the module and the file, repo-relative",
              all(e.startswith("plugins/scrumia-widget/") for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_a_conformant_module_produces_no_finding() -> None:
    print("a module meeting the standard passes the delegation — the rule does not over-reach")
    tmp = Path(tempfile.mkdtemp())
    try:
        install_checker(tmp)
        write_module(tmp)
        errors = run_check(tmp, "check_module_anatomy")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_a_delegated_finding_fails_the_gate() -> None:
    print("a module with no README is a finding, and a finding fails the gate (AC-6)")
    tmp = Path(tempfile.mkdtemp())
    try:
        install_checker(tmp)
        (write_module(tmp) / "README.md").unlink()
        v.WARNINGS.clear()
        errors = run_check(tmp, "check_module_anatomy")
        check("the missing README is reported through the delegation",
              any("README.md" in e and "module-anatomy/BR-4" in e for e in errors), str(errors))
        # main() returns 1 on ERRORS and 0 on WARNINGS, so which list it lands in is
        # the whole of "a finding fails the gate".
        check("as an error, which is what makes the run exit non-zero",
              list(v.WARNINGS) == [], str(v.WARNINGS))
    finally:
        shutil.rmtree(tmp)


def test_the_gate_says_so_when_the_checker_is_missing() -> None:
    print("no checker on disk is an error — a gate with nothing to delegate to is not clean")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_module(tmp)
        errors = run_check(tmp, "check_module_anatomy")
        check("the missing checker is reported",
              any("scrumia-module" in e and "missing" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_a_published_name_resolving_nowhere_is_still_caught() -> None:
    print("a dangling bin/ symlink: BR-7's clause the checker misses, kept here until #312")
    tmp = Path(tempfile.mkdtemp())
    try:
        bin_dir = tmp / "plugins" / "scrumia-widget" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "scrumia-ghost").symlink_to("../scripts/gone.sh")
        errors = run_check(tmp, "check_published_names")
        check("the name resolving nowhere is reported",
              any("scrumia-ghost" in e and "resolving nowhere" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_a_working_published_name_is_not_flagged() -> None:
    print("a bin/ entry that resolves is untouched — executability is the checker's")
    tmp = Path(tempfile.mkdtemp())
    try:
        bin_dir = tmp / "plugins" / "scrumia-widget" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "scrumia-real").write_text("#!/bin/sh\n", encoding="utf-8")
        errors = run_check(tmp, "check_published_names")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_a_run_that_could_not_conclude_is_not_read_as_clean() -> None:
    print("state, never the finding count: exit 1 is the tool failing, not a clean module")
    tmp = Path(tempfile.mkdtemp())
    try:
        install_checker(tmp)
        plugin = write_module(tmp)
        (plugin / ".claude-plugin" / "plugin.json").write_text("{ not json", encoding="utf-8")
        errors = run_check(tmp, "check_module_anatomy")
        check("the run is reported as one that could not conclude",
              any("could not conclude" in e for e in errors), str(errors))
        check("and it is not silently folded into an empty finding list",
              errors != [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_a_directory_that_is_not_a_module_is_not_judged() -> None:
    print("plugins/ also holds caches — a directory with no manifest is skipped, not judged")
    tmp = Path(tempfile.mkdtemp())
    try:
        install_checker(tmp)
        write_module(tmp)
        (tmp / "plugins" / ".cache" / "stuff").mkdir(parents=True)
        errors = run_check(tmp, "check_module_anatomy")
        check("no verdict is demanded of it", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_every_module_is_checked_including_the_one_shipping_the_checker() -> None:
    print("the loop covers every module, the checker's own included — no exemption (AC-3)")
    tmp = Path(tempfile.mkdtemp())
    try:
        install_checker(tmp)
        write_module(tmp)
        write_module(tmp, "scrumia-other")
        (tmp / "plugins" / "scrumia-other" / "README.md").unlink()
        write_manifest(tmp / "plugins" / "scrumia-core", "0.4.0")
        errors = run_check(tmp, "check_module_anatomy")
        check("the module owning the checker is judged like any other",
              any(e.startswith("plugins/scrumia-core/") for e in errors), str(errors))
        check("a later module is reached, so the loop does not stop at the first verdict",
              any(e.startswith("plugins/scrumia-other/") for e in errors), str(errors))
        check("and the conformant one draws nothing",
              not any(e.startswith("plugins/scrumia-widget/") for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_the_real_marketplace_passes_the_delegation() -> None:
    print("every module this repository ships meets the standard as the gate now applies it")
    errors = run_check(REPO, "check_module_anatomy")
    check("no finding on any shipped module", errors == [], str(errors))


def test_canonical_url_naming_no_file_is_caught() -> None:
    print("a canonical blob URL pointing at nothing is an error — the escape hatch is gated too")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin_skill(tmp, f"See [the ADR]({v.CANONICAL_BLOB}docs/adr/9999-nope.md).\n")
        errors = run_doc_links(tmp)
        check("the dangling URL is reported",
              any("canonical URL names no file" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_canonical_url_naming_a_real_file_passes() -> None:
    print("a canonical blob URL naming a file that exists passes")
    tmp = Path(tempfile.mkdtemp())
    try:
        (tmp / "docs" / "adr").mkdir(parents=True)
        (tmp / "docs" / "adr" / "0018-real.md").write_text("# Real\n", encoding="utf-8")
        write_plugin_skill(tmp, f"See [the ADR]({v.CANONICAL_BLOB}docs/adr/0018-real.md).\n")
        errors = run_doc_links(tmp)
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


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
        "## Files present\n\n<...>\n",
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
            "## Links\n\n- none\n\n## Files present\n\n| File | Read it when |\n|---|---|\n",
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


def test_app_feature_missing_business_md_is_caught() -> None:
    print("an app-stratum leaf without business.md is an error — every feature states its value")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "app" / "site" / "widget"
        write_feature_index(feature)
        (feature / "qa.md").write_text("# QA\n", encoding="utf-8")
        (feature / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
        errors = run_check(tmp, "check_feature_mandatory_files")
        check("missing business.md is reported",
              any("missing mandatory file business.md" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_ticket_reference_in_a_spec_is_caught() -> None:
    print("a #NN ticket reference outside CHANGELOG.md is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "qa.md").write_text("# QA\n\nFixed in #26.\n", encoding="utf-8")
        errors = run_check(tmp, "check_no_tracker_refs")
        check("ticket reference is reported",
              any("ticket reference #26" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_hex_colour_and_changelog_refs_are_not_tickets() -> None:
    print("hex colours (#9E4517) and CHANGELOG.md issue refs produce zero findings")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "legal.md").write_text("# Legal\n\nThe hue pair (`#9E4517` / `#F0996F`).\n", encoding="utf-8")
        (feature / "CHANGELOG.md").write_text("## 2026-08-10 — x\n- Issue: #193\n", encoding="utf-8")
        errors = run_check(tmp, "check_no_tracker_refs")
        check("zero findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_business_without_value_heading_is_caught() -> None:
    print("a business.md with no '## Value' content is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "business.md").write_text("# Widget rules\n\n## Rules\n\nA rule.\n", encoding="utf-8")
        errors = run_check(tmp, "check_business_value_heading")
        check("missing Value section is reported",
              any("no '## Value' section" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_ticket_url_reference_is_caught() -> None:
    print("a GitHub issue URL in a spec is a ticket reference too")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "tech.md").write_text(
            "# Tech\n\nSee https://github.com/acme/repo/issues/42 for the story.\n", encoding="utf-8")
        errors = run_check(tmp, "check_no_tracker_refs")
        check("URL reference is reported",
              any("github.com/acme/repo/issues/42" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_long_digit_run_is_not_a_ticket() -> None:
    print("a six-digit colour literal (#000000) is not a ticket number")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "tech.md").write_text("# Tech\n\nThe ink is `#000000` everywhere.\n", encoding="utf-8")
        errors = run_check(tmp, "check_no_tracker_refs")
        check("zero findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_qa_without_criterion_shape_is_caught() -> None:
    print("a qa.md with prose criteria and no '### AC-<n>' heading is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "qa.md").write_text("# QA\n\n## AC-1\n\nIt should work well.\n", encoding="utf-8")
        errors = run_check(tmp, "check_qa_shape")
        check("shape violation is reported",
              any("no '### AC-<n>' criterion heading" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_qa_with_fenced_criteria_passes() -> None:
    print("a qa.md of '### AC-<n>' headings each with a fenced scenario passes")
    tmp = Path(tempfile.mkdtemp())
    try:
        feature = tmp / "features" / "business" / "widget"
        write_feature_index(feature)
        (feature / "qa.md").write_text(
            "# QA\n\n### AC-1 — It fails when it should\n\n```gherkin\nGiven x\nWhen y\nThen z\n```\n",
            encoding="utf-8")
        errors = run_check(tmp, "check_qa_shape")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


# --- check_spec_changelogs ---

SPEC_ENTRY = (
    "# Changelog — widget\n\n"
    "## 2026-08-10 — The widget states its boundary\n"
    "- Issue: #42\n"
    "- Category: Changed\n"
    "- Breaking: no\n"
)


def write_spec_changelog(root: Path, body: str) -> Path:
    feature = root / "features" / "business" / "widget"
    write_feature_index(feature)
    (feature / "CHANGELOG.md").write_text(body, encoding="utf-8")
    return feature


def test_spec_entry_with_pr_line_is_caught() -> None:
    print("a spec entry carrying a PR: line is an error, whatever its value")
    for value in ("#48", "#NN (filled at merge)", "(filled at merge)", "TBD"):
        tmp = Path(tempfile.mkdtemp())
        try:
            write_spec_changelog(tmp, SPEC_ENTRY.replace(
                "- Breaking: no\n", f"- PR: {value}\n- Breaking: no\n"))
            errors = run_check(tmp, "check_spec_changelogs")
            check(f"'PR: {value}' is reported",
                  any("PR:" in e for e in errors), str(errors))
        finally:
            shutil.rmtree(tmp)


def test_spec_entry_with_unfilled_placeholder_is_caught() -> None:
    print("a #NN placeholder in any field is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_spec_changelog(tmp, SPEC_ENTRY.replace("- Issue: #42", "- Issue: #NN"))
        errors = run_check(tmp, "check_spec_changelogs")
        check("#NN is reported", any("#NN" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_spec_entry_without_category_is_caught() -> None:
    print("a spec entry with no Category: line is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_spec_changelog(tmp, SPEC_ENTRY.replace("- Category: Changed\n", ""))
        errors = run_check(tmp, "check_spec_changelogs")
        check("the missing category is reported",
              any("exactly one Category" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_spec_entry_with_foreign_category_is_caught() -> None:
    print("Fixed and Security have no referent in a spec, so they are errors there")
    for value in ("Fixed", "Security", "Invented"):
        tmp = Path(tempfile.mkdtemp())
        try:
            write_spec_changelog(tmp, SPEC_ENTRY.replace("Category: Changed", f"Category: {value}"))
            errors = run_check(tmp, "check_spec_changelogs")
            check(f"'{value}' is reported",
                  any(f"category '{value}'" in e for e in errors), str(errors))
        finally:
            shutil.rmtree(tmp)


def test_spec_entry_with_bad_heading_is_caught() -> None:
    print("a heading that is not a date and a title is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_spec_changelog(tmp, SPEC_ENTRY.replace(
            "## 2026-08-10 — The widget states its boundary", "## Unreleased"))
        errors = run_check(tmp, "check_spec_changelogs")
        check("the malformed heading is reported",
              any("YYYY-MM-DD" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_conformant_spec_changelog_passes() -> None:
    print("a conformant spec changelog, wrapped prose and free-text Breaking included")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_spec_changelog(tmp, SPEC_ENTRY.replace(
            "- Breaking: no\n",
            "- Breaking: no. The previous wording stays valid for readers of the\n"
            "  older guide, which is why nothing is dated here.\n"))
        errors = run_check(tmp, "check_spec_changelogs")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


# --- check_plugin_changelogs ---

PLUGIN_CHANGELOG = (
    "# Changelog — scrumia-widget\n\n"
    "## [Unreleased]\n\n"
    "## [0.4.0] - 2026-08-10\n"
    "### Added\n"
    "- The widget slot.\n"
)


def write_manifest(plugin: Path, version: str) -> None:
    manifest = plugin / ".claude-plugin"
    manifest.mkdir(parents=True, exist_ok=True)
    (manifest / "plugin.json").write_text(
        f'{{"name": "{plugin.name}", "version": "{version}"}}\n', encoding="utf-8")


def write_plugin(root: Path, body: str | None, version: str = "0.4.0") -> Path:
    plugin = root / "plugins" / "scrumia-widget"
    plugin.mkdir(parents=True, exist_ok=True)
    write_manifest(plugin, version)
    if body is not None:
        (plugin / "CHANGELOG.md").write_text(body, encoding="utf-8")
    return plugin


def test_plugin_without_changelog_is_caught() -> None:
    print("a shipped module with no changelog is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin(tmp, None)
        errors = run_check(tmp, "check_plugin_changelogs")
        check("the missing file is reported",
              any("missing CHANGELOG.md" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_plugin_second_changelog_is_caught() -> None:
    print("a skill-level changelog shadows the one a consumer reads")
    tmp = Path(tempfile.mkdtemp())
    try:
        plugin = write_plugin(tmp, PLUGIN_CHANGELOG)
        skill = plugin / "skills" / "scrumia-widget"
        skill.mkdir(parents=True)
        (skill / "CHANGELOG.md").write_text("# Changelog\n\n## [0.1.0] - 2026-01-01\n", encoding="utf-8")
        errors = run_check(tmp, "check_plugin_changelogs")
        check("the shadowing file is reported",
              any("shadows" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_plugin_bad_version_heading_is_caught() -> None:
    print("a plugin section heading that is not '[<version>] - date' is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin(tmp, PLUGIN_CHANGELOG.replace("## [0.4.0] - 2026-08-10", "## 0.4.0"))
        errors = run_check(tmp, "check_plugin_changelogs")
        check("the malformed heading is reported",
              any("[<version>]" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_plugin_foreign_category_is_caught() -> None:
    print("a category outside Keep a Changelog's six is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin(tmp, PLUGIN_CHANGELOG.replace("### Added", "### Improved"))
        errors = run_check(tmp, "check_plugin_changelogs")
        check("'Improved' is reported",
              any("category 'Improved'" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_plugin_entry_with_placeholder_is_caught() -> None:
    print("a #NN placeholder in a plugin changelog is an error too")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin(tmp, PLUGIN_CHANGELOG.replace("- The widget slot.", "- The widget slot, per #NN."))
        errors = run_check(tmp, "check_plugin_changelogs")
        check("#NN is reported", any("#NN" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_plugin_without_version_section_is_caught() -> None:
    print("a plugin changelog with no version section at all is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin(tmp, "# Changelog — scrumia-widget\n")
        errors = run_check(tmp, "check_plugin_changelogs")
        check("the empty changelog is reported",
              any("no version section" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_plugin_release_without_category_is_caught() -> None:
    print("a released version with bullets but no ### category is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin(tmp, "# Changelog — scrumia-widget\n\n## [Unreleased]\n\n"
                          "## [0.4.0] - 2026-08-10\n- did a thing\n")
        errors = run_check(tmp, "check_plugin_changelogs")
        check("the uncategorised release is reported",
              any("no category section" in e for e in errors), str(errors))
        check("[Unreleased] is not reported for being empty",
              not any("Unreleased" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_plugin_version_without_date_is_caught() -> None:
    print("a released version with no date is an error — Keep a Changelog requires one")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin(tmp, PLUGIN_CHANGELOG.replace("## [0.4.0] - 2026-08-10", "## [0.4.0]"))
        errors = run_check(tmp, "check_plugin_changelogs")
        check("the undated release is reported",
              any("[<version>]" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_banned_field_outside_an_entry_is_caught() -> None:
    print("a PR: line or a #NN in the preamble is on disk too, so it is an error")
    for preamble, needle in (("- PR: #48\n", "PR:"), ("Tracked in #NN.\n", "#NN")):
        tmp = Path(tempfile.mkdtemp())
        try:
            write_spec_changelog(tmp, SPEC_ENTRY.replace(
                "\n## 2026-08-10", f"\n{preamble}\n## 2026-08-10"))
            errors = run_check(tmp, "check_spec_changelogs")
            check(f"'{needle}' before the first entry is reported",
                  any(needle in e for e in errors), str(errors))
        finally:
            shutil.rmtree(tmp)


def test_spec_entry_missing_a_required_field_is_caught() -> None:
    print("an entry missing Issue: or Breaking: is an error, not only one missing Category:")
    for field in ("- Issue: #42\n", "- Breaking: no\n"):
        tmp = Path(tempfile.mkdtemp())
        try:
            write_spec_changelog(tmp, SPEC_ENTRY.replace(field, ""))
            errors = run_check(tmp, "check_spec_changelogs")
            check(f"the missing '{field.strip()}' is reported",
                  any("needs exactly one" in e for e in errors), str(errors))
        finally:
            shutil.rmtree(tmp)


def test_spec_entry_with_an_extra_field_is_caught() -> None:
    print("a field outside the three is an error — the entry carries three, and only three")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_spec_changelog(tmp, SPEC_ENTRY.replace(
            "- Breaking: no\n", "- Author: bob\n- Breaking: no\n"))
        errors = run_check(tmp, "check_spec_changelogs")
        check("'Author:' is reported", any("unknown field 'Author:'" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_empty_spec_changelog_is_caught() -> None:
    print("a spec changelog holding only its heading is an unwritten mandatory file")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_spec_changelog(tmp, "# Changelog — widget\n")
        errors = run_check(tmp, "check_spec_changelogs")
        check("the empty changelog is reported", any("no entry" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_changelog_outside_a_leaf_feature_is_reached() -> None:
    print("an EPIC directory with no index.md is walked too — it was escaping entirely")
    tmp = Path(tempfile.mkdtemp())
    try:
        epic = tmp / "features" / "app" / "site"
        epic.mkdir(parents=True)
        (epic / "CHANGELOG.md").write_text(
            "# Changelog — site\n\n## 2026-08-10 — A thing\n- Issue: #1\n- PR: #2\n"
            "- Category: Added\n- Breaking: no\n", encoding="utf-8")
        errors = run_check(tmp, "check_spec_changelogs")
        check("the non-leaf changelog is gated",
              any("PR:" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_changelog_behind_plugin_json_is_caught() -> None:
    print("a module bumped in plugin.json with no matching changelog section is an error")
    tmp = Path(tempfile.mkdtemp())
    try:
        plugin = write_plugin(tmp, PLUGIN_CHANGELOG)
        write_manifest(plugin, "0.5.0")
        errors = run_check(tmp, "check_plugin_changelogs")
        check("the stale changelog is reported",
              any("plugin.json declares 0.5.0" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_changelog_current_with_plugin_json_passes() -> None:
    print("the newest section matching plugin.json produces no finding")
    tmp = Path(tempfile.mkdtemp())
    try:
        plugin = write_plugin(tmp, PLUGIN_CHANGELOG)
        write_manifest(plugin, "0.4.0")
        errors = run_check(tmp, "check_plugin_changelogs")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_directory_without_a_manifest_is_not_a_module() -> None:
    print("plugins/ also holds caches — a directory with no plugin.json owes no changelog")
    tmp = Path(tempfile.mkdtemp())
    try:
        (tmp / "plugins" / ".cache").mkdir(parents=True)
        errors = run_check(tmp, "check_plugin_changelogs")
        check("no changelog is demanded of it", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def write_marketplace(root: Path, entry_version: str, top_version: str = "0.4.0") -> None:
    market = root / ".claude-plugin"
    market.mkdir(parents=True, exist_ok=True)
    (market / "marketplace.json").write_text(
        '{"version": "' + top_version + '", "plugins": [{"name": "scrumia-widget", '
        '"version": "' + entry_version + '", "source": "./plugins/scrumia-widget"}]}\n',
        encoding="utf-8")


def test_marketplace_version_mismatch_names_the_file_to_fix() -> None:
    print("plugin.json is the authority, so the error names marketplace.json as the one to fix")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_manifest(write_plugin(tmp, PLUGIN_CHANGELOG), "0.5.0")
        write_marketplace(tmp, "0.4.0")
        errors = run_check(tmp, "check_marketplace")
        check("the error names marketplace.json as the file to fix",
              any("fix marketplace.json" in e for e in errors), str(errors))
        check("it does not report a symmetric 'mismatch'",
              not any("version mismatch" in e for e in errors), str(errors))
    finally:
        shutil.rmtree(tmp)


def test_marketplace_agreeing_versions_pass() -> None:
    print("a module whose version differs from the marketplace's own is the normal state")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_manifest(write_plugin(tmp, PLUGIN_CHANGELOG), "0.5.0")
        write_marketplace(tmp, "0.5.0", top_version="0.4.0")
        v.ROOT = tmp
        v.ERRORS.clear()
        v.WARNINGS.clear()
        v.check_marketplace()
        check("no errors", list(v.ERRORS) == [], str(v.ERRORS))
        check("and no lockstep warning either", list(v.WARNINGS) == [], str(v.WARNINGS))
    finally:
        shutil.rmtree(tmp)


def test_plugin_keeps_fixed_and_security() -> None:
    print("Fixed and Security are legitimate for a module, unlike for a spec")
    tmp = Path(tempfile.mkdtemp())
    try:
        write_plugin(tmp, PLUGIN_CHANGELOG + "### Fixed\n- A thing.\n### Security\n- Another.\n")
        errors = run_check(tmp, "check_plugin_changelogs")
        check("no findings", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def test_template_placeholders_are_not_reached() -> None:
    print("the template legitimately carries #NN, and neither check walks it")
    tmp = Path(tempfile.mkdtemp())
    try:
        assets = tmp / "plugins" / "scrumia-specs" / "skills" / "scrumia-feature" / "assets"
        assets.mkdir(parents=True)
        (assets / "CHANGELOG.template.md").write_text(
            "# Changelog — <feature>\n\n## YYYY-MM-DD — <title>\n- Issue: #NN\n", encoding="utf-8")
        (tmp / "plugins" / "scrumia-specs" / "CHANGELOG.md").write_text(
            PLUGIN_CHANGELOG, encoding="utf-8")
        write_spec_changelog(tmp, SPEC_ENTRY)
        errors = run_check(tmp, "check_spec_changelogs") + run_check(tmp, "check_plugin_changelogs")
        check("no findings at all — the fixture is conformant", errors == [], str(errors))
    finally:
        shutil.rmtree(tmp)


def main() -> int:
    for test in (test_broken_link_under_features_is_caught,
                 test_valid_link_under_features_passes,
                 test_repo_features_pass_the_real_gate,
                 test_doc_links_leaves_plugins_to_the_procedural_check,
                 test_delegation_still_catches_what_the_gate_stopped_checking,
                 test_a_conformant_module_produces_no_finding,
                 test_a_delegated_finding_fails_the_gate,
                 test_the_gate_says_so_when_the_checker_is_missing,
                 test_a_published_name_resolving_nowhere_is_still_caught,
                 test_a_working_published_name_is_not_flagged,
                 test_a_run_that_could_not_conclude_is_not_read_as_clean,
                 test_a_directory_that_is_not_a_module_is_not_judged,
                 test_every_module_is_checked_including_the_one_shipping_the_checker,
                 test_the_real_marketplace_passes_the_delegation,
                 test_canonical_url_naming_no_file_is_caught,
                 test_canonical_url_naming_a_real_file_passes,
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
                 test_global_index_itself_is_not_a_leaf,
                 test_app_feature_missing_business_md_is_caught,
                 test_ticket_reference_in_a_spec_is_caught,
                 test_hex_colour_and_changelog_refs_are_not_tickets,
                 test_business_without_value_heading_is_caught,
                 test_ticket_url_reference_is_caught,
                 test_long_digit_run_is_not_a_ticket,
                 test_qa_without_criterion_shape_is_caught,
                 test_qa_with_fenced_criteria_passes,
                 test_spec_entry_with_pr_line_is_caught,
                 test_spec_entry_with_unfilled_placeholder_is_caught,
                 test_spec_entry_without_category_is_caught,
                 test_spec_entry_with_foreign_category_is_caught,
                 test_spec_entry_with_bad_heading_is_caught,
                 test_conformant_spec_changelog_passes,
                 test_plugin_without_changelog_is_caught,
                 test_plugin_second_changelog_is_caught,
                 test_plugin_bad_version_heading_is_caught,
                 test_plugin_foreign_category_is_caught,
                 test_plugin_entry_with_placeholder_is_caught,
                 test_plugin_without_version_section_is_caught,
                 test_plugin_release_without_category_is_caught,
                 test_plugin_version_without_date_is_caught,
                 test_banned_field_outside_an_entry_is_caught,
                 test_spec_entry_missing_a_required_field_is_caught,
                 test_spec_entry_with_an_extra_field_is_caught,
                 test_empty_spec_changelog_is_caught,
                 test_changelog_outside_a_leaf_feature_is_reached,
                 test_changelog_behind_plugin_json_is_caught,
                 test_changelog_current_with_plugin_json_passes,
                 test_directory_without_a_manifest_is_not_a_module,
                 test_marketplace_version_mismatch_names_the_file_to_fix,
                 test_marketplace_agreeing_versions_pass,
                 test_plugin_keeps_fixed_and_security,
                 test_template_placeholders_are_not_reached):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
