#!/usr/bin/env python3
"""Acceptance tests for plugins/scrumia-core/scripts/compose-status.sh (#63).

Run from the repo root: python3 tools/test_compose_status.py
Exit code 0 when everything passes, 1 otherwise. No dependencies.
"""

import os
import pty
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "scrumia-core" / "scripts" / "compose-status.sh"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  ok    {name}")
    else:
        detail = str(detail)
        FAILURES.append(f"{name}{' — ' + detail if detail else ''}")
        print(f"  FAIL  {name}{' — ' + detail if detail else ''}")


def env_for(config: Path | None = None, **extra: str) -> dict[str, str]:
    env = dict(os.environ)
    env.pop("NO_COLOR", None)
    if config is not None:
        env["SCRUMIA_CONFIG"] = str(config)
    env.update(extra)
    return env


def run_piped(env: dict[str, str], args: list[str] | None = None):
    proc = subprocess.run(
        [str(SCRIPT), *(args or [])], cwd=ROOT, env=env, capture_output=True, text=True
    )
    return proc.returncode, proc.stdout, proc.stderr


# Unbreakable by design and exempt: a shell command, a lone token such as a
# slash-command name, and a path — wrap folds at word boundaries or not at all,
# so a line carrying one word past the width is the width's problem, not a defect.
def foldable(line: str) -> bool:
    body = line.split("compose-status.sh:", 1)[-1]
    return len(body.split()) > 1 and not body.strip().startswith("claude ")


def report_only(text: str) -> str:
    """The report, without the tool's own notices.

    A pty carries one stream, so a terminal capture holds stdout and stderr
    interleaved. Every assertion about what the composition *says* runs on the
    report; the notices are asserted separately, where they belong.
    """
    out, in_notice = [], False
    for line in text.split("\n"):
        if line.startswith("compose-status.sh:"):
            in_notice = True
            continue
        if in_notice and line.strip():
            continue
        in_notice = False
        out.append(line)
    return "\n".join(out)


def run_tty(env: dict[str, str]) -> str:
    """Same call, but with a real terminal on stdout — the colour path."""
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(ROOT)
        os.execvpe(str(SCRIPT), ["compose-status.sh"], env)
        os._exit(127)
    chunks = []
    try:
        while True:
            data = os.read(fd, 4096)
            if not data:
                break
            chunks.append(data)
    except OSError:
        pass
    os.waitpid(pid, 0)
    return b"".join(chunks).decode("utf-8", "replace")


def snapshot(root: Path) -> dict[str, tuple[int, int]]:
    out = {}
    for path in root.rglob("*"):
        if ".git" in path.parts or ".worktrees" in path.parts or not path.is_file():
            continue
        st = path.stat()
        out[str(path)] = (st.st_size, st.st_mtime_ns)
    return out


def config_with(body: str) -> Path:
    handle = tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False, encoding="utf-8"
    )
    handle.write(body)
    handle.close()
    return Path(handle.name)


PROJECT_CONFIG = """
project:
  name: "Demo"
  repo: "acme/demo"
extends:
  - scrumia-specs
  - scrumia-github-project
  - scrumia-teams
  - scrumia-design
apps:
  - name: "site"
    path: "site"
    extends: []
"""

CROWDED_CONFIG = """
project:
  name: "Wide"
extends:
  - scrumia-specs
  - scrumia-github-project
apps:
  - name: "web"
    path: "apps/web"
    extends: [scrumia-impl-solidjs, scrumia-practice-tdd, scrumia-practice-solid, scrumia-practice-tanstack-query]
"""

# The retired shape, tolerated for one minor: read, and said out loud.
LEGACY_CONFIG = """
project:
  name: "Demo"
composition:
  specs: scrumia-specs
  tracker: scrumia-github-project
  design: null
apps:
  - name: "web"
    path: "apps/web"
    implementation: scrumia-impl-solidjs
    practices: [scrumia-practice-tdd]
"""

# Nothing plugged in: a flat list has no per-slot key to leave empty, so the
# absence has to be said rather than shown as a column of nulls.
EMPTY_CONFIG = """
project:
  name: "Bare"
extends: []
apps: []
"""

