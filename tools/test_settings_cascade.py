#!/usr/bin/env python3
"""Acceptance tests for the modules that consume the settings cascade (#315).

AC-18's consuming half and AC-19 of features/business/modular-composition/, and AC-22 of
features/business/execution-policy/: a module resolves its configuration through
`scrumia-extends --settings` rather than out of the raw config, and one that cannot
resolve it stops instead of answering from its own defaults.

The two consumers under test are `plugins/scrumia-github-project/bin/scrumia-board` and
`plugins/scrumia-teams/bin/scrumia-pick-model`. Neither is allowed to reach the network
here: `gh` is a stub that always fails, which is enough, because every assertion below is
about what happens *before* the first API call.

Run from the repo root: python3 tools/test_settings_cascade.py
Exit code 0 when everything passes, 1 otherwise.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOARD = ROOT / "plugins" / "scrumia-github-project" / "bin" / "scrumia-board"
PICK = ROOT / "plugins" / "scrumia-teams" / "bin" / "scrumia-pick-model"
EXTENDS_BIN = ROOT / "plugins" / "scrumia-core" / "bin"

FAILURES: list[str] = []
TMP = Path(tempfile.mkdtemp(prefix="scrumia-cascade-"))


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  ok    {name}")
    else:
        FAILURES.append(f"{name}{' — ' + str(detail) if detail else ''}")
        print(f"  FAIL  {name}{' — ' + str(detail) if detail else ''}")


def make_bin() -> Path:
    """A PATH holding only what the tools legitimately need — and a `gh` that refuses.

    Built rather than inherited so that "scrumia-extends is not reachable" is a state a
    test can actually create: on a developer's machine the harness has already put it on
    PATH, and a test that trusted the ambient PATH would silently never exercise it.
    """
    binned = TMP / "bin"
    binned.mkdir(exist_ok=True)
    # The system directories join PATH below, so only what may live outside them is
    # linked here — plus `gh`, which is shadowed rather than found.
    for tool in ("jq", "yq", "python3"):
        found = shutil.which(tool)
        if found and not (binned / tool).exists():
            (binned / tool).symlink_to(found)
    stub = binned / "gh"
    stub.write_text("#!/bin/sh\necho 'gh stub: refusing to reach the network' >&2\nexit 1\n")
    stub.chmod(0o755)
    return binned


BIN = make_bin()


def write(name: str, body: str) -> Path:
    path = TMP / name
    path.write_text(body, encoding="utf-8")
    return path


def run(tool: Path, args: list[str], config: Path, local: Path | None = None,
        resolver: bool = True, extra_env: dict[str, str] | None = None):
    # scrumia-extends lives only in a plugin's bin/, so omitting it here is what makes
    # the resolver genuinely unreachable while awk, tr and the rest stay available.
    system = f"{BIN}:/usr/bin:/bin"
    path = f"{EXTENDS_BIN}:{system}" if resolver else system
    env = {
        "PATH": path,
        "HOME": str(TMP),
        "NO_COLOR": "1",
        "SCRUMIA_CONFIG": str(config),
        "SCRUMIA_CONFIG_LOCAL": str(local) if local else str(TMP / "absent.local.yaml"),
    }
    env.update(extra_env or {})
    proc = subprocess.run([str(tool), *args], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout, proc.stderr


def as_json(out: str):
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


# --------------------------------------------------------------- the configurations

BASE_PROJECT = """project:
  name: "T"
  repo: "acme/widgets"
"""

MATRIX = """      matrix:
        S:  { low: sonnet, medium: sonnet, high: sonnet, critical: opus }
        L:  { low: sonnet, medium: opus,   high: opus,   critical: opus }
"""

# Layer 1 only, in the shape this repository still ships: `settings.team.execution`.
RETIRED_SHAPE = BASE_PROJECT + """extends:
  - scrumia-teams
  - scrumia-github-project
settings:
  team:
    execution:
      unlabeled: sonnet
      unrated_risk: medium
""" + MATRIX + """  tracker:
    project_number: 11
    board:
      field_id: "FIELD_BASE"
      flow:
        in_progress: "In progress"
      options:
        "In progress": "opt-base"
