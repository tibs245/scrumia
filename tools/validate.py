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
        if manifest.get("version") != entry.get("version"):
            error(
                f"plugins/{name}: version mismatch — plugin.json {manifest.get('version')} "
                f"vs marketplace.json {entry.get('version')}"
            )
        if manifest.get("version") != market.get("version"):
            warn(
                f"plugins/{name}: version {manifest.get('version')} differs from "
                f"marketplace version {market.get('version')}"
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


def check_doc_links() -> None:
    """Relative markdown links in docs/, plugins/ and features/ must resolve.

    Links may use ${CLAUDE_SKILL_DIR} (the only variable Claude Code substitutes
    inside skill content — ${CLAUDE_PLUGIN_ROOT} works in hooks.json/MCP configs
    only). We resolve it to the linking file's skill directory. A lingering
    ${CLAUDE_PLUGIN_ROOT} in a skill file is flagged: it would reach the agent
    unsubstituted.
    """
    link_re = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
    for md in sorted([
        *ROOT.glob("docs/**/*.md"),
        *ROOT.glob("plugins/**/*.md"),
        *ROOT.glob("features/**/*.md"),
        ROOT / "README.md",
    ]):
        rel = md.relative_to(ROOT)
        skill_dir = None
        if rel.parts[0] == "plugins" and len(rel.parts) >= 4 and rel.parts[2] == "skills":
            skill_dir = ROOT / rel.parts[0] / rel.parts[1] / "skills" / rel.parts[3]
        for match in link_re.finditer(md.read_text(encoding="utf-8")):
            target = match.group(1)
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
            if not resolved.exists():
                error(f"{rel}: broken link → {target}")


def check_skill_scripts() -> None:
    """Scripts a skill tells the agent to run must resolve and be executable.

    check_doc_links only sees markdown links, so a ${CLAUDE_PLUGIN_ROOT} sitting
    in a bash block used to pass silently — and reach the agent unsubstituted.
    """
    plugin_root_re = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}")
    script_re = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/([\w./-]+\.(?:sh|py))")
    for md in sorted(ROOT.glob("plugins/**/SKILL.md")):
        rel = md.relative_to(ROOT)
        text = md.read_text(encoding="utf-8")
        if plugin_root_re.search(text):
            error(f"{rel}: ${{CLAUDE_PLUGIN_ROOT}} anywhere in a skill is not substituted — use ${{CLAUDE_SKILL_DIR}}")
        skill_dir = md.parent
        for match in script_re.finditer(text):
            script = (skill_dir / match.group(1)).resolve()
            if not script.exists():
                error(f"{rel}: references missing script → {match.group(0)}")
            elif not os.access(script, os.X_OK):
                error(f"{script.relative_to(ROOT)}: not executable (chmod +x)")


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


def main() -> int:
    check_marketplace()
    check_skills()
    check_agents()
    check_commands()
    check_hooks()
    check_doc_links()
    check_skill_scripts()
    check_french_leftovers()
    check_composition_drift()

    for msg in WARNINGS:
        print(f"warning: {msg}")
    for msg in ERRORS:
        print(f"error: {msg}")
    print(f"\n{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
