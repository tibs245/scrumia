#!/usr/bin/env python3
"""Validate the ScrumIA marketplace: manifests, skills, agents, commands, hooks, doc links.

Run from the repo root: python3 tools/validate.py
Exit code 0 when everything passes, 1 otherwise. No dependencies.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_features_index as bfi  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []
WARNINGS: list[str] = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        error(f"{path.relative_to(ROOT)}: missing")
    except json.JSONDecodeError as e:
        error(f"{path.relative_to(ROOT)}: invalid JSON — {e}")
    return None


def frontmatter(path: Path) -> dict[str, str] | None:
    """Parse the minimal YAML frontmatter used by skills and agents."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def check_marketplace() -> dict[str, dict]:
    """Marketplace entries and plugin directories must match one to one."""
    market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    if market is None:
        return {}

    entries = {p.get("name"): p for p in market.get("plugins", [])}
    dirs = {d.name for d in (ROOT / "plugins").iterdir() if d.is_dir()}

    for name in sorted(dirs - entries.keys()):
        error(f"plugins/{name}: present on disk but not registered in marketplace.json")
    for name in sorted(entries.keys() - dirs):
        error(f"marketplace.json: entry '{name}' has no plugins/{name} directory")

    for name, entry in entries.items():
        if name not in dirs:
            continue
        manifest = load_json(ROOT / "plugins" / name / ".claude-plugin" / "plugin.json")
        if manifest is None:
            continue
        if manifest.get("name") != name:
            error(f"plugins/{name}/plugin.json: name '{manifest.get('name')}' != directory")
        # Modules version independently, so only plugin.json can say which side is wrong.
        if manifest.get("version") != entry.get("version"):
            error(
                f"marketplace.json: entry '{name}' says {entry.get('version')} — "
                f"plugins/{name}/plugin.json declares {manifest.get('version')}, "
                f"and it is the authority; fix marketplace.json"
            )
        source = entry.get("source")
        if source != f"./plugins/{name}":
            error(f"marketplace.json: entry '{name}' source '{source}' is not ./plugins/{name}")
    return entries


def check_skills() -> None:
    """Every skills/<dir>/SKILL.md needs a frontmatter whose name matches the dir."""
    seen: dict[str, str] = {}
    for skill_md in sorted((ROOT / "plugins").glob("*/skills/*/SKILL.md")):
        rel = skill_md.relative_to(ROOT)
        fields = frontmatter(skill_md)
        if fields is None:
            error(f"{rel}: missing frontmatter")
            continue
        name = fields.get("name")
        description = fields.get("description")
        if not name:
            error(f"{rel}: frontmatter has no name")
        elif name != skill_md.parent.name:
            error(f"{rel}: frontmatter name '{name}' != directory '{skill_md.parent.name}'")
        if not description:
            error(f"{rel}: frontmatter has no description")
        if name:
            if name in seen:
                error(f"{rel}: skill name '{name}' already used by {seen[name]}")
            seen[name] = str(rel)
    for skill_dir in sorted((ROOT / "plugins").glob("*/skills/*/")):
        if not (skill_dir / "SKILL.md").exists():
            error(f"{skill_dir.relative_to(ROOT)}: skill directory without SKILL.md")


def check_agents() -> None:
    for agent_md in sorted((ROOT / "plugins").glob("*/agents/*.md")):
        rel = agent_md.relative_to(ROOT)
        fields = frontmatter(agent_md)
        if fields is None:
            error(f"{rel}: missing frontmatter")
            continue
        for key in ("name", "description"):
            if not fields.get(key):
                error(f"{rel}: frontmatter has no {key}")


def check_commands() -> None:
    """Every commands/<name>.md needs a description, and the names it cites must resolve."""
    known = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}
    known |= {s.parent.name for s in (ROOT / "plugins").glob("*/skills/*/SKILL.md")}
    # A published bin/ name is a hand-off like any other, and rots the same way.
    known |= {b.name for b in (ROOT / "plugins").glob("*/bin/*")}
    for cmd_md in sorted((ROOT / "plugins").glob("*/commands/*.md")):
        rel = cmd_md.relative_to(ROOT)
        fields = frontmatter(cmd_md)
        if fields is None:
            error(f"{rel}: missing frontmatter")
            continue
        if not fields.get("description"):
            error(f"{rel}: frontmatter has no description")
        # A command's whole job is handing off to a skill it names. A typo there sends
        # the agent to something that doesn't exist, and no other check would see it.
        for match in re.finditer(r"`(scrumia-[\w-]+)`", cmd_md.read_text(encoding="utf-8")):
            if match.group(1) not in known:
                error(f"{rel}: references '{match.group(1)}', which is no plugin or skill")