"""

# The shape ADR-0021 migrates to: each module's own keys under its `params:`.
MIGRATED_SHAPE = BASE_PROJECT + """modules:
  "acme/scrumia:scrumia-teams":
    params:
      execution:
        unlabeled: sonnet
        unrated_risk: medium
""" + MATRIX.replace("      ", "        ") + """  "acme/scrumia:scrumia-github-project":
    params:
      project_number: 22
      board:
        field_id: "FIELD_PARAMS"
        flow:
          in_progress: "In progress"
        options:
          "In progress": "opt-params"
settings: {}
"""


def module_key(module: str) -> str:
    """The key a config must use for this checkout — derived the way the tools derive it."""
    manifest = json.loads((ROOT / "plugins" / module / ".claude-plugin" / "plugin.json").read_text())
    src = manifest.get("repository") or manifest.get("homepage") or ""
    src = src.split("://", 1)[-1].split("/", 1)[-1] if "://" in src else src
    return f"{src.removesuffix('.git').rstrip('/')}:{manifest['name']}"


TEAMS_KEY = module_key("scrumia-teams")
TRACKER_KEY = module_key("scrumia-github-project")
MIGRATED_SHAPE = MIGRATED_SHAPE.replace("acme/scrumia:scrumia-teams", TEAMS_KEY)
MIGRATED_SHAPE = MIGRATED_SHAPE.replace("acme/scrumia:scrumia-github-project", TRACKER_KEY)


# --------------------------------------------------------------- AC-18, consuming half

def test_layer_three_reaches_the_policy() -> None:
    """A value only the per-machine layer carries changes what the policy answers."""
    cfg = write("l3.yaml", RETIRED_SHAPE)
    local = write("l3.local.yaml", """settings:
  team:
    execution:
      matrix:
        L: { low: opus }
""")
    code, out, err = run(PICK, ["--scope", "L", "--risk", "low"], cfg)
    answer = as_json(out) or {}
    check("AC-18 baseline: the versioned layer answers sonnet for L/low",
          code == 0 and answer.get("model") == "sonnet", f"{code} {out} {err}")

    code, out, err = run(PICK, ["--scope", "L", "--risk", "low"], cfg, local=local)
    answer = as_json(out) or {}
    check("AC-18 consuming half: the local layer's cell wins for scrumia-pick-model",
          code == 0 and answer.get("model") == "opus", f"{code} {out} {err}")


def test_layer_three_reaches_the_board() -> None:
    cfg = write("b3.yaml", RETIRED_SHAPE)
    local = write("b3.local.yaml", """settings:
  tracker:
    project_number: 99
""")
    code, out, err = run(BOARD, ["doctor"], cfg, local=local)
    answer = as_json(out) or {}
    check("AC-18 consuming half: the local layer's project number wins for scrumia-board",
          answer.get("project_number") == 99, f"{code} {out} {err}")


def test_layer_two_reaches_both() -> None:
    """The migrated shape — each module's keys under its own `params:` — resolves."""
    cfg = write("l2.yaml", MIGRATED_SHAPE)
    code, out, err = run(PICK, ["--scope", "L", "--risk", "medium"], cfg)
    answer = as_json(out) or {}
    check("AC-18: scrumia-pick-model resolves a policy carried only by its own params:",
          code == 0 and answer.get("model") == "opus", f"{code} {out} {err}")

    code, out, err = run(BOARD, ["doctor"], cfg)
    answer = as_json(out) or {}
    check("AC-18: scrumia-board resolves a board carried only by its own params:",
          answer.get("project_number") == 22 and answer.get("field_id") == "FIELD_PARAMS",
          f"{code} {out} {err}")


def test_params_outrank_settings_on_the_same_key() -> None:
    """BR-14's order, tested where it can actually be observed.

    Both values sit in the *same* shape, so only the layer order decides which wins —
    a fixture whose two values sit in different shapes would be decided by the consumer's
    shape rule instead, and would pass with the cascade's merge order inverted.
    """
    both = RETIRED_SHAPE.replace("extends:\n  - scrumia-teams\n  - scrumia-github-project\n",
                                 f'modules:\n  "{TEAMS_KEY}":\n    params:\n'
                                 '      team:\n        execution:\n          matrix:\n'
                                 '            L: { low: opus }\n'
                                 f'  "{TRACKER_KEY}":\n    params:\n'
                                 '      tracker:\n        project_number: 77\n')
    cfg = write("half.yaml", both)
    code, out, err = run(BOARD, ["doctor"], cfg)
    answer = as_json(out) or {}
    check("BR-14 order: params: beat settings: on the identical key",
          answer.get("project_number") == 77, f"{code} {out} {err}")

    code, out, err = run(PICK, ["--scope", "L", "--risk", "low"], cfg)
    answer = as_json(out) or {}
    check("BR-14 order: params: beat settings: on the identical matrix cell",
          code == 0 and answer.get("model") == "opus", f"{code} {out} {err}")


