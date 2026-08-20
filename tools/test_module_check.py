#!/usr/bin/env python3
"""Tests scrumia-module check against features/business/module-anatomy/'s criteria.

One test per criterion this ticket owns — AC-1, AC-3, AC-4, AC-6, AC-7, AC-8, AC-9,
AC-10, AC-11, AC-16. Every module is a fixture built in a temp directory, so nothing
here depends on what this repository happens to ship today — except AC-3, which is
about a run over every module the marketplace ships.

Here rather than inside the module it tests, for the reason the tool itself reports: a
test under `plugins/scrumia-core/` that reaches the repository root climbs out of its own
module, which is what `modular-composition`'s BR-7 forbids and what AC-3 refuses to exempt
the checker's own module from. `tools/` is the repository's, so reaching `plugins/` from
here is not a climb. Same arrangement as `tools/test_compose_status.py`.

    python3 tools/test_module_check.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "plugins" / "scrumia-core" / "bin" / "scrumia-module"
FAILURES: list[str] = []

CLEAN, TOOL_FAILED, BAD_USAGE, FINDINGS, NOT_A_MODULE = 0, 1, 2, 3, 4

README = """# fixture

One paragraph saying what the module is for.

## What it answers

A question.

## What it refuses

A boundary.

## What it ships

| Skill | Role |
|---|---|
| `fixture` | does the thing |
"""


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}{': ' + detail if detail else ''}")
        FAILURES.append(name)


def module(tmp: Path, name: str = "fixture", *, manifest: bool = True, **files) -> Path:
    """A module tree. Every fixture is minimal: what a test does not name is absent."""
    root = tmp / name
    root.mkdir(parents=True, exist_ok=True)
    if manifest:
        # BR-13 names `description` as always-present, so the helper must carry it.
        write(root / ".claude-plugin" / "plugin.json",
              json.dumps({"name": name, "version": "0.1.0",
                          "description": f"The {name} module.",
                          "repository": "https://github.com/acme/marketplace"}))
    for rel, body in files.items():
        write(root / rel.replace("__", "/"), body)
    return root


def write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def run(*args: str) -> tuple[int, str, str]:
    result = subprocess.run([sys.executable, str(TOOL), *args],
                            capture_output=True, text=True, timeout=60)
    return result.returncode, result.stdout, result.stderr


def verdict(root: Path) -> tuple[int, dict]:
    code, out, err = run("check", str(root), "--json")
    try:
        return code, json.loads(out)
    except json.JSONDecodeError:
        FAILURES.append(f"unparseable --json for {root}")
        return code, {"state": "unparseable", "findings": [], "stderr": err}


def rules(envelope: dict) -> list[str]:
    return [f["rule"] for f in envelope["findings"]]


def messages(envelope: dict) -> str:
    return "\n".join(f"{f['file']} {f['rule']} {f['message']}" for f in envelope["findings"])


# --------------------------------------------------------------------------- AC-1

def test_ac1_verdict_and_five_states(tmp: Path) -> None:
    print("AC-1 — a verdict on a module it has never seen")
    root = module(tmp / "ac1", **{"README.md": README})
    code, envelope = verdict(root)
    check("a conformant module is clean, exit 0", (code, envelope["state"]) == (CLEAN, "clean"),
          f"{code} {envelope['state']} {messages(envelope)}")

    dirty = module(tmp / "ac1b")
    code, envelope = verdict(dirty)
    check("a module with findings exits 3 and names them",
          code == FINDINGS and envelope["state"] == "findings" and envelope["findings"] != [],
          f"{code} {envelope['state']}")
    check("every finding names module, file, rule and one line",
          all(f["module"] and f["file"] and f["rule"] and f["message"] for f in envelope["findings"]))

    states = {
        "clean": run("check", str(root))[0],
        "findings": run("check", str(dirty))[0],
        "not a module": run("check", str(tmp))[0],
        "bad usage": run("check", "--nonsense")[0],
    }
    check("clean, findings, not-a-module and bad usage are four distinct codes",
          len(set(states.values())) == 4, str(states))
    check("the tool's own failure keeps 1 for itself, unused by the four",
          TOOL_FAILED not in states.values(), str(states))
    check("--json names the state in a field, never inferred from an empty list",
          "state" in envelope and envelope["state"] == "findings")


# --------------------------------------------------------------------------- AC-3

def test_ac3_the_owner_is_checked_like_any_other() -> None:
    print("AC-3 — the owner is checked like every other module")
    plugins = sorted(p for p in (ROOT / "plugins").iterdir()
                     if (p / ".claude-plugin" / "plugin.json").is_file())
    seen = {}
    for plugin in plugins:
        code, envelope = verdict(plugin)
        seen[envelope.get("module")] = (code, envelope)
    check("the owner of the check appears in a run over every module",
          "scrumia-core" in seen, str(sorted(seen)))
    code, envelope = seen.get("scrumia-core", (None, {"findings": []}))
    check("its verdict carries the same states as any other module's",
          code in (CLEAN, FINDINGS) and envelope["state"] in ("clean", "findings"), str(code))
    check("a finding against it has the same shape as any other module's",
          all(set(f) == {"module", "file", "rule", "message"} for f in envelope["findings"]))
    source = TOOL.read_text(encoding="utf-8")
    check("the tool names no module of its own to skip", "scrumia-core" not in source)


# --------------------------------------------------------------------------- AC-4

def test_ac4_neither_surface_writes(tmp: Path) -> None:
    print("AC-4 — the procedural check writes nothing")
    root = module(tmp / "ac4", **{"skills__s__SKILL.md": "# s\n\n[gone](nowhere.md)\n"})

    def snapshot() -> dict[str, tuple[int, float, str]]:
        return {str(p.relative_to(root)): (p.stat().st_size, p.stat().st_mtime,
                                           p.read_text(encoding="utf-8", errors="replace"))
                for p in sorted(root.rglob("*")) if p.is_file()}

    before = snapshot()
    first = verdict(root)
    second = verdict(root)
    check("the tree is byte-for-byte unchanged after two runs", snapshot() == before)
    check("no file was created", set(snapshot()) == set(before))
    check("the second run reports what the first did", first == second)


# --------------------------------------------------------------------------- AC-6

def test_ac6_no_readme_is_a_finding(tmp: Path) -> None:
    print("AC-6 — a module with no README is a finding")
    root = module(tmp / "ac6", **{
        "skills__s__SKILL.md": "---\nname: s\ndescription: d\n---\n\n# s\n",
        "CHANGELOG.md": "# Changelog\n",
    })
    _, envelope = verdict(root)
    named = [f for f in envelope["findings"] if f["file"] == "README.md"]
    check("the missing README is named", len(named) == 1, messages(envelope))
    check("it cites the rule that requires one",
          named and named[0]["rule"] == "module-anatomy/BR-4")
    check("the SKILL.md contract does not satisfy it",
          named and "SKILL.md" in named[0]["message"])


# --------------------------------------------------------------------------- AC-7

def test_ac7_required_sections(tmp: Path) -> None:
    print("AC-7 — required sections, present and in order")
    missing = README.replace("## What it refuses\n\nA boundary.\n\n", "")
    _, envelope = verdict(module(tmp / "ac7a", **{"README.md": missing}))
    check("a missing required section is named",
          any("What it refuses".lower() in f["message"].lower() for f in envelope["findings"]),
          messages(envelope))

    _, envelope = verdict(module(tmp / "ac7b", **{"README.md": README}))
    check("the four required sections and no optional one raise nothing",
          envelope["findings"] == [], messages(envelope))

    swapped = README.replace("## What it refuses\n\nA boundary.\n\n", "")
    swapped = swapped.replace("## What it answers", "## What it refuses\n\nA boundary.\n\n## What it answers")
    _, envelope = verdict(module(tmp / "ac7c", **{"README.md": swapped}))
    ordering = [f for f in envelope["findings"] if "order" in f["message"]]
    check("required sections out of order is a finding naming the order",
          len(ordering) == 1 and "what it answers" in ordering[0]["message"], messages(envelope))

    empty = README.replace("## What it refuses\n\nA boundary.", "## What it refuses")
    _, envelope = verdict(module(tmp / "ac7d", **{"README.md": empty}))
    check("a heading with nothing under it is a finding",
          any("nothing under it" in f["message"] for f in envelope["findings"]), messages(envelope))

    fenced = README + "\n```bash\n# What it refuses is a shell comment here\nrun\n```\n"
    _, envelope = verdict(module(tmp / "ac7f", **{"README.md": fenced}))
    check("a `#` inside a fenced block is not read as a section",
          envelope["findings"] == [], messages(envelope))

    renamed = README.replace("# fixture", "# not-the-published-name")
    _, envelope = verdict(module(tmp / "ac7e", **{"README.md": renamed}))
    check("the name heading is the published one",
          any("published name" in f["message"] for f in envelope["findings"]), messages(envelope))

    # Two shapes a README may legitimately take. Reporting either is how a check earns
    # the argument that ends with nobody running it.
    tagline = README.replace("# fixture", "# fixture — the thing it does")
    tagline = tagline.replace("## What it ships", "## What it ships (skills and names on PATH)")
    _, envelope = verdict(module(tmp / "ac7g", **{"README.md": tagline}))
    check("a tagline after the name, and a qualified section title, raise nothing",
          envelope["findings"] == [], messages(envelope))


# --------------------------------------------------------------------------- AC-8

def test_ac8_containment(tmp: Path) -> None:
    print("AC-8 — a reference leaving the module, and the two permitted forms")
    outside = tmp / "ac8" / "elsewhere"
    outside.mkdir(parents=True, exist_ok=True)
    (outside / "rule.md").write_text("x", encoding="utf-8")
    root = module(tmp / "ac8", **{
        "README.md": README,
        "skills__s__SKILL.md": "# s\n\nSee [the rule](../../../elsewhere/rule.md).\n",
    })
    _, envelope = verdict(root)
    leaving = [f for f in envelope["findings"] if f["rule"] == "modular-composition/BR-7"]
    check("a reference resolving outside the module is a finding", len(leaving) == 1, messages(envelope))
    check("it names the file and the reference",
          leaving and leaving[0]["file"] == "skills/s/SKILL.md" and "rule.md" in leaving[0]["message"])
    check("it cites the rule by its qualified identifier",
          leaving and leaving[0]["rule"] == "modular-composition/BR-7")
    check("the document it points at is an absolute URL",
          leaving and "https://github.com/" in leaving[0]["message"], messages(envelope))

    # ${CLAUDE_PLUGIN_ROOT} reaches an agent unsubstituted, so a path built from it
    # resolves nowhere — but the variable is legitimate in a hooks.json a README quotes.
    quoting = module(tmp / "ac8c", **{
        "README.md": README + '\n```json\n{"command": "${CLAUDE_PLUGIN_ROOT}/hooks/run.sh"}\n```\n',
    })
    _, envelope = verdict(quoting)
    check("a README quoting a hooks.json raises nothing", envelope["findings"] == [],
          messages(envelope))
    fence = "```bash\n${CLAUDE_PLUGIN_ROOT}/scripts/run.sh\n```\n"
    unsubstituted = module(tmp / "ac8d", **{
        "README.md": README,
        "skills__s__SKILL.md": f"# s\n\nRead [the guide](guides/01-run.md).\n\n{fence}",
        "skills__s__guides__01-run.md": f"# running\n\n{fence}",
        "agents__a.md": f"---\nname: a\n---\n\n{fence}",
        "commands__c.md": f"# c\n\n{fence}",
    })
    _, envelope = verdict(unsubstituted)
    flagged = {f["file"] for f in envelope["findings"] if "CLAUDE_PLUGIN_ROOT" in f["message"]}
    check("the variable is a finding in every file an agent executes, not only SKILL.md",
          flagged == {"skills/s/SKILL.md", "skills/s/guides/01-run.md",
                      "agents/a.md", "commands/c.md"}, str(sorted(flagged)))

    permitted = module(tmp / "ac8b", **{
        "README.md": README,
        "skills__s__SKILL.md": (
            "# s\n\nRun `scrumia-board move 4 in_review`, the name the tracker publishes.\n"
            "See [ADR-0018](https://github.com/tibs245/scrumia/blob/main/docs/adr/"
            "0018-modules-reach-by-name.md).\n"
        ),
    })
    _, envelope = verdict(permitted)
    check("a bare name on PATH and an absolute URL raise nothing",
          envelope["findings"] == [], messages(envelope))


# --------------------------------------------------------------------------- AC-9

def test_ac9_links_and_scripts(tmp: Path) -> None:
    print("AC-9 — a link or a script that does not exist")
    root = module(tmp / "ac9", **{
        "README.md": README,
        "skills__s__SKILL.md": (
            "# s\n\nRead [the reference](references/gone.md).\n\n"
            "```bash\n${CLAUDE_SKILL_DIR}/scripts/absent.sh\n```\n"
        ),
    })
    _, envelope = verdict(root)
    check("the missing link and the missing script are two separate findings",
          len(envelope["findings"]) == 2, messages(envelope))
    check("each names the referring file",
          all(f["file"] == "skills/s/SKILL.md" for f in envelope["findings"]))
    check("each names its missing target",
          any("gone.md" in f["message"] for f in envelope["findings"])
          and any("absent.sh" in f["message"] for f in envelope["findings"]), messages(envelope))

    shipped = module(tmp / "ac9b", **{
        "README.md": README,
        "skills__s__SKILL.md": "# s\n\n```bash\n${CLAUDE_SKILL_DIR}/run.sh\n```\n",
        "skills__s__run.sh": "#!/usr/bin/env bash\n",
        "bin__fixture-tool": "#!/usr/bin/env bash\n",
    })
    os.chmod(shipped / "skills" / "s" / "run.sh", 0o755)
    os.chmod(shipped / "bin" / "fixture-tool", 0o755)
    _, envelope = verdict(shipped)
    check("a script and a published name the module ships raise nothing",
          envelope["findings"] == [], messages(envelope))

    os.chmod(shipped / "bin" / "fixture-tool", 0o644)
    _, envelope = verdict(shipped)
    check("a published name that cannot run is a finding",
          any(f["file"] == "bin/fixture-tool" and "executable" in f["message"]
              for f in envelope["findings"]), messages(envelope))


# --------------------------------------------------------------------------- AC-10

def test_ac10_extension_data(tmp: Path) -> None:
    print("AC-10 — extension data shipped is checked, extension data omitted is not")
    _, envelope = verdict(module(tmp / "ac10a", **{"README.md": README}))
    check("shipping none of the three files raises nothing", envelope["findings"] == [],
          messages(envelope))

    _, envelope = verdict(module(tmp / "ac10b", **{
        "README.md": README, "extends.json": "{ not json",
    }))
    check("an extends.json that does not parse is a finding",
          any(f["file"] == "extends.json" for f in envelope["findings"]), messages(envelope))

    _, envelope = verdict(module(tmp / "ac10c", **{
        "README.md": README,
        "registers.json": json.dumps({"review": {"skill": "s", "purpose": "p"}}),
        "skills__s__SKILL.md": "# s\n\nThis skill never consults the register.\n",
    }))
    check("a registers.json naming a register the module never opens is a finding",
          any("never applied" in f["message"] for f in envelope["findings"]), messages(envelope))

    _, envelope = verdict(module(tmp / "ac10d", **{
        "README.md": README,
        "dependencies.jsonl": '"scrumia-board"\nnot-a-record\n',
    }))
    check("an unqualified name and a malformed line are each a finding",
          len([f for f in envelope["findings"] if f["file"] == "dependencies.jsonl"]) == 2,
          messages(envelope))

    _, envelope = verdict(module(tmp / "ac10e", **{
        "README.md": README,
        "extends.json": json.dumps({"implement": [{"name": "n", "summary": "s", "read": "gone.md"}]}),
    }))
    check("a directive reading a file the module does not ship is a finding",
          any("gone.md" in f["message"] for f in envelope["findings"]), messages(envelope))

    # Whose bin/ publishes a name is invisible from one tree, so a source that resolves
    # nowhere is not this surface's to refuse — only an entry that names none.
    _, envelope = verdict(module(tmp / "ac10f", **{
        "README.md": README,
        "dependencies.jsonl": '"ghost-marketplace:scrumia-nothing"\n',
    }))
    check("a qualified name whose source this tree cannot see raises nothing",
          envelope["findings"] == [], messages(envelope))

    # The rules-hierarchy arrangement: the entry point routes, a reference file runs it.
    _, envelope = verdict(module(tmp / "ac10g", **{
        "README.md": README,
        "registers.json": json.dumps({"review": {"skill": "s", "purpose": "p"}}),
        "skills__s__SKILL.md": "# s\n\nRead [the register](references/register.md).\n",
        "skills__s__references__register.md": "Run `scrumia-extends review`.\n",
    }))
    check("a register opened from a file the skill routes to is not a broken promise",
          envelope["findings"] == [], messages(envelope))


# --------------------------------------------------------------------------- AC-11

def test_ac11_not_a_module(tmp: Path) -> None:
    print("AC-11 — a directory that is not a module is refused, not judged")
    plain = tmp / "ac11" / "just-a-folder"
    plain.mkdir(parents=True, exist_ok=True)
    (plain / "notes.md").write_text("[gone](missing.md)\n", encoding="utf-8")
    code, out, err = run("check", str(plain), "--json")
    envelope = json.loads(out)
    check("it exits on the not-a-module code, distinct from bad usage",
          code == NOT_A_MODULE and code != BAD_USAGE, str(code))
    check("it names the state and says so on stderr",
          envelope["state"] == "not_a_module" and "not a module" in err, err)
    check("it returns no findings", envelope["findings"] == [])
    check("the envelope carries the four fields tech.md fixes, and no fifth",
          set(envelope) == {"ok", "state", "module", "findings"}, str(sorted(envelope)))


# --------------------------------------------------------------------------- AC-22

def test_ac22_manifest_fields(tmp: Path) -> None:
    print("AC-22 — the manifest carries the fixed field set, no extras or omissions")
    fixture = lambda body, name="ac22": write(
        tmp / name / ".claude-plugin" / "plugin.json", body)

    root = module(tmp / "ac22a", **{"README.md": README})
    _, envelope = verdict(root)
    check("name, version, description, repository and no others raise nothing",
          envelope["state"] == "clean" and envelope["findings"] == [],
          messages(envelope))

    body = json.dumps({"name": "fixture", "version": "0.1.0",
                       "description": "The fixture module."})
    root = tmp / "ac22b"
    (root / ".claude-plugin").mkdir(parents=True)
    fixture(body, name="ac22b")
    (root / "README.md").write_text(README, encoding="utf-8")
    _, envelope = verdict(root)
    check("omitting repository and homepage is conformant, BR-13 marks them conditional",
          envelope["state"] == "clean" and envelope["findings"] == [],
          messages(envelope))

    # A manifest carrying the schema's metadata fields is conformant: those are what
    # every shipped plugin already has, and the rule is against invention, not metadata.
    body = json.dumps({"name": "fixture", "version": "0.1.0",
                       "description": "The fixture module.",
                       "repository": "https://github.com/acme/marketplace",
                       "author": {"name": "acme"}, "license": "MIT",
                       "keywords": ["fixture", "test"]})
    root = tmp / "ac22c"
    (root / ".claude-plugin").mkdir(parents=True)
    fixture(body, name="ac22c")
    (root / "README.md").write_text(README, encoding="utf-8")
    _, envelope = verdict(root)
    check("author, license and keywords are schema fields and raise nothing",
          envelope["state"] == "clean" and envelope["findings"] == [],
          messages(envelope))

    # The failure mode the rule exists against: keys no schema defines.
    body = json.dumps({"name": "fixture", "version": "0.1.0",
                       "description": "The fixture module.",
                       "maintainer": "acme", "sponsor": "acme", "vibe": "good"})
    root = tmp / "ac22e"
    (root / ".claude-plugin").mkdir(parents=True)
    fixture(body, name="ac22e")
    (root / "README.md").write_text(README, encoding="utf-8")
    _, envelope = verdict(root)
    extras = [f for f in envelope["findings"]
              if f["file"] == ".claude-plugin/plugin.json"
              and f["rule"] == "module-anatomy/BR-13"
              and "the plugin schema defines" in f["message"]]
    check("a manifest with three invented keys reports each as its own finding",
          sorted(f["message"].split("`")[1] for f in extras)
          == ["maintainer", "sponsor", "vibe"],
          messages(envelope))
    check("every invention finding names the manifest and BR-13",
          all(f["file"] == ".claude-plugin/plugin.json"
              and f["rule"] == "module-anatomy/BR-13" for f in extras),
          messages(envelope))
    check("each finding cites BR-13 by absolute URL",
          all("https://github.com/" in f["message"] for f in extras),
          messages(envelope))

    body = json.dumps({"name": "fixture", "version": "0.1.0",
                       "repository": "https://github.com/acme/marketplace"})
    root = tmp / "ac22d"
    (root / ".claude-plugin").mkdir(parents=True)
    fixture(body, name="ac22d")
    (root / "README.md").write_text(README, encoding="utf-8")
    _, envelope = verdict(root)
    missing = [f for f in envelope["findings"]
               if f["file"] == ".claude-plugin/plugin.json"
               and f["rule"] == "module-anatomy/BR-13"
               and "always-present" in f["message"]]
    check("a manifest omitting `description` raises one finding naming the field",
          len(missing) == 1 and "description" in missing[0]["message"],
          messages(envelope))


# --------------------------------------------------------------------------- AC-16

def test_ac16_one_finding_shape(tmp: Path) -> None:
    print("AC-16 — findings carry one shape, revealing no surface")
    root = module(tmp / "ac16", **{
        "skills__s__SKILL.md": "# s\n\n[gone](nowhere.md)\n",
        "extends.json": "{ not json",
    })
    _, envelope = verdict(root)
    check("more than one rule produced a row", len(set(rules(envelope))) > 1, messages(envelope))
    check("every row carries exactly module, file, rule and one line",
          all(set(f) == {"module", "file", "rule", "message"} for f in envelope["findings"]))
    check("nothing in a row names the surface that produced it",
          not any(word in json.dumps(envelope["findings"]).lower()
                  for word in ("procedural", "audit", "checker")), messages(envelope))
    check("every rule is qualified by the feature that owns it",
          all("/" in f["rule"] for f in envelope["findings"]), str(rules(envelope)))


def main() -> int:
    if not TOOL.is_file():
        print(f"{TOOL}: missing", file=sys.stderr)
        return 1
    tmp = Path(tempfile.mkdtemp(prefix="scrumia-module-check."))
    try:
        test_ac1_verdict_and_five_states(tmp)
        test_ac3_the_owner_is_checked_like_any_other()
        test_ac4_neither_surface_writes(tmp)
        test_ac6_no_readme_is_a_finding(tmp)
        test_ac7_required_sections(tmp)
        test_ac8_containment(tmp)
        test_ac9_links_and_scripts(tmp)
        test_ac10_extension_data(tmp)
        test_ac11_not_a_module(tmp)
        test_ac16_one_finding_shape(tmp)
        test_ac22_manifest_fields(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if FAILURES:
        print(f"\n{len(FAILURES)} failure(s): {', '.join(FAILURES)}")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
