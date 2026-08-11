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
actions:
  merge/approve: human
  build/apply-implementation: not-applicable
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


def test_ac1_readable_and_names_what_is_plugged_in() -> None:
    print("AC-1 — reads well in a real terminal, names every module it runs")
    config = config_with(PROJECT_CONFIG)
    out = ANSI.sub("", run_tty(env_for(config, COLUMNS="100"))).replace("\r\n", "\n")

    check("names the project", "Demo" in out and "acme/demo" in out)
    check("lists every module extends names", all(m in out for m in
          ("scrumia-specs", "scrumia-github-project", "scrumia-teams", "scrumia-design")))
    check("names no module the project does not run", "scrumia-discovery" not in out)
    check("shows each app and what it extends", "site" in out and "Extends" in out)
    check("reports the actions this project answers itself",
          "merge/approve" in out and "human" in out)
    check("a not-applicable answer keeps its own wording",
          "build/apply-implementation" in out and "not-applicable" in out)
    check("points at what derives the rest", "scrumia-assemble" in out)

    rows = [l for l in out.split("\n")
            if re.match(r"^  (merge/approve|build/apply-implementation) ", l)]
    offsets = {len(l) - len(l.lstrip()[len(l.split()[0]):].lstrip()) for l in rows}
    check("the answer column is aligned", len(rows) == 2 and len(offsets) == 1,
          f"{len(rows)} rows, offsets {offsets}")

    lines = out.split("\n")
    check("no line overflows the terminal", all(len(l) <= 100 for l in lines),
          "longest %d" % max((len(l) for l in lines), default=0))
    os.unlink(config)


def test_ac1_narrow_terminal() -> None:
    print("AC-1 — alignment survives a narrow terminal")
    config = config_with(PROJECT_CONFIG)
    for cols in (30, 40, 60):
        out = ANSI.sub("", run_tty(env_for(config, COLUMNS=str(cols)))).replace("\r\n", "\n")
        # Unbreakable by design, and exempt: a shell command, and a lone token
        # such as a slash-command name. Folding either breaks the copy-paste.
        def foldable(line: str) -> bool:
            return len(line.split()) > 1 and not line.strip().startswith("claude ")

        over = [l for l in out.split("\n") if len(l) > cols and foldable(l)]
        check(f"nothing foldable overflows at {cols} columns", not over, f"{over[:1]!r}")
        check(f"still names every module at {cols} columns",
              all(m in out for m in ("scrumia-specs", "scrumia-design")))
        check(f"still reports the project's own answers at {cols} columns",
              "merge/approve" in out and "human" in out)
    os.unlink(config)

    # A long per-app extends list is the widest thing the table can carry; it must
    # push the layout narrow rather than run off the side.
    crowded = config_with(CROWDED_CONFIG)
    for cols in (80, 100):
        out = ANSI.sub("", run_tty(env_for(crowded, COLUMNS=str(cols)))).replace("\r\n", "\n")
        over = [l for l in out.split("\n") if len(l) > cols and len(l.split()) > 1
                and not l.strip().startswith("claude ")]
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
          ANSI.sub("", tty).replace("\r\n", "\n") == piped)
    os.unlink(config)


def test_ac3_read_only_and_no_argument() -> None:
    print("AC-3 — writes nothing, needs no argument")
    before = snapshot(ROOT)
    code, out, err = run_piped(env_for())
    after = snapshot(ROOT)

    check("exits 0 with no argument in a configured repo", code == 0, f"exit {code}, {err.strip()}")
    check("prints something to stdout", len(out.strip()) > 0)
    check("nothing on stderr", err == "", err.strip())
    check("no file created, changed or touched", before == after,
          str(set(before) ^ set(after))[:200])

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
    _, out, _ = run_piped(env_for(config))
    check("the modules it names are still reported",
          "scrumia-specs" in out and "scrumia-github-project" in out)
    check("a null entry contributes nothing rather than a row",
          "null" not in out and "none" not in out.split("Extends")[0])
    check("the per-app implementation and practices fold into that app's extends",
          "scrumia-impl-solidjs" in out and "scrumia-practice-tdd" in out)
    check("the reader is told the shape is retired", "retired" in out)
    check("the advice is given once, not repeated per key",
          out.count("retired") == 1, out.count("retired"))
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
        out = ANSI.sub("", run_tty(env_for(config, COLUMNS=cols))).replace("\r\n", "\n")
        check(f"the name survives a glob character at {cols} columns",
              "R&D * team" in out or ("R&D" in out and "* team" in out), out[:120])
        check(f"no repository file leaks into the output at {cols} columns",
              "compose-status.sh" not in out and "README.md" not in out, out[:200])
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
    test_ac4_both_skills_end_by_running_it()
    print(f"\n{len(FAILURES)} failure(s)")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