def check_hooks() -> None:
    for hooks_json in sorted((ROOT / "plugins").glob("*/hooks/hooks.json")):
        data = load_json(hooks_json)
        if data is None:
            continue
        text = json.dumps(data)
        for match in re.finditer(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)", text):
            script = hooks_json.parent.parent / match.group(1)
            rel = script.relative_to(ROOT)
            if not script.exists():
                error(f"{hooks_json.relative_to(ROOT)}: references missing file {rel}")
            elif not os.access(script, os.X_OK):
                error(f"{rel}: not executable (chmod +x)")


CANONICAL_BLOB = "https://github.com/tibs245/scrumia/blob/main/"


def containment_hint(resolved: Path) -> str:
    """The remedy differs by what's on the other side of the escape.

    A target still under plugins/ is another module — AC-11 bans citing it by any
    path, a canonical URL included, because only a published name is a real edge for
    the coverage calculation. A target outside plugins/ (docs/, features/) is exactly
    what the canonical-URL escape hatch exists for; offering it for the other case
    would send an author to fix one AC-11 violation by writing another.

    Resolved, same reason plugin_root_of is: on macOS a temp root is a symlink, and
    an unresolved plugins/ never contains a resolved child.
    """
    if resolved.is_relative_to((ROOT / "plugins").resolve()):
        return (
            "a module is installed one path segment deeper than it sits here, so this "
            "resolves somewhere else once installed — and a sibling module is cited by "
            "name, never by any path, canonical URL included (AC-11): publish a name "
            "under bin/, or name the module in prose instead"
        )
    return (
        "a module is installed one path segment deeper than it sits here, so this resolves "
        f"somewhere else once installed — publish a name under bin/, or cite {CANONICAL_BLOB}<path>"
    )


def plugin_root_of(rel: Path) -> Path | None:
    """The plugin a repo-relative path belongs to, or None outside plugins/.

    Resolved, because the targets it is compared against are: on macOS a temp root
    is a symlink, and an unresolved root never contains a resolved child.
    """
    if rel.parts[0] != "plugins" or len(rel.parts) < 2:
        return None
    return (ROOT / "plugins" / rel.parts[1]).resolve()


def check_doc_links() -> None:
    """Relative markdown links in docs/, plugins/ and features/ must resolve.

    Links may use ${CLAUDE_SKILL_DIR} (the only variable Claude Code substitutes
    inside skill content — ${CLAUDE_PLUGIN_ROOT} works in hooks.json/MCP configs
    only). We resolve it to the linking file's skill directory. A lingering
    ${CLAUDE_PLUGIN_ROOT} in a skill file is flagged: it would reach the agent
    unsubstituted.

    Inside plugins/, a link must also stay inside its own plugin (ADR-0018), and a
    canonical blob URL must name a file that exists — otherwise the escape hatch
    the rule opens becomes the next place links rot unchecked.
    """
    link_re = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
    for md in sorted([
        *ROOT.glob("docs/**/*.md"),
        *ROOT.glob("plugins/**/*.md"),
        *ROOT.glob("features/**/*.md"),
        ROOT / "README.md",
    ]):
        rel = md.relative_to(ROOT)
        plugin_dir = plugin_root_of(rel)
        skill_dir = None
        if rel.parts[0] == "plugins" and len(rel.parts) >= 4 and rel.parts[2] == "skills":
            skill_dir = ROOT / rel.parts[0] / rel.parts[1] / "skills" / rel.parts[3]
        for match in link_re.finditer(md.read_text(encoding="utf-8")):
            target = match.group(1)
            if target.startswith(CANONICAL_BLOB):
                cited = ROOT / target[len(CANONICAL_BLOB):]
                if not cited.exists():
                    error(f"{rel}: canonical URL names no file in this repo → {target}")
                continue
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("${CLAUDE_PLUGIN_ROOT}"):
                error(f"{rel}: ${{CLAUDE_PLUGIN_ROOT}} is not substituted in skill/doc content — use ${{CLAUDE_SKILL_DIR}} → {target}")
                continue
            if target.startswith("${CLAUDE_SKILL_DIR}"):
                if skill_dir is None:
                    error(f"{rel}: uses ${{CLAUDE_SKILL_DIR}} outside a skill directory → {target}")
                    continue
                resolved = (skill_dir / target[len("${CLAUDE_SKILL_DIR}/"):]).resolve()
            else:
                resolved = (md.parent / target).resolve()
            if plugin_dir is not None and not resolved.is_relative_to(plugin_dir):
                error(f"{rel}: link leaves plugins/{plugin_dir.name} → {target} — {containment_hint(resolved)}")
                continue
            if not resolved.exists():
                error(f"{rel}: broken link → {target}")


