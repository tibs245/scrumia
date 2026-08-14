#!/usr/bin/env python3
"""Acceptance tests for the writing side of `modules:` (#303).

AC-17 and AC-18 of features/business/modular-composition/, from the half that produces a
configuration rather than the half that reads one. The reading side is asserted by
tools/test_scrumia_extends.py and tools/test_settings_cascade.py; nothing there can fail
when the installer writes a shape no reader accepts, which is what this file covers.

Three kinds of assertion, in descending order of strength:

1. The config template `scrumia-init` Step 3 tells an agent to write is extracted from the
   skill and fed to the real reader. A template that parses as nothing, keys a module by a
   bare name, or hides the execution grid where the cascade will not find it fails here —
   and it fails for the same reason a real project would.
2. This repository's own `CLAUDE.md` is checked against its own `.scrumia/config.yaml`, key
   by key. The migration this ticket finishes is exactly a config and a `CLAUDE.md` that
   were allowed to disagree, and a substring check on either alone cannot see it.
3. The migration procedure itself is prose an agent executes, so what is asserted is that
   each branch is still stated — the three sources, and the refusal to guess a fourth.

Run from the repo root: python3 tools/test_init_migration.py
Exit code 0 when everything passes, 1 otherwise.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INIT = ROOT / "plugins" / "scrumia-core" / "skills" / "scrumia-init" / "SKILL.md"
CLAUDE_MD = ROOT / "CLAUDE.md"
CONFIG = ROOT / ".scrumia" / "config.yaml"
EXTENDS_BIN = ROOT / "plugins" / "scrumia-core" / "bin"

FAILURES: list[str] = []

# The grammar BR-13 admits: a marketplace as <owner>/<repo>, or one of the two bare words.
KEY = re.compile(r"^(?:[^/:]+/[^/:]+|shared|local):[^:]+$")


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    if not ok:
        FAILURES.append(label)
        if detail:
            print(f"       {detail}")


def skill_text() -> str:
    return INIT.read_text(encoding="utf-8")


def template_yaml() -> str:
    """The ```yaml block of Step 3 — the one an agent copies into .scrumia/config.yaml."""
    text = skill_text()
    step3 = text[text.index("## Step 3"):text.index("## Step 4")]
    blocks = re.findall(r"```yaml\n(.*?)```", step3, re.S)
    if not blocks:
        raise AssertionError("Step 3 carries no ```yaml block to check")
    return blocks[0]


def run_extends(args: list[str], config: Path, marketplace: Path | None = None
                ) -> tuple[int, str, str]:
    env = dict(os.environ)
    env["PATH"] = f"{EXTENDS_BIN}{os.pathsep}{env['PATH']}"
    env["SCRUMIA_CONFIG"] = str(config)
    # All three tiers pinned, so no assertion here can be answered by a real module on the
    # machine running the suite. SCRUMIA_MODULE_DIR replaces the PATH sweep entirely.
    env.pop("SCRUMIA_SHARED_DIR", None)
    env.pop("SCRUMIA_CONFIG_LOCAL", None)
    if marketplace is not None:
        env["SCRUMIA_MODULE_DIR"] = str(marketplace)
    else:
        env.pop("SCRUMIA_MODULE_DIR", None)
    p = subprocess.run([str(EXTENDS_BIN / "scrumia-extends"), *args],
                       capture_output=True, text=True, env=env, timeout=30)
    return p.returncode, p.stdout, p.stderr


def state_of(out: str, key: str) -> str:
    try:
        rows = json.loads(out)
    except json.JSONDecodeError:
        return "unparseable"
    return next((r.get("state", "?") for r in rows if r.get("key") == key), "not-listed")


# ------------------------------------------------------------------ AC-17, writing side