def test_a_local_source_resolves() -> None:
    """BR-13 admits `local:` and `shared:`; a key derived from a manifest cannot guess them."""
    cfg = write("local.yaml", BASE_PROJECT + """modules:
  "local:scrumia-teams":
    params:
      execution:
        unlabeled: sonnet
        matrix:
          L: { high: opus }
  "local:scrumia-github-project":
    params:
      project_number: 42
      board: { field_id: "FIELD_LOCAL_SOURCE" }
settings: {}
""")
    code, out, err = run(BOARD, ["doctor"], cfg)
    answer = as_json(out) or {}
    check("BR-13: a module declared from `local:` still resolves its own params:",
          answer.get("project_number") == 42, f"{code} {out} {err}")

    code, out, err = run(PICK, ["--scope", "L", "--risk", "high"], cfg)
    answer = as_json(out) or {}
    check("BR-13: the policy resolves under a `local:` key too",
          code == 0 and answer.get("model") == "opus", f"{code} {out} {err}")


def test_a_partial_migration_keeps_both_halves() -> None:
    """One key migrated, the rest not: nothing may fall through to a built-in literal."""
    partial = RETIRED_SHAPE.replace(
        "extends:\n  - scrumia-teams\n  - scrumia-github-project\n",
        f'modules:\n  "{TEAMS_KEY}":\n    params:\n'
        '      execution:\n        matrix:\n          L: { low: opus }\n'
        f'  "{TRACKER_KEY}":\n    params:\n'
        '      board:\n        field_id: "FIELD_MIGRATED"\n'
    ).replace("      unlabeled: sonnet\n", "      unlabeled: opus\n")
    cfg = write("partial.yaml", partial)

    code, out, err = run(PICK, ["--scope", "XL", "--risk", "low"], cfg)
    answer = as_json(out) or {}
    check("AC-22: an unmigrated `unlabeled` survives beside a migrated matrix",
          code == 0 and answer.get("model") == "opus", f"{code} {out} {err}")

    code, out, err = run(BOARD, ["move", "1", "in_progress"], cfg)
    answer = as_json(out) or {}
    check("AC-18: an unmigrated flow and options survive beside a migrated field id",
          code != 0 and "graphql lookup failed" in (answer.get("error") or ""),
          f"{code} {out} {err}")
    code, out, err = run(BOARD, ["doctor"], cfg)
    check("AC-18: and the migrated field id is the one that wins",
          (as_json(out) or {}).get("field_id") == "FIELD_MIGRATED", f"{code} {out} {err}")


# --------------------------------------------------------------- AC-19 and AC-22

def test_no_resolver_stops_both_tools() -> None:
    """The failure this ticket exists for: no resolver must never mean "use my defaults"."""
    cfg = write("noresolver.yaml", RETIRED_SHAPE)

    code, out, err = run(PICK, ["--scope", "L", "--risk", "low"], cfg, resolver=False)
    answer = as_json(out) or {}
    check("AC-22: scrumia-pick-model refuses to answer when the resolver is unreachable",
          code != 0 and answer.get("ok") is False and "model" not in answer,
          f"{code} {out} {err}")
    check("AC-19: and it names scrumia-extends as what it could not reach",
          "scrumia-extends" in (answer.get("error") or ""), answer.get("error"))

    # `doctor` is the deliberate exception, covered by its own test below.
    code, out, err = run(BOARD, ["read"], cfg, resolver=False)
    answer = as_json(out) or {}
    check("AC-19: scrumia-board refuses to run when the resolver is unreachable",
          code != 0 and answer.get("ok") is False
          and "scrumia-extends" in (answer.get("error") or ""),
          f"{code} {out} {err}")