# The current shape: one mapping, every key qualified by the source it comes from,
# and one bare name that is not a declaration at all.
MODULES_CONFIG = """
project:
  name: "Demo"
  repo: "acme/demo"
modules:
  "tibs245/scrumia:scrumia-specs":
    params:
      root: features
  "shared:acme-conventions": {}
  "local:acme-docs-rules": {}
apps:
  - name: "web"
    path: "apps/web"
    modules:
      "tibs245/scrumia:scrumia-practice-tdd": {}
"""

UNSOURCED_CONFIG = """
project:
  name: "Bare name"
modules:
  "scrumia-specs": {}
  ":scrumia-teams": {}
  "github:scrumia-design": {}
  "local:acme-docs-rules": {}
"""

LOCAL_LAYER = """
settings:
  autonomy:
    level: autonomous
"""


def test_ac1_readable_and_names_what_is_plugged_in() -> None:
    print("AC-1 — reads well in a real terminal, names every module it runs")
    config = config_with(PROJECT_CONFIG)
    out = report_only(ANSI.sub("", run_tty(env_for(config, COLUMNS="100"))).replace("\r\n", "\n"))

    check("names the project", "Demo" in out and "acme/demo" in out)
    check("lists every module extends names", all(m in out for m in
          ("scrumia-specs", "scrumia-github-project", "scrumia-teams", "scrumia-design")))
    check("names no module the project does not run", "scrumia-discovery" not in out)
    check("shows each app and what it extends", "site" in out and "Extends" in out)
    check("points at what carries the rest", "scrumia-extends --list" in out)
    check("resolves no register itself",
          "implement" not in out and "required" not in out)

    rows = [l for l in out.split("\n") if re.match(r"^  site +site", l)]
    check("the app table's columns are aligned", len(rows) == 1, f"{len(rows)} rows")

    lines = out.split("\n")
    check("no line overflows the terminal", all(len(l) <= 100 for l in lines),
          "longest %d" % max((len(l) for l in lines), default=0))
    os.unlink(config)


def test_ac1_narrow_terminal() -> None:
    print("AC-1 — alignment survives a narrow terminal")
    config = config_with(PROJECT_CONFIG)
    for cols in (30, 40, 60):
        out = ANSI.sub("", run_tty(env_for(config, COLUMNS=str(cols)))).replace("\r\n", "\n")
        over = [l for l in out.split("\n") if len(l) > cols and foldable(l)]
        check(f"nothing foldable overflows at {cols} columns", not over, f"{over[:1]!r}")
        check(f"still names every module at {cols} columns",
              all(m in out for m in ("scrumia-specs", "scrumia-design")))
        # The footer wraps at these widths, so the name is what has to survive,
        # not the whole invocation.
        check(f"still points at what carries the rest at {cols} columns",
              "scrumia-extends" in out)
    os.unlink(config)

    # A long per-app extends list is the widest thing the table can carry; it must
    # push the layout narrow rather than run off the side.
    crowded = config_with(CROWDED_CONFIG)
    for cols in (80, 100):
        out = ANSI.sub("", run_tty(env_for(crowded, COLUMNS=str(cols)))).replace("\r\n", "\n")
        over = [l for l in out.split("\n") if len(l) > cols and foldable(l)]
        check(f"a crowded apps table still fits {cols} columns", not over, f"{over[:1]!r}")
        check(f"every practice is still named at {cols} columns",
              all(p in out for p in ("scrumia-practice-tdd", "scrumia-practice-solid",
                                     "scrumia-practice-tanstack-query")))
    os.unlink(crowded)


def test_ac2_colour_gating() -> None:
    print("AC-2 — colour only on a TTY, and NO_COLOR honoured")
    config = config_with(PROJECT_CONFIG)

    _, piped, _ = run_piped(env_for(config))
    check("no escape sequence when stdout is a pipe", "\x1b[" not in piped)

    tty = run_tty(env_for(config, COLUMNS="100"))
    check("colour when stdout is a terminal", "\x1b[" in tty)

    muted = run_tty(env_for(config, COLUMNS="100", NO_COLOR="1"))
    check("NO_COLOR=1 drops colour on a terminal", "\x1b[" not in muted)

    still = run_tty(env_for(config, COLUMNS="100", NO_COLOR=""))
    check("NO_COLOR set but empty keeps colour", "\x1b[" in still)

    check("the piped text matches the terminal text",
          report_only(ANSI.sub("", tty).replace("\r\n", "\n")) == piped)
    os.unlink(config)