def check_skill_scripts() -> None:
    """Scripts a skill tells the agent to run must resolve, stay in the plugin, and be executable.

    check_doc_links only sees markdown links, so a ${CLAUDE_PLUGIN_ROOT} sitting
    in a bash block used to pass silently — and reach the agent unsubstituted.
    """
    plugin_root_re = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}")
    script_re = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/([\w./-]+\.(?:sh|py))")
    for md in sorted(ROOT.glob("plugins/**/SKILL.md")):
        rel = md.relative_to(ROOT)
        plugin_dir = plugin_root_of(rel)
        text = md.read_text(encoding="utf-8")
        if plugin_root_re.search(text):
            error(f"{rel}: ${{CLAUDE_PLUGIN_ROOT}} anywhere in a skill is not substituted — use ${{CLAUDE_SKILL_DIR}}")
        skill_dir = md.parent
        for match in script_re.finditer(text):
            script = (skill_dir / match.group(1)).resolve()
            if plugin_dir is not None and not script.is_relative_to(plugin_dir):
                error(f"{rel}: script call leaves plugins/{plugin_dir.name} → {match.group(0)} — {containment_hint(script)}")
                continue
            if not script.exists():
                error(f"{rel}: references missing script → {match.group(0)}")
            elif not os.access(script, os.X_OK):
                error(f"{script.relative_to(ROOT)}: not executable (chmod +x)")


def check_published_names() -> None:
    """Everything under a plugin's bin/ is executable: PATH is how another module reaches it."""
    for bin_dir in sorted((ROOT / "plugins").glob("*/bin")):
        for entry in sorted(bin_dir.iterdir()):
            rel = entry.relative_to(ROOT)
            if not entry.is_file():
                error(f"{rel}: bin/ holds published executables, nothing else")
            elif not os.access(entry, os.X_OK):
                error(f"{rel}: not executable (chmod +x) — a name on PATH that cannot run")


def check_french_leftovers() -> None:
    """The repo is English-only (site/fr/ excepted): flag leftover French prose."""
    accents = re.compile(r"[àâäçèéêëîïôöùûü]", re.IGNORECASE)
    for md in sorted([*ROOT.glob("docs/**/*.md"), *ROOT.glob("plugins/**/*.md"), ROOT / "README.md"]):
        text = md.read_text(encoding="utf-8")
        hits = accents.findall(text)
        if len(hits) > 3:  # tolerate proper nouns and borrowed words
            warn(f"{md.relative_to(ROOT)}: {len(hits)} accented characters — leftover French?")