def test_no_policy_at_all_stops_the_tool() -> None:
    """No layer carries an execution block: an unresolvable grid, not a hole in one."""
    cfg = write("nopolicy.yaml", BASE_PROJECT + "extends:\n  - scrumia-teams\nsettings: {}\n")
    code, out, err = run(PICK, ["--scope", "L", "--risk", "low"], cfg)
    answer = as_json(out) or {}
    check("AC-22: an unresolvable policy answers no model at all",
          code != 0 and answer.get("ok") is False and "model" not in answer,
          f"{code} {out} {err}")
    check("AC-22: and the refusal names the block it looked for",
          "execution" in (answer.get("error") or ""), answer.get("error"))


def test_an_empty_policy_block_is_not_a_policy() -> None:
    """`execution: {}` resolves — and carries no grid, which is AC-22's Given word for word."""
    cfg = write("emptyexec.yaml", BASE_PROJECT + """extends:
  - scrumia-teams
settings:
  team:
    execution: {}
""")
    code, out, err = run(PICK, ["--scope", "L", "--risk", "high"], cfg)
    answer = as_json(out) or {}
    check("AC-22: a resolved but empty execution block answers no model",
          code != 0 and answer.get("ok") is False and "model" not in answer,
          f"{code} {out} {err}")


def test_a_policy_without_its_defaults_says_so() -> None:
    """A grid alone still answers, but the literals standing in for the rest are named."""
    cfg = write("gridonly.yaml", BASE_PROJECT + """extends:
  - scrumia-teams
settings:
  team:
    execution:
      matrix:
        L: { high: opus }
""")
    code, out, err = run(PICK, ["--scope", "L", "--risk", "high"], cfg)
    answer = as_json(out) or {}
    check("AC-22: a grid with no configured defaults answers, and names what stood in",
          code == 0 and answer.get("model") == "opus"
          and "unlabeled" in err and "unrated_risk" in err, f"{code} {out} {err}")


def test_one_configured_prefix_does_not_cover_the_other() -> None:
    """AC-11's project keeps its own labels — and forgets one of the two prefixes."""
    cfg = write("halflabels.yaml", BASE_PROJECT + """extends:
  - scrumia-teams
settings:
  team:
    execution:
      unlabeled: sonnet
      unrated_risk: medium
      labels:
        scope_prefix: "size/"
      matrix:
        L: { medium: opus }
""")
    code, out, err = run(PICK, ["--scope", "L"], cfg)
    check("AC-22: the prefix no layer carries is named, though its sibling was configured",
          code == 0 and "labels.risk_prefix=risk/" in err
          and "labels.scope_prefix" not in err, f"{code} {out} {err}")


def test_doctor_diagnoses_rather_than_dies() -> None:
    """The one command whose contract is "tell me what is broken" must survive it."""
    cfg = write("doctor.yaml", RETIRED_SHAPE)
    code, out, err = run(BOARD, ["doctor"], cfg, resolver=False)
    answer = as_json(out) or {}
    check("AC-19: doctor reports the unresolved composition as a failed check",
          answer.get("checks", {}).get("settings_resolved") is False
          and answer.get("ok") is False, f"{code} {out} {err}")
    check("AC-19: and names it as the cause, ahead of the symptoms it produces",
          "scrumia-extends" in (answer.get("detail") or ""), answer.get("detail"))


def test_a_bare_key_mid_migration_is_absence_not_a_value() -> None:
    """jq's recursive merge propagates an explicit null; a config error must not silently win."""
    cfg = write("nullkey.yaml", BASE_PROJECT + f"""modules:
  "{TEAMS_KEY}":
    params:
      execution:
        unrated_risk:
        matrix:
          L: {{ critical: opus, medium: sonnet }}
settings:
  team:
    execution:
      unrated_risk: critical
""")
    code, out, err = run(PICK, ["--scope", "L"], cfg)
    answer = as_json(out) or {}
    check("AC-22: a key written bare in the migrated shape does not overwrite the base layer",
          code == 0 and answer.get("risk") == "critical" and answer.get("model") == "opus",
          f"{code} {out} {err}")