def test_ac17_the_template_writes_sourced_keys() -> None:
    print("AC-17 — the template writes modules:, and every key carries its source")
    import yaml

    raw = template_yaml()
    check("the template no longer writes the retired list",
          not re.search(r"^extends:", raw, re.M), "a top-level extends: survives in Step 3")

    doc = yaml.safe_load(raw)
    check("it parses as YAML and carries modules:", isinstance(doc.get("modules"), dict))
    if not isinstance(doc.get("modules"), dict):
        return

    for key in doc["modules"]:
        check(f"'{key}' matches <source>:<module>", bool(KEY.match(key)))
    sources = {k.rsplit(":", 1)[0] for k in doc["modules"]}
    check("more than one source is shown, so the grammar reads as a grammar",
          len(sources) > 1, f"sources shown: {sorted(sources)}")

    apps = doc.get("apps") or []
    check("an app carries a modules mapping, not a list",
          bool(apps) and all(isinstance(a.get("modules"), dict) for a in apps),
          json.dumps(apps))
    check("every app still carries the path per-app activation keys on",
          all(a.get("path") for a in apps), json.dumps(apps))


def test_ac17_the_real_reader_accepts_the_template() -> None:
    print("AC-17 — the reader resolves the template without a warning or a refusal")
    with tempfile.TemporaryDirectory(prefix="scrumia-init-") as tmp:
        cfg = Path(tmp) / ".scrumia" / "config.yaml"
        cfg.parent.mkdir(parents=True)
        cfg.write_text(template_yaml(), encoding="utf-8")

        code, out, err = run_extends(["--modules", "--json"], cfg)
        check("--modules runs on the template", code == 0, err[:300])
        check("no key is refused as not a declaration",
              "is not a declaration" not in err and "is not a declaration" not in out,
              err[:300])
        check("no migration notice fires on a template already on modules:",
              "retired" not in err, err[:300])
        check("the composition is not read as empty",
              "composition is empty" not in err, err[:300])

        declared = json.loads(out) if code == 0 and out.strip() else []
        keys = {m.get("key") for m in declared} if isinstance(declared, list) else set()
        check("the template's keys are the ones reported back",
              keys >= {"tibs245/scrumia:scrumia-teams"}, f"reported: {sorted(keys)}")

        # A test that only ever sees green proves nothing about what it is watching.
        broken = Path(tmp) / ".scrumia" / "broken.yaml"
        broken.write_text(template_yaml().replace('"tibs245/scrumia:scrumia-teams"',
                                                  '"scrumia-teams"'), encoding="utf-8")
        _, out2, err2 = run_extends(["--modules"], broken)
        check("and the same check goes red on a bare name",
              "'scrumia-teams' is not a declaration" in (out2 + err2), (out2 + err2)[:300])


def test_ac17_the_migration_sources_rather_than_guesses() -> None:
    print("AC-17 — the migration sources each name, and reports one it cannot")
    text = skill_text()
    step3 = text[text.index("## Step 3"):text.index("## Step 4")]

    for retired in ("extends:", "composition:", "practices"):
        check(f"the retired `{retired}` is named as something to migrate from",
              retired in step3)
    check("the sourcing asks the resolver instead of searching the tiers by hand",
          "scrumia-extends --modules" in step3, "the migration reimplements discovery")

    # Answering `shadow` with anything but silence freezes one checkout into the file.
    rows = dict(re.findall(r"^\|\s*`(resolved|shadow|conflict|absent)`\s*\|[^|]*\|([^|]*)\|",
                           step3, re.M))
    check("every state the resolver returns has a row", set(rows) ==
          {"resolved", "shadow", "conflict", "absent"}, f"rows found: {sorted(rows)}")
    for state in ("shadow", "conflict", "absent"):
        check(f"`{state}` is answered with writing nothing",
              "nothing" in rows.get(state, "").lower(), rows.get(state, "<no row>"))
    check("`resolved` is the one row that produces a key",
          "nothing" not in rows.get("resolved", "x").lower(), rows.get("resolved", "<no row>"))
    check("a name it cannot source is reported rather than written",
          "reported, not written" in step3 or "reported, never written" in step3,
          "the refusal to guess a source is no longer stated")