def check_composition_drift() -> None:
    """The composition output shown on the site must match the real output from the script.

    The fixture is at tests/fixtures/composition-output.txt and serves as the gate.
    Drifts in .scrumia/config.yaml that aren't reflected here fail CI.
    """
    fixture_path = ROOT / "tests" / "fixtures" / "composition-output.txt"
    if not fixture_path.exists():
        error(f"{fixture_path.relative_to(ROOT)}: fixture missing — run compose-status.sh and commit the output")
        return

    script_path = ROOT / "plugins" / "scrumia-core" / "scripts" / "compose-status.sh"
    if not script_path.exists():
        error(f"{script_path.relative_to(ROOT)}: script missing")
        return

    try:
        result = subprocess.run(
            ["bash", str(script_path)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=5
        )
        real_output = result.stdout
    except subprocess.TimeoutExpired:
        error(f"{script_path.relative_to(ROOT)}: script timed out")
        return
    except Exception as e:
        error(f"{script_path.relative_to(ROOT)}: failed to run — {e}")
        return

    fixture_content = fixture_path.read_text(encoding="utf-8")

    if real_output.strip() != fixture_content.strip():
        error(
            f"{fixture_path.relative_to(ROOT)}: output drifted from the real composition. "
            f"Run 'bash plugins/scrumia-core/scripts/compose-status.sh > tests/fixtures/composition-output.txt' "
            f"to update the fixture."
        )
        return

    # Nobody reads the fixture; the page renders the string below. Gating only
    # the fixture lets the site show a stale composition with the check green.
    for lang in ("en", "fr"):
        page_strings = ROOT / "site" / "i18n" / lang / "index.json"
        try:
            shown = json.loads(page_strings.read_text(encoding="utf-8")).get("install_composition_output")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            error(f"{page_strings.relative_to(ROOT)}: unreadable — {e}")
            continue
        if shown is None:
            error(f"{page_strings.relative_to(ROOT)}: no 'install_composition_output' to check")
        elif shown.strip() != fixture_content.strip():
            error(
                f"{page_strings.relative_to(ROOT)}: 'install_composition_output' does not match "
                f"{fixture_path.relative_to(ROOT)} — the page would show a composition this repo does not have"
            )


DEPRECATED_APP_KEYS = ("implementation", "practices")


def check_deprecated_composition_keys() -> None:
    """Warn once when .scrumia/config.yaml still carries what extends: replaced (ADR-0019).

    Both spellings are read during the deprecation window, so this warns rather than
    errors — a project mid-migration still passes CI. Matched structurally (which
    top-level section a line sits in), never on the word alone: settings.practices.<module>
    and settings.implementation.<module> are settings namespaces a practice or
    implementation module still reads, not the retired slot keys that happen to share a
    word with them (same trap the scrumia-init migration itself had to name).
    """
    config_path = ROOT / ".scrumia" / "config.yaml"
    if not config_path.exists():
        return

    found: set[str] = set()
    section: str | None = None
    for raw in config_path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not raw[:1].isspace():
            section = line.split(":", 1)[0].strip()
            if section == "composition":
                found.add("composition:")
            continue
        if section == "apps":
            key = line.strip().split(":", 1)[0]
            if key in DEPRECATED_APP_KEYS:
                found.add(f"apps[].{key}:")

    if found:
        warn(
            f"{config_path.relative_to(ROOT)}: still uses deprecated "
            f"{', '.join(sorted(found))} — extends: replaces them (ADR-0019); both "
            f"spellings are read for now, but run scrumia-init to convert this project"
        )


CROSS_MODULE_PATH_RE = re.compile(r"\bplugins/([\w-]+)/")


def check_module_citations_by_name() -> None:
    """A module cites another only by the name the harness resolves, never a path.

    check_doc_links and check_skill_scripts already gate a link or script call that
    leaves its own plugin (ADR-0018) — resolution and containment. This is narrower and
    additional: even a path that would resolve is banned, in prose that is neither a
    markdown link nor a script call — the class of citation those two checks do not see,
    because a plugin literally spelling out another module's path can sit in a fenced
    example block with no link syntax at all. A path cannot be counted as a real edge by
    the coverage calculation modular-composition/qa.md AC-2 depends on; naming is what
    AC-11 requires instead.

    Matches only a trailing-slash form (plugins/<module>/…), so prose that legitimately
    needs to show the banned shape — a rule stating what not to write — can still do so
    by using plugins/<module> with no slash, or the literal placeholder plugins/<module>/.
    """
    for md in sorted(ROOT.glob("plugins/**/*.md")):
        rel = md.relative_to(ROOT)
        own_plugin = plugin_root_of(rel)
        if own_plugin is None:
            continue
        text = md.read_text(encoding="utf-8")
        for match in CROSS_MODULE_PATH_RE.finditer(text):
            cited = match.group(1)
            if cited == own_plugin.name:
                continue  # a module citing its own path is not a cross-module citation
            error(
                f"{rel}: cites '{cited}' by a path (plugins/{cited}/…) — name the module "
                f"instead, in prose the harness resolves (AC-11); a path is not a real "
                f"edge the coverage calculation can count"
            )


def check_feature_mandatory_files() -> None:
    """Every leaf feature carries index.md, qa.md, CHANGELOG.md and business.md.

    Per the catalog's existence categories (plugins/scrumia-specs/.../catalog.md):
    all four are unconditional — every feature states its value in business.md.
    """
    for feature_dir in bfi.find_leaf_features(ROOT):
        rel = feature_dir.relative_to(ROOT)
        for name in ["index.md", "qa.md", "CHANGELOG.md", "business.md"]:
            if not (feature_dir / name).exists():
                error(f"{rel}: missing mandatory file {name}")


# #NN with 1-4 digits: repo ticket numbers. 5+ digit runs (#000000) are colour
# literals, not tickets. URLs and "issue NN" spellings are tickets too.
TICKET_REF_RES = [
    re.compile(r"#\d{1,4}\b(?![0-9a-fA-F])"),
    re.compile(r"github\.com/[\w./-]+/(?:issues|pull)/\d+"),
    re.compile(r"\bissues?\s+#?\d+\b", re.IGNORECASE),
]


def check_no_tracker_refs() -> None:
    """A spec cites no ticket: issue/PR numbers live in the tracker and the changelog only."""
    features_root = ROOT / "features"
    for path in sorted(features_root.rglob("*.md")):
        if path.name == "CHANGELOG.md":
            continue
        rel = path.relative_to(ROOT)
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pattern in TICKET_REF_RES:
                for m in pattern.finditer(line):
                    error(f"{rel}:{i}: ticket reference {m.group(0)} — only CHANGELOG.md cites issues or PRs")


def check_business_value_heading() -> None:
    """Every business.md opens its value: a '## Value' heading with non-empty content."""
    for feature_dir in bfi.find_leaf_features(ROOT):
        path = feature_dir / "business.md"
        if not path.exists():
            continue  # check_feature_mandatory_files already reports this
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        m = re.search(r"^## Value\s*\n(.*?)(?=\n## |\Z)", text, re.MULTILINE | re.DOTALL)
        if not m or not m.group(1).strip():
            error(f"{rel}: no '## Value' section with content — every feature states who it is for, "
                  f"what it brings, why it matters, and whether that is measured")


def check_qa_shape() -> None:
    """qa.md carries identified criteria: '### AC-<n>' headings, each with a fenced scenario."""
    for feature_dir in bfi.find_leaf_features(ROOT):
        path = feature_dir / "qa.md"
        if not path.exists():
            continue  # check_feature_mandatory_files already reports this
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        headings = re.findall(r"^### (AC-\d+)\b.*$", text, re.MULTILINE)
        if not headings:
            error(f"{rel}: no '### AC-<n>' criterion heading — acceptance criteria carry stable identifiers")
            continue
        sections = re.split(r"^### AC-\d+\b.*$", text, flags=re.MULTILINE)[1:]
        for ac, body in zip(headings, sections):
            if "```" not in body:
                error(f"{rel}: {ac} has no fenced scenario — a criterion is a Given/When/Then that can fail")


GUARDRAIL_BUSINESS_LINES = 200
GUARDRAIL_QA_CRITERIA = 12


def check_splitting_guardrails() -> None:
    """ADR-0004's guardrails, surfaced as warnings so the fourth breach is not silent."""
    for feature_dir in bfi.find_leaf_features(ROOT):
        rel = feature_dir.relative_to(ROOT)
        business = feature_dir / "business.md"
        if business.exists():
            lines = len(business.read_text(encoding="utf-8").splitlines())
            if lines > GUARDRAIL_BUSINESS_LINES:
                warn(f"{rel}/business.md: {lines} lines against the ~{GUARDRAIL_BUSINESS_LINES} splitting guardrail")
        qa = feature_dir / "qa.md"
        if qa.exists():
            count = len(re.findall(r"^### AC-\d+\b", qa.read_text(encoding="utf-8"), re.MULTILINE))
            if count > GUARDRAIL_QA_CRITERIA:
                warn(f"{rel}/qa.md: {count} criteria against the ~{GUARDRAIL_QA_CRITERIA} splitting guardrail")


def check_feature_index_sections() -> None:
    """A leaf index.md's ## headings must be within the set the template declares.

    The allowed set is parsed from the template, never a second hardcoded list —
    so the two cannot drift from each other.
    """
    template_path = (
        ROOT / "plugins" / "scrumia-specs" / "skills" / "scrumia-feature"
        / "assets" / "index.template.md"
    )
    if not template_path.exists():
        error(f"{template_path.relative_to(ROOT)}: missing — cannot determine the index section set")
        return
    heading_re = re.compile(r"^## (.+)$", re.MULTILINE)
    allowed = set(heading_re.findall(template_path.read_text(encoding="utf-8")))
    for feature_dir in bfi.find_leaf_features(ROOT):
        index_md = feature_dir / "index.md"
        if not index_md.exists():
            continue  # check_feature_mandatory_files already reports this
        rel = index_md.relative_to(ROOT)
        for heading in heading_re.findall(index_md.read_text(encoding="utf-8")):
            if heading not in allowed:
                error(f"{rel}: section '{heading}' is not in the template's set {sorted(allowed)}")


def check_feature_files_present() -> None:
    """The 'Files present' table's entries must match the feature's real files, both directions.

    Only markdown table rows count — a line starting with '|' whose first cell is
    backticked. A prose mention of a filename (including the "No `legal.md`: ..."
    absence idiom) is not a row and must not be read as one.
    """
    section_re = re.compile(r"^## Files present\s*\n(.*?)(?=\n## |\Z)", re.MULTILINE | re.DOTALL)
    row_re = re.compile(r"^\|\s*`([^`]+)`\s*\|")
    for feature_dir in bfi.find_leaf_features(ROOT):
        index_md = feature_dir / "index.md"
        if not index_md.exists():
            continue  # check_feature_mandatory_files already reports this
        rel = feature_dir.relative_to(ROOT)
        section = section_re.search(index_md.read_text(encoding="utf-8"))
        listed: set[str] = set()
        if section:
            for line in section.group(1).splitlines():
                match = row_re.match(line.strip())
                if match:
                    listed.add(match.group(1))
        actual = {p.name for p in feature_dir.iterdir() if p.is_file() and p.name != "index.md"}
        for name in sorted(listed - actual):
            error(f"{rel}/index.md: 'Files present' lists '{name}', which is not on disk")
        for name in sorted(actual - listed):
            error(f"{rel}/index.md: '{name}' is on disk but missing from 'Files present'")


def check_global_index_drift() -> None:
    """features/index.md must match tools/build_features_index.py's output, recomputed in memory.

    Same pattern as check_composition_drift: nobody reads the generator's source to
    know if the committed file is current, so the gate recomputes rather than trusts it.
    """
    index_path = ROOT / "features" / "index.md"
    if not index_path.exists():
        error(f"{index_path.relative_to(ROOT)}: missing — run python3 tools/build_features_index.py")
        return
    real = bfi.generate_index(ROOT)
    committed = index_path.read_text(encoding="utf-8")
    if real.strip() == committed.strip():
        return
    real_lines = real.splitlines()
    committed_lines = committed.splitlines()
    divergent = next(
        (b for a, b in zip(real_lines, committed_lines) if a != b),
        (committed_lines[len(real_lines):] or real_lines[len(committed_lines):] or [""])[0],
    )
    error(
        f"{index_path.relative_to(ROOT)}: drifted from the generator's output at "
        f"'{divergent}' — run python3 tools/build_features_index.py"
    )


SPEC_CATEGORIES = {"Added", "Changed", "Deprecated", "Removed"}
PLUGIN_CATEGORIES = SPEC_CATEGORIES | {"Fixed", "Security"}
SPEC_ENTRY_FIELDS = {"Issue", "Category", "Breaking"}

ENTRY_HEADING_RE = re.compile(r"^\d{4}-\d{2}-\d{2} — \S")
VERSION_HEADING_RE = re.compile(r"^(?:\[Unreleased\]|\[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2})$")
BULLET_KEY_RE = re.compile(r"^- ([A-Za-z]+):")
PLACEHOLDER_RE = re.compile(r"#NN\b")


def _report_banned_fields(text: str, rel: str) -> None:
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("- PR:"):
            error(f"{rel}:{i}: a PR: line — an entry names only what exists when it is written")
        if PLACEHOLDER_RE.search(line):
            error(f"{rel}:{i}: an unfilled #NN placeholder")


def _entries(text: str) -> list[tuple[str, list[str]]]:
    """Split a changelog into (heading, body lines) per '## ' block."""
    blocks: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        if line.startswith("## "):
            blocks.append((line[3:].strip(), []))
        elif blocks:
            blocks[-1][1].append(line)
    return blocks


def check_spec_changelogs() -> None:
    """A feature's changelog entry names only what exists when it is written."""
    # Every CHANGELOG.md under features/, not only the leaves: an EPIC directory
    # carrying one has the same reader and the same way to rot.
    for path in sorted((ROOT / "features").rglob("CHANGELOG.md")):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        # File-scoped, not entry-scoped: a banned field in the preamble is still on disk.
        _report_banned_fields(text, str(rel))
        entries = _entries(text)
        if not entries:
            error(f"{rel}: no entry — a mandatory file with no content is an unwritten one")
        for heading, body in entries:
            where = f"{rel}: '{heading}'"
            if not ENTRY_HEADING_RE.match(heading):
                error(f"{where}: heading is not 'YYYY-MM-DD — <one-line title>'")
            keys = [m.group(1) for m in map(BULLET_KEY_RE.match, body) if m]
            for required in ("Issue", "Category", "Breaking"):
                if keys.count(required) != 1:
                    error(f"{where}: needs exactly one {required}: line, found {keys.count(required)}")
            for extra in sorted(set(keys) - SPEC_ENTRY_FIELDS):
                error(f"{where}: unknown field '{extra}:' — the entry carries three, and only three")
            for line in body:
                m = BULLET_KEY_RE.match(line)
                if m and m.group(1) == "Category":
                    value = line.split(":", 1)[1].strip()
                    if value not in SPEC_CATEGORIES:
                        error(
                            f"{where}: category '{value}' is not one of "
                            f"{', '.join(sorted(SPEC_CATEGORIES))}"
                        )


def check_plugin_changelogs() -> None:
    """Every shipped module carries a Keep a Changelog file a consumer can read."""
    for plugin_dir in sorted(d for d in (ROOT / "plugins").iterdir() if d.is_dir()):
        # A directory is a module when it declares itself one; plugins/ also holds caches.
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not manifest_path.exists():
            continue
        path = plugin_dir / "CHANGELOG.md"
        if not path.exists():
            error(f"plugins/{plugin_dir.name}: missing CHANGELOG.md")
            continue
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        _report_banned_fields(text, str(rel))
        entries = _entries(text)
        if not entries:
            error(f"{rel}: no version section")
        for heading, body in entries:
            where = f"{rel}: '{heading}'"
            if not VERSION_HEADING_RE.match(heading):
                error(f"{where}: heading is not '[<version>] - YYYY-MM-DD' or '[Unreleased]'")
            categories = [line[4:].strip() for line in body if line.startswith("### ")]
            for category in categories:
                if category not in PLUGIN_CATEGORIES:
                    error(
                        f"{where}: category '{category}' is not one of "
                        f"{', '.join(sorted(PLUGIN_CATEGORIES))}"
                    )
            # [Unreleased] is empty until something lands in it; a released version is not.
            if not categories and heading != "[Unreleased]":
                error(f"{where}: no category section — a release states what kind of change it is")
        released = [h for h, _ in entries if h != "[Unreleased]"]
        declared = (load_json(manifest_path) or {}).get("version")
        # The shape being gated buys nothing if the newest section describes an older release.
        if released and declared and not released[0].startswith(f"[{declared}]"):
            error(
                f"{rel}: newest section is '{released[0]}' but plugin.json declares "
                f"{declared} — the changelog cites plugin.json, so add the missing section"
            )
        # A second changelog under the same plugin shadows the one a consumer reads.
        for stray in plugin_dir.rglob("CHANGELOG.md"):
            if stray != path:
                error(
                    f"{stray.relative_to(ROOT)}: a module carries one changelog, at its root — "
                    f"this one shadows {rel}"
                )


def main() -> int:
    check_marketplace()
    check_skills()
    check_agents()
    check_commands()
    check_hooks()
    check_doc_links()
    check_skill_scripts()
    check_published_names()
    check_french_leftovers()
    check_composition_drift()
    check_deprecated_composition_keys()
    check_module_citations_by_name()
    check_feature_mandatory_files()
    check_no_tracker_refs()
    check_business_value_heading()
    check_qa_shape()
    check_splitting_guardrails()
    check_feature_index_sections()
    check_feature_files_present()
    check_global_index_drift()
    check_spec_changelogs()
    check_plugin_changelogs()

    for msg in WARNINGS:
        print(f"warning: {msg}")
    for msg in ERRORS:
        print(f"error: {msg}")
    print(f"\n{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