def test_ac3_read_only_and_no_argument() -> None:
    print("AC-3 — writes nothing, needs no argument")
    before = snapshot(ROOT)
    code, out, err = run_piped(env_for())
    after = snapshot(ROOT)

    check("exits 0 with no argument in a configured repo", code == 0, f"exit {code}, {err.strip()}")
    check("prints something to stdout", len(out.strip()) > 0)
    check("stderr says nothing on this repository's own config", err == "", err.strip())
    check("no file created, changed or touched", before == after,
          str(set(before) ^ set(after))[:200])

    # A migrated config earns silence: a warning every run is a warning nobody reads.
    migrated = config_with(MODULES_CONFIG)
    code, out, err = run_piped(env_for(migrated))
    check("a config on modules: says nothing on stderr", err == "", err.strip())
    check("and still prints its composition", "Demo" in out, out[:120])
    os.unlink(migrated)

    retired = config_with(PROJECT_CONFIG)
    _, _, err = run_piped(env_for(retired))
    check("a config still on the retired extends: is told to migrate",
          err.startswith("compose-status.sh:") and "migrate to 'modules:'" in err,
          err.strip())
    os.unlink(retired)

    code, _, err = run_piped(env_for(), ["--help"])
    check("--help documents the call", code == 2 and "compose-status.sh" in err)

    code, _, err = run_piped(env_for(), ["63"])
    check("an unexpected argument is refused, not ignored", code == 2)

    missing = Path(tempfile.gettempdir()) / "scrumia-no-such-config.yaml"
    code, out, err = run_piped(env_for(missing))
    check("a missing config fails loudly on stderr",
          code == 1 and "scrumia-init" in err and out == "", f"exit {code}")


def test_ac3_the_retired_shape_is_read_and_said_out_loud() -> None:
    print("AC-3 — the retired composition:/practices: keys are read, and named as retired")
    config = config_with(LEGACY_CONFIG)
    _, out, err = run_piped(env_for(config))
    check("the modules it names are still reported",
          "scrumia-specs" in out and "scrumia-github-project" in out)
    check("a null entry contributes nothing rather than a row",
          "null" not in out and "none" not in out.split("Extends")[0])
    check("the per-app implementation and practices fold into that app's extends",
          "scrumia-impl-solidjs" in out and "scrumia-practice-tdd" in out)
    # The report is what the site publishes verbatim; a migration is the reader's
    # business and belongs on the stream a published artefact does not carry.
    check("the reader is told the shape is retired", "retired" in err, err.strip())
    check("the advice is given once, not repeated per key",
          err.count("retired") == 1, err.count("retired"))
    check("the report itself stays free of it", "retired" not in out)
    os.unlink(config)

    bare = config_with(EMPTY_CONFIG)
    _, out, _ = run_piped(env_for(bare))
    check("an empty extends is stated, not shown as a blank table",
          "extends is empty" in out, out[:200])
    check("nothing is called not declared, since there is no key to omit",
          "not declared" not in out)
    os.unlink(bare)


def test_ac3_config_text_is_never_expanded() -> None:
    print("AC-3 — config text is printed, never expanded against the filesystem")
    config = config_with(PROJECT_CONFIG.replace('name: "Demo"', 'name: "R&D * team"'))
    for cols in ("25", "100"):
        out = report_only(ANSI.sub("", run_tty(env_for(config, COLUMNS=cols))).replace("\r\n", "\n"))
        check(f"the name survives a glob character at {cols} columns",
              "R&D * team" in out or ("R&D" in out and "* team" in out), out[:120])
        check(f"no repository file leaks into the output at {cols} columns",
              "compose-status.sh" not in out and "README.md" not in out, out[:200])
    os.unlink(config)


