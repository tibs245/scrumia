#!/usr/bin/env python3
"""Measure design/tokens.css against the WCAG minimum of every real pair, both themes.

Run from anywhere: python3 tools/check_contrast.py [-v]. Non-zero if a pair misses.
"""

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "design" / "tokens.css"

DECL = re.compile(r"^\s*(--[a-z0-9-]+)\s*:\s*(.+?);", re.MULTILINE | re.DOTALL)
LIGHT_DARK = re.compile(r"^light-dark\(\s*(#[0-9A-Fa-f]{6})\s*,\s*(#[0-9A-Fa-f]{6})\s*\)$")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")

# Minimums are WCAG 2.1: 4.5 for body text (1.4.3), 3.0 for a boundary that
# carries meaning (1.4.11).
PAIRS = [
    # 4.5 not 3.0: the run has no wash left, so both actors now carry text.
    ("human", "ground", 4.5, ".step-title, .step-who and the filled .step-dot, human step"),
    ("agent", "ground", 4.5, ".step-who and the .step-dot ring, agent step"),
    ("agent", "agent-surface", 4.5, ".badge — module name on its wash"),
    ("agent", "surface", 4.5, ".flow-num numeral and ring, .card-manager left rule"),
    ("human", "human-surface", 4.5, ".flow-human .flow-num, .badge-human, .note-warn title"),
    ("text", "agent-surface", 4.5, "text on the agent wash"),
    ("text-soft", "human-surface", 4.5, ".opt description, on a chosen option"),
    # #56: the composer draws a chosen module name in the human hue, as text on
    # the ground. The 3.0 pair above is a rule and a dot; this one is read.
    ("human", "ground", 4.5, ".slots-choose .slot-fill — a chosen module name"),
    ("text", "ground", 4.5, "body copy on the ground"),
    ("text-soft", "ground", 4.5, "secondary copy on the ground"),
    ("text-faint", "ground", 4.5, "mono labels on the ground"),
    ("text", "surface", 4.5, "body copy on a surface"),
    ("text-faint", "surface-sunken", 4.5, "code and inputs"),
    ("agent", "surface-sunken", 4.5, "pre .m — module names inside a generated file"),
    ("accent", "ground", 4.5, "the accent as a link"),
    ("accent", "surface", 4.5, "the accent on a card"),
    ("accent", "accent-surface", 4.5, ".note title on its wash"),
    ("accent-ink", "accent", 4.5, "text laid on the solid accent"),
    ("ok", "ground", 4.5, "the available pill"),
    ("border-strong", "ground", 3.0, "control outlines — the 3:1 UI minimum"),
    ("border-strong", "surface", 3.0, "control outlines on a surface"),
    ("text", "surface-sunken", 4.5, ".key-entry-field — a key typed into the field"),
    # The thinnest margin in key-entry: re-measure if --human-surface ever moves.
    ("text-faint", "human-surface", 4.5, ".key-entry-label, on a chosen option"),
    ("border-strong", "surface-sunken", 3.0, ".key-entry-field's own boundary"),
]

# identity.md decision 4: the human blue lives a hue category off the accent
# cyan, or the human mark starts reading as the thing that points. Contrast is a
# luminance ratio and cannot see this, which is how it would ship unnoticed.
HUE_FLOORS = [("human", "accent", 35.0, 8.0)]


def parse(text: str) -> dict[str, tuple[str, str]]:
    """Every token that resolves to a literal colour, as (light, dark)."""
    out = {}
    # Prose in this file discusses declarations, and a sentence is not a token.
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    for name, value in DECL.findall(text):
        value = " ".join(value.split())
        if m := LIGHT_DARK.match(value):
            out[name[2:]] = (m.group(1), m.group(2))
        elif HEX.match(value):
            out[name[2:]] = (value, value)
    return out


def _linear(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _rgb(value: str) -> tuple[float, float, float]:
    h = value.lstrip("#")
    return tuple(_linear(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def ratio(fg: str, bg: str) -> float:
    def lum(v):
        r, g, b = _rgb(v)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def oklab(value: str) -> tuple[float, float, float]:
    r, g, b = _rgb(value)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def hue_gap(x: str, y: str) -> float:
    def angle(v):
        _, a, b = oklab(v)
        return math.degrees(math.atan2(b, a)) % 360
    d = abs(angle(x) - angle(y)) % 360
    return min(d, 360 - d)


def delta_e(x: str, y: str) -> float:
    return math.dist(oklab(x), oklab(y)) * 100


def main() -> int:
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    palette = parse(TOKENS.read_text())
    failures = []

    for theme, index in (("light", 0), ("dark", 1)):
        for fg, bg, minimum, what in PAIRS:
            missing = [n for n in (fg, bg) if n not in palette]
            if missing:
                failures.append(f"{theme}: {what} — no such token: {', '.join(missing)}")
                continue
            a, b = palette[fg][index], palette[bg][index]
            got = ratio(a, b)
            ok = got >= minimum
            if not ok:
                failures.append(
                    f"{theme}: {what} — --{fg} on --{bg} is {got:.2f}:1, "
                    f"needs {minimum}:1 ({a} on {b})")
            if verbose:
                print(f"  {'ok  ' if ok else 'FAIL'} {theme:5} {got:>6.2f} "
                      f"(min {minimum}) --{fg} on --{bg} — {what}")

        for x, y, min_hue, min_de in HUE_FLOORS:
            a, b = palette[x][index], palette[y][index]
            h, e = hue_gap(a, b), delta_e(a, b)
            ok = h >= min_hue and e >= min_de
            if not ok:
                failures.append(
                    f"{theme}: --{x} and --{y} are {h:.1f}° / dE {e:.1f} apart, "
                    f"needs {min_hue}° / dE {min_de} — see identity.md decision 4")
            if verbose:
                print(f"  {'ok  ' if ok else 'FAIL'} {theme:5} {h:>6.1f}° dE {e:>5.1f} "
                      f"--{x} vs --{y} — hue separation")

    for line in failures:
        print(f"error: {line}", file=sys.stderr)
    total = len(PAIRS) * 2 + len(HUE_FLOORS) * 2
    print(f"{len(failures)} failure(s) over {total} measured pair(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