def test_doctor_does_not_certify_an_empty_board() -> None:
    """The resolver ran, and no layer carried the board — AC-19's third case."""
    cfg = write("emptyboard.yaml", BASE_PROJECT + "extends:\n  - scrumia-github-project\nsettings: {}\n")
    code, out, err = run(BOARD, ["doctor"], cfg)
    answer = as_json(out) or {}
    check("AC-19: doctor reports settings_resolved false when no layer carries the board",
          answer.get("checks", {}).get("settings_resolved") is False, f"{code} {out} {err}")
    check("AC-19: and says so, rather than reporting a symptom with no cause",
          "no layer of the cascade" in (answer.get("detail") or ""), answer.get("detail"))


def test_the_soft_gate_is_not_environment_settable() -> None:
    """Only the doctor dispatch may lift the gate; the environment may not."""
    cfg = write("softgate.yaml", RETIRED_SHAPE)
    env_extra = {"SOFT_SETTINGS": "yes"}
    code, out, err = run(BOARD, ["find", "1"], cfg, resolver=False, extra_env=env_extra)
    answer = as_json(out) or {}
    check("AC-19: SOFT_SETTINGS from the environment does not let a command past the gate",
          code != 0 and "scrumia-extends" in (answer.get("error") or ""), f"{code} {out} {err}")


def test_a_hole_in_the_grid_still_answers() -> None:
    """AC-10 is untouched: a missing *cell* is data, and stays answerable."""
    cfg = write("hole.yaml", RETIRED_SHAPE)
    code, out, err = run(PICK, ["--scope", "XL", "--risk", "low"], cfg)
    answer = as_json(out) or {}
    check("AC-10 unchanged: a grid with no cell for the pair still answers the default",
          code == 0 and answer.get("model") == "sonnet", f"{code} {out} {err}")
    check("AC-22 vs AC-10: the two cases are distinguishable by ok:",
          answer.get("ok") is True, f"{code} {out} {err}")


def test_board_settings_gate_before_the_api() -> None:
    """Every board setting resolves through the cascade — including the column mapping."""
    cfg = write("cols.yaml", BASE_PROJECT + "extends:\n  - scrumia-github-project\nsettings: {}\n")
    local = write("cols.local.yaml", """settings:
  tracker:
    project_number: 5
    board:
      field_id: "FIELD_LOCAL"
      flow:
        in_progress: "Doing"
      options:
        Doing: "opt-local"
""")
    code, out, err = run(BOARD, ["move", "1", "in_progress"], cfg, local=local)
    answer = as_json(out) or {}
    error = answer.get("error") or ""
    check("AC-18: project number, field id, flow step and option id all resolve from layer 3",
          code != 0 and "graphql lookup failed" in error, f"{code} {out} {err}")

    code, out, err = run(BOARD, ["move", "1", "in_progress"], cfg)
    answer = as_json(out) or {}
    check("AC-19: without that layer the board names the missing setting, and stops",
          code != 0 and "project_number" in (answer.get("error") or ""), f"{code} {out} {err}")


def main() -> int:
    print("Settings cascade — the consuming half (#315)\n")
    for test in (test_layer_three_reaches_the_policy,
                 test_layer_three_reaches_the_board,
                 test_layer_two_reaches_both,
                 test_params_outrank_settings_on_the_same_key,
                 test_a_local_source_resolves,
                 test_a_partial_migration_keeps_both_halves,
                 test_no_resolver_stops_both_tools,
                 test_no_policy_at_all_stops_the_tool,
                 test_an_empty_policy_block_is_not_a_policy,
                 test_a_policy_without_its_defaults_says_so,
                 test_one_configured_prefix_does_not_cover_the_other,
                 test_doctor_diagnoses_rather_than_dies,
                 test_doctor_does_not_certify_an_empty_board,
                 test_the_soft_gate_is_not_environment_settable,
                 test_a_bare_key_mid_migration_is_absence_not_a_value,
                 test_a_hole_in_the_grid_still_answers,
                 test_board_settings_gate_before_the_api):
        print(f"\n{test.__name__}")
        test()

    shutil.rmtree(TMP, ignore_errors=True)
    if FAILURES:
        print(f"\n{len(FAILURES)} failure(s):")
        for line in FAILURES:
            print(f"  - {line}")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