def test_ac17_a_marketplace_source_is_the_manifest_not_the_alias() -> None:
    print("AC-17 — the marketplace half of a key is what the resolver actually binds")
    with tempfile.TemporaryDirectory(prefix="scrumia-src-") as tmp:
        tmp = Path(tmp)
        # A fork: the alias names acme/fork, the manifest still claims the upstream.
        mod = tmp / "market" / "acme-thing" / ".claude-plugin"
        mod.mkdir(parents=True)
        (mod / "plugin.json").write_text(json.dumps(
            {"name": "acme-thing", "repository": "https://github.com/tibs245/scrumia.git"}),
            encoding="utf-8")

        def declared_as(key: str) -> str:
            cfg = tmp / f"{key.replace('/', '_').replace(':', '-')}.yaml"
            cfg.write_text(f'project:\n  name: t\nmodules:\n  "{key}": {{}}\napps: []\n',
                           encoding="utf-8")
            _, out, _ = run_extends(["--modules", "--json"], cfg, marketplace=tmp / "market")
            return state_of(out, key)

        check("the manifest's repository is what binds",
              declared_as("tibs245/scrumia:acme-thing") == "resolved",
              declared_as("tibs245/scrumia:acme-thing"))
        check("the marketplace it was installed through does not",
              declared_as("acme/fork:acme-thing") == "absent",
              declared_as("acme/fork:acme-thing"))

    step3 = skill_text()[skill_text().index("## Step 3"):skill_text().index("## Step 4")]
    check("and the skill sources from the manifest, not the alias table",
          "`.claude-plugin/plugin.json`" in step3 and "cross-check, not the source" in step3,
          "the sourcing rule no longer names the manifest as the authority")
    check("the migration verifies the rewrite against the run it started from",
          "must resolve to the same root" in step3,
          "nothing tells the migration to re-resolve after writing")


def test_the_skill_does_not_migrate_unasked() -> None:
    # Consent about this skill's own behaviour, not a rule of the feature — so it carries
    # no AC, and asserting it under one would credit a criterion that does not say it.
    print("scrumia-init — a project is migrated when it asks, not in passing")
    text = skill_text()
    step3 = text[text.index("## Step 3"):text.index("## Step 4")]
    check("the refusal to migrate unasked is stated",
          "do not migrate a file you have not been asked to" in step3.lower())


# ------------------------------------------------------------------ AC-18, writing side

def test_ac18_the_template_places_a_setting_by_its_reader() -> None:
    print("AC-18 — a block one module reads is written under that module's params:")
    import yaml

    doc = yaml.safe_load(template_yaml())
    settings = doc.get("settings") or {}
    # `team.roles` is the one block ADR-0021 keeps in layer 1, because three modules read
    # it. Anything else left here is a block whose reader the template failed to name.
    check("settings: keeps only what no single module owns",
          set(settings) == {"team"}, f"settings: carries {sorted(settings)}")
    check("and what it keeps is the roles list, not a module's configuration",
          set(settings.get("team", {})) == {"roles"},
          json.dumps(settings.get("team", {}))[:200])

    teams = (doc["modules"].get("tibs245/scrumia:scrumia-teams") or {}).get("params") or {}
    check("the execution grid moved under the module that reads it",
          "matrix" in (teams.get("execution") or {}), json.dumps(teams)[:200])
    tracker = (doc["modules"].get("tibs245/scrumia:scrumia-github-project") or {}).get("params") or {}
    check("so did autonomy, whose only reader is the tracker module",
          "autonomy" in tracker, json.dumps(tracker)[:200])


def test_ac18_the_cascade_reaches_what_the_template_wrote() -> None:
    print("AC-18 — what the template writes is what the cascade resolves")
    with tempfile.TemporaryDirectory(prefix="scrumia-init-") as tmp:
        cfg = Path(tmp) / ".scrumia" / "config.yaml"
        cfg.parent.mkdir(parents=True)
        cfg.write_text(template_yaml(), encoding="utf-8")

        code, out, err = run_extends(
            ["--settings", "tibs245/scrumia:scrumia-teams"], cfg)
        check("--settings resolves for the module the template configured", code == 0, err[:300])
        resolved = json.loads(out) if code == 0 and out.strip() else {}
        check("the grid resolves through layer 2, not out of the raw file",
              (resolved.get("execution") or {}).get("matrix", {}).get("L", {}).get("low") == "opus",
              json.dumps(resolved)[:300])
        check("and the layer that answered is named as the module's own params:",
              "params: of tibs245/scrumia:scrumia-teams" in err, err[:300])
        # AC-18's second Given: a block left in layer 1 reaches every module that reads it,
        # so leaving `team.roles` there is not the same as hiding it from this module.
        check("what the template left in settings: still reaches the module",
              (resolved.get("team") or {}).get("roles"), json.dumps(resolved)[:200])
        check("and both layers are named as having answered",
              "settings:" in err and "params: of" in err, err[:300])