def test_ac17_the_key_carries_the_source() -> None:
    print("AC-17 — a module is reported under the key it is declared by")
    config = config_with(MODULES_CONFIG)
    _, out, err = run_piped(env_for(config, COLUMNS="140"))

    for key in ("tibs245/scrumia:scrumia-specs", "shared:acme-conventions",
                "local:acme-docs-rules"):
        check(f"{key} is reported by its key, source included", key in out, out[:300])
    check("an app's own modules are keyed the same way",
          "tibs245/scrumia:scrumia-practice-tdd" in out, out[:400])
    # Never "runs": this resolves nothing, and BR-6 forbids one tool claiming present what
    # the resolver reports absent.
    check("the heading claims a declaration, not a presence it did not check",
          "Modules this project declares" in out and "extends" not in out.split("App")[0])
    check("a module's params are shown beside it", "root=features" in out, out[:300])
    check("no migration notice for a config already on modules:", err == "", err.strip())
    os.unlink(config)

    bare = config_with(UNSOURCED_CONFIG)
    _, out, _ = run_piped(env_for(bare, COLUMNS="140"))
    check("a bare name is named as not a declaration",
          "'scrumia-specs' is not a declaration" in out, out[:400])
    check("and the grammar it should have used is stated",
          "<source>:<module>" in out, out[:400])
    # One grammar, two readers: a key one of them refuses and the other lists as a
    # module running is the drift the qualified key exists to remove.
    check("a key whose source half is missing is refused too",
          "':scrumia-teams' is not a declaration" in out, out[:600])
    check("a source outside the three BR-13 enumerates is refused",
          "'github:scrumia-design' is not a declaration" in out, out[:600])
    check("a sourced key beside them is not accused",
          "'local:acme-docs-rules' is not a declaration" not in out)
    os.unlink(bare)


def test_ac18_the_local_layer_is_reported_as_such() -> None:
    print("AC-18 — the per-machine layer is named where it changes what resolves")
    config = config_with(MODULES_CONFIG)
    _, without, err = run_piped(env_for(config))
    check("nothing is claimed when there is no local layer",
          "local layer" not in without and "local layer" not in err, without[:200])

    local = config_with(LOCAL_LAYER)
    _, report, err = run_piped(env_for(config, SCRUMIA_CONFIG_LOCAL=str(local)))
    check("the layer in effect is named", "local layer is in effect" in err, err[:300])
    check("the file that holds it is named", str(local) in err)
    check("and the cost is stated, not hidden", "not versioned" in err, err[-400:])
    # The report is versioned and gated by a fixture; what one machine happens to
    # override is the least reproducible thing the tool knows.
    check("the report itself carries nothing machine-local",
          "local layer" not in report and str(local) not in report, report[-300:])
    os.unlink(local)
    os.unlink(config)


def test_ac4_both_skills_end_by_running_it() -> None:
    print("AC-4 — scrumia-init and scrumia-compose end by running it")
    call = "${CLAUDE_SKILL_DIR}/../../scripts/compose-status.sh"
    script_call = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/[\w./-]+\.(?:sh|py)")
    for skill in ("scrumia-init", "scrumia-compose"):
        md = ROOT / "plugins" / "scrumia-core" / "skills" / skill / "SKILL.md"
        text = md.read_text(encoding="utf-8")
        check(f"{skill} invokes the script", call in text)
        if call not in text:
            continue
        calls = script_call.findall(text)
        check(f"{skill} runs it last of all its scripts", calls[-1].endswith("compose-status.sh"),
              f"last is {calls[-1]}")
        tail = text[text.rindex(call):]
        check(f"{skill} has no further procedural step after it",
              "\n## Step" not in tail, "a later step follows the call")


def main() -> int:
    if not os.access(SCRIPT, os.X_OK):
        print(f"error: {SCRIPT.relative_to(ROOT)} is not executable")
        return 1
    test_ac1_readable_and_names_what_is_plugged_in()
    test_ac1_narrow_terminal()
    test_ac2_colour_gating()
    test_ac3_read_only_and_no_argument()
    test_ac3_the_retired_shape_is_read_and_said_out_loud()
    test_ac3_config_text_is_never_expanded()
    test_ac17_the_key_carries_the_source()
    test_ac18_the_local_layer_is_reported_as_such()
    test_ac4_both_skills_end_by_running_it()
    print(f"\n{len(FAILURES)} failure(s)")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
