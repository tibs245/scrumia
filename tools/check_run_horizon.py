#!/usr/bin/env python3
"""Measure the home page's run section against its acceptance criteria.

Run from anywhere: python3 tools/check_run_horizon.py [-v]. Non-zero if a rule breaks.

The line budget is a pixel fact — two lines at 1400px in French is not something
reading the copy can confirm — so the widths below are rendered in headless
Chrome and read back. Exit 2, not 1, when no browser is found: a check that
passes because it could not run is worse than one that is missing.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE = ROOT / "site" / "assets" / "style.css"
PAGES = {"en": ROOT / "site" / "index.html", "fr": ROOT / "site" / "fr" / "index.html"}
CHROMES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]
# Both sides of the run's one threshold, and the extremes on either side of it.
WIDTHS = [1920, 1512, 1440, 1439, 1280, 1024, 901, 768, 390]
HUMAN_STEPS = 3
TOTAL_STEPS = 7

PROBE = """
<script>
(function () {
  function lines(el) {
    var lh = parseFloat(getComputedStyle(el).lineHeight);
    return Math.round(el.getBoundingClientRect().height / lh);
  }
  var steps = [].map.call(document.querySelectorAll('.step'), function (s) {
    var dot = s.querySelector('.step-dot');
    var cs = getComputedStyle(dot);
    return {
      no: s.querySelector('.step-no').textContent,
      human: s.classList.contains('step-human'),
      title: lines(s.querySelector('.step-title')),
      out: lines(s.querySelector('.step-out')),
      who: (s.querySelector('.step-who') || {}).textContent || '',
      fill: cs.backgroundColor,
      ring: cs.borderTopColor
    };
  });
  var track = document.querySelector('.run-track');
  document.title = 'PROBE' + JSON.stringify({
    track: Math.round(track.getBoundingClientRect().width),
    ground: getComputedStyle(document.body).backgroundColor,
    horizon: getComputedStyle(document.querySelector('.run-horizon')).display,
    steps: steps
  });
})();
</script>
"""


def find_chrome() -> str | None:
    return next((c for c in CHROMES if Path(c).exists()), None)


def render(chrome: str, page: Path, width: int) -> dict:
    html = page.read_text(encoding="utf-8").replace("</body>", PROBE + "</body>")
    tmp = page.with_name("_probe.html")
    tmp.write_text(html, encoding="utf-8")
    try:
        dom = subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--force-prefers-reduced-motion", "--force-device-scale-factor=1",
             "--virtual-time-budget=4000", f"--window-size={width},1600",
             "--dump-dom", tmp.as_uri()],
            capture_output=True, text=True, timeout=120).stdout
    finally:
        tmp.unlink(missing_ok=True)
    found = re.search(r"<title>PROBE(.*?)</title>", dom, re.DOTALL)
    if not found:
        raise RuntimeError(f"{page.name} at {width}px rendered no measurement")
    text = found.group(1)
    for entity, char in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"')):
        text = text.replace(entity, char)
    return json.loads(text)


def balanced(css: str, start: int) -> tuple[str, int]:
    """The body of the { } opening at `start`, and the index just past its close."""
    depth = 0
    for i in range(start, len(css)):
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                return css[start + 1:i], i + 1
    raise ValueError("unbalanced braces in " + str(STYLE))


def rules(css: str):
    """Every (prelude, body) pair, descending through at-rules into their contents."""
    i = mark = 0
    while i < len(css):
        if css[i] == "{":
            prelude = css[mark:i].strip()
            body, end = balanced(css, i)
            if prelude.startswith("@") and "{" in body:
                yield from rules(body)
            else:
                yield prelude, body
            i = mark = end
        elif css[i] == "}":
            i += 1
            mark = i
        else:
            i += 1


def check_css(fail, verbose: bool) -> None:
    """AC-4, and it needs no browser: one animated glow, on the human mark alone."""
    css = re.sub(r"/\*.*?\*/", "", STYLE.read_text(encoding="utf-8"), flags=re.DOTALL)
    glowing = [name for name in re.findall(r"@keyframes\s+([\w-]+)", css)
               if "box-shadow" in balanced(css, css.index("{", css.index("@keyframes " + name)))[0]]
    if glowing != ["bloom"]:
        fail(f"AC-4: the animated glows are {glowing or 'none'}, expected exactly ['bloom']")
    users = [sel for sel, body in rules(css) if re.search(r"animation:\s*bloom\b", body)]
    if not users:
        fail("AC-4: nothing consumes the bloom — the flare is dead code")
    for sel in users:
        if ".step-human" not in sel:
            fail(f"AC-4: the bloom is spent outside the human mark, on '{sel}'")
    if verbose and glowing == ["bloom"] and users:
        print(f"  ok    AC-4  bloom is the only animated glow, on {users}")


def check_page(data: dict, lang: str, width: int, fail, verbose: bool) -> None:
    steps = data["steps"]
    if len(steps) != TOTAL_STEPS:
        fail(f"{lang} {width}: {len(steps)} steps, expected {TOTAL_STEPS}")
        return

    for s in steps:
        # AC-1 — the copy gives way before the layout does.
        if s["title"] != 1:
            fail(f"{lang} {width}: step {s['no']} title runs {s['title']} lines")
        if s["out"] > 2:
            fail(f"{lang} {width}: step {s['no']} runs {s['out']} lines, budget is 2")
        # AC-3 — the actor is a word on both variants, not an absence on one.
        if not s["who"].strip():
            fail(f"{lang} {width}: step {s['no']} names no actor")

    # AC-2 — three of seven, countable before a word is read.
    human = [s for s in steps if s["human"]]
    if len(human) != HUMAN_STEPS:
        fail(f"{lang} {width}: {len(human)} human steps, expected {HUMAN_STEPS}")

    # AC-3 — filled versus hollow, because the two hues share a luminance.
    for s in steps:
        filled = s["fill"] == s["ring"]
        if s["human"] and not filled:
            fail(f"{lang} {width}: human step {s['no']} draws a hollow mark")
        if not s["human"] and filled:
            fail(f"{lang} {width}: agent step {s['no']} draws a filled mark")

    # The horizon exists only where it fits; below that the rail carries the run.
    wide = width >= 1440
    if wide and data["horizon"] == "none":
        fail(f"{lang} {width}: the horizon is hidden at a width that fits it")
    if not wide and data["horizon"] != "none":
        fail(f"{lang} {width}: the horizon is drawn below the width it needs")
    if wide and data["track"] < 1400:
        fail(f"{lang} {width}: the track is {data['track']}px, expected --page-wide")

    if verbose:
        shape = "horizon" if wide else "rail   "
        print(f"  ok    {lang} {width:>4} {shape} track={data['track']:>4} "
              + " ".join(f"{s['no']}:{s['out']}" for s in steps))


def main() -> int:
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    failures: list[str] = []
    check_css(failures.append, verbose)

    chrome = find_chrome()
    if not chrome:
        print("error: no Chrome or Chromium found — the line budget went unmeasured",
              file=sys.stderr)
        return 2

    for lang, page in PAGES.items():
        if not page.exists():
            failures.append(f"{page.relative_to(ROOT)}: missing — run tools/build_site.py first")
            continue
        for width in WIDTHS:
            check_page(render(chrome, page, width), lang, width, failures.append, verbose)

    for line in failures:
        print(f"error: {line}", file=sys.stderr)
    print(f"{len(failures)} failure(s) over {len(PAGES) * len(WIDTHS)} rendered page(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