def test_ac18_the_three_layers_are_stated_in_order() -> None:
    print("AC-18 — the order is stated where the layers are, not only applied")
    text = skill_text()
    step3 = text[text.index("## Step 3"):text.index("## Step 4")]
    layers = re.findall(r"^(\d)\. `([^`]+)`", step3, re.M)
    check("the three layers are a numbered list, in the order that decides",
          [n for n, _ in layers] == ["1", "2", "3"]
          and layers[0][1] == "settings:"
          and layers[1][1].startswith("modules[")
          and "config.local.yaml" in layers[2][1],
          f"found: {layers}")
    check("layer 3 is marked as the one that is never committed",
          "never committed" in step3)


# --------------------------------------------------- this repository, the first adopter

def test_the_writing_rule_has_a_rule_upstream_of_its_criterion() -> None:
    # qa.md carries one scenario per rule in business.md, never a rule of its own.
    print("AC-17 — the writer-side scenario has a business rule above it")
    business = (ROOT / "features" / "business" / "modular-composition"
                / "business.md").read_text(encoding="utf-8")
    br13 = business[business.index("- **BR-13**"):business.index("- **BR-14**")]
    check("BR-13 governs writing a key and not only reading one",
          "writes" in br13 or "written" in br13, br13[:200])
    check("it names the manifest as the marketplace source",
          "manifest" in br13, br13[:200])
    check("and it refuses to settle an ambiguous name when writing",
          "reported and left unwritten" in br13, br13[:300])
    check("the asymmetry between resolving and recording is stated in prose too",
          "may settle an ambiguous name for the length of one call" in business)


def test_claude_md_names_the_keys_its_config_declares() -> None:
    print("AC-17 — this repository's CLAUDE.md names modules by the key it declares them by")
    import yaml

    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    declared = set(cfg.get("modules") or {})
    check("the repository's own config is on modules:", bool(declared),
          "no modules: in .scrumia/config.yaml")

    md = CLAUDE_MD.read_text(encoding="utf-8")
    section = md[md.index("## ScrumIA composition"):md.index("### What rules apply")]
    named = set(re.findall(r"`([^`\s]+:[^`\s]+)`", section)) & set(
        re.findall(r"`([^`\s]+:scrumia-[^`\s]+)`", section))

    check("every module the config declares is named in the table",
          declared <= named, f"missing from CLAUDE.md: {sorted(declared - named)}")
    check("and nothing is named there that the config does not declare",
          named <= declared, f"named but not declared: {sorted(named - declared)}")
    check("the per-app table no longer speaks of `Extends`",
          "| Extends |" not in section, "the retired column heading survives")

    # Step 5 regenerates everything between the markers, so a generic sentence living
    # there and not in the template survives exactly until the next scrumia-init run.
    text = skill_text()
    blocks = re.findall(r"^````markdown\n(.*?)^````", text, re.S | re.M)
    template = blocks[0] if blocks else ""
    check("Step 5 still carries the CLAUDE.md template as a fenced block",
          "<!-- scrumia:start -->" in template, "no ````markdown block found in the skill")
    generic = "Read either through `scrumia-extends --settings`"
    check("a generic sentence inside the markers is in the template that regenerates them",
          (generic in md) == (generic in template),
          "the cascade sentence is in CLAUDE.md but not in scrumia-init's template")


def main() -> int:
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("error: PyYAML is required to read the template and the config")
        return 1
    test_ac17_the_template_writes_sourced_keys()
    test_ac17_the_real_reader_accepts_the_template()
    test_ac17_the_migration_sources_rather_than_guesses()
    test_ac17_a_marketplace_source_is_the_manifest_not_the_alias()
    test_the_writing_rule_has_a_rule_upstream_of_its_criterion()
    test_the_skill_does_not_migrate_unasked()
    test_ac18_the_template_places_a_setting_by_its_reader()
    test_ac18_the_cascade_reaches_what_the_template_wrote()
    test_ac18_the_three_layers_are_stated_in_order()
    test_claude_md_names_the_keys_its_config_declares()
    print(f"\n{len(FAILURES)} failure(s)")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
