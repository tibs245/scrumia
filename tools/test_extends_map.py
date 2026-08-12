#!/usr/bin/env python3
"""Tests for the home page's #extends section (features/app/site/extends-map/, #296).

Run from anywhere: python3 tools/test_extends_map.py
Exit code 0 when everything passes, 1 otherwise. No dependencies beyond PyYAML,
already required by tools/build_site.py's own extends_map_specials.

AC-9 is deliberately not covered here — the spec states it as a review obligation
a build cannot check (a diff's meaning against hand-written prose), and AC-2 is
what a build *can* check of it. That is exactly what test_ac2 does.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site as bs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
PAGES = {"en": REPO / "site" / "index.html", "fr": REPO / "site" / "fr" / "index.html"}
CSS = REPO / "site" / "assets" / "style.css"
FAILURES: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ok   {name}")
    else:
        FAILURES.append(f"{name}{': ' + detail if detail else ''}")
        print(f"  FAIL {name}{': ' + detail if detail else ''}")


def extends_section(lang: str) -> str:
    page = PAGES[lang].read_text(encoding="utf-8")
    match = re.search(r'<section id="extends">.*?</section>', page, re.DOTALL)
    if not match:
        raise SystemExit(f"{PAGES[lang]}: no #extends section — run tools/build_site.py first")
    return match.group(0)


def ext_css_block(strip_comments: bool = False) -> str:
    match = re.search(r"/\* ---------- Extends.*?(?=/\* ---------- Modules)", CSS.read_text(encoding="utf-8"), re.DOTALL)
    if not match:
        raise SystemExit(f"{CSS}: no Extends CSS block")
    block = match.group(0)
    return re.sub(r"/\*.*?\*/", "", block, flags=re.DOTALL) if strip_comments else block


# --- AC-1 ----------------------------------------------------------------------


def test_ac1_mechanism_not_a_bare_claim() -> None:
    print("AC-1 the claim ships with a skill, several modules, and the real table — not asserted alone")
    section = extends_section("en")
    check("a declaring skill is shown", "ext-declares" in section)

    # Scoped to the populated row's own <ul>, not a whole-section <li> count.
    populated = re.search(r'<div class="ext-row">(.*?)</div>\s*</div>\s*(?:<!--.*?-->\s*)?'
                           r'<div class="ext-row ext-row-empty">', section, re.DOTALL)
    check("the populated row is found", bool(populated))
    contributors = re.findall(r"<li>", populated.group(1)) if populated else []
    check("more than one module contributes in the populated row", len(contributors) >= 2, str(len(contributors)))

    invocation = re.search(r"<pre><code>(.*?)</code></pre>", section, re.DOTALL)
    check("the invocation is shown", bool(invocation) and "scrumia-extends" in invocation.group(1))
    check("the accent lands on the invocation, the point the claim turns on (identity.md decision 4)",
          bool(invocation) and invocation.group(1).startswith('<span class="k">scrumia-extends</span>'))
    check("the real table follows it", "<tbody><tr>" in section)


# --- AC-2 ----------------------------------------------------------------------


def test_ac2_every_name_is_real() -> None:
    print("AC-2 every module, register and directive named is one this composition actually runs")

    bs.ERRORS.clear()
    live = bs.extends_map_specials()
    check("the live composition produces the figure with no error", bs.ERRORS == [], str(bs.ERRORS))
    check("a populated register is named", bool(live.get("@ext_full_register")))
    check("an empty register is named", bool(live.get("@ext_empty_register")))

    real = bs.load_extends_map(bs.load_project_modules())
    check("the populated register's declaring module is one this project runs",
          live.get("@ext_full_module") in [m for m in bs.load_project_modules()])
    check("the populated register's contributors are real modules",
          all(f"<li><code>{m}</code></li>" in live["@ext_full_contributors"]
              for m in {d["module"] for d in real["directives"].get(bs.EXTENDS_FIGURE["populated"], [])}))

    # The build-time guard: a register this composition does not open must fail
    # loudly rather than let the figure quietly name something invented.
    saved = dict(bs.EXTENDS_FIGURE)
    try:
        bs.EXTENDS_FIGURE["populated"] = "no-such-register"
        bs.ERRORS.clear()
        result = bs.extends_map_specials()
        check("an invented register produces no specials and an error",
              result == {} and any("no-such-register" in e for e in bs.ERRORS), str(bs.ERRORS))
    finally:
        bs.EXTENDS_FIGURE.clear()
        bs.EXTENDS_FIGURE.update(saved)


# --- AC-3 ----------------------------------------------------------------------


def test_ac3_empty_register_is_named_not_omitted() -> None:
    print("AC-3 the empty register is shown and stated in words, not just an absence of lines")
    for lang, words in (("en", "no contribution"), ("fr", "aucune contribution")):
        section = extends_section(lang)
        check(f"[{lang}] the empty row is present", "ext-row-empty" in section)
        check(f"[{lang}] it states the empty state in words", words in section)

    # The build-time guard: if the picked "empty" register gains a contributor,
    # the figure must stop claiming it is empty rather than quietly go stale.
    saved = dict(bs.EXTENDS_FIGURE)
    try:
        bs.EXTENDS_FIGURE["empty"] = bs.EXTENDS_FIGURE["populated"]
        bs.ERRORS.clear()
        result = bs.extends_map_specials()
        check("a now-populated register refuses to stand in as the empty example",
              result == {} and any("empty-register example" in e for e in bs.ERRORS), str(bs.ERRORS))
    finally:
        bs.EXTENDS_FIGURE.clear()
        bs.EXTENDS_FIGURE.update(saved)


# --- AC-4 ----------------------------------------------------------------------


def test_ac4_reaches_reference_and_slots() -> None:
    print("AC-4 the section points at the reference and at #slots, rather than re-explaining either")
    section = extends_section("en")
    check("it links to the reference", 'href="reference.html"' in section)
    check("it links back to #slots", 'href="#slots"' in section)
    page = PAGES["en"].read_text(encoding="utf-8")
    check("#slots exists on the same page", '<section id="slots">' in page)


# --- AC-5 ----------------------------------------------------------------------


def test_ac5_legible_with_no_script() -> None:
    print("AC-5 the claim, figure and table are all present in the static HTML — nothing needs script")
    section = extends_section("en")
    check("no <noscript> fallback is needed (there is nothing to fall back from)",
          "<noscript" not in section)
    check("no element hides the figure's content by default markup",
          not re.search(r"[^-]\bhidden\b", section) and 'style="display' not in section)
    check("the fade-in class is opt-in decoration, not the only way to see the content",
          'class="ext-figure summon"' in section)


# --- AC-6 ----------------------------------------------------------------------


def test_ac6_tokens_only() -> None:
    print("AC-6 the figure carries no literal colour, spacing or duration of its own")
    block = ext_css_block(strip_comments=True)
    literal_color = re.findall(r"#[0-9a-fA-F]{3,8}\b", block)
    literal_fn = re.findall(r"\b(?:rgb|hsl|oklch|oklab)\(", block)
    check("no literal colour", not literal_color, str(literal_color))
    check("no literal colour function outside a token", not literal_fn, str(literal_fn))
    # 0/1px are the stylesheet's own hairline exception; a @media condition is a
    # breakpoint, which cannot read a custom property (run-horizon states why).
    declarations = re.sub(r"@media[^{]*\{", "", block)
    stray_px = [m for m in re.findall(r"(-?\d+)px", declarations) if m not in ("0", "1")]
    check("no stray pixel value beyond the hairline/reset exception", not stray_px, str(stray_px))


# --- AC-7 ----------------------------------------------------------------------


def test_ac7_turns_rather_than_scrolls() -> None:
    print("AC-7 the figure is a vertical list by default, three columns only past a width query")
    block = ext_css_block()
    outside_media = re.split(r"@media[^{]*\{.*?\n\}\n", block, flags=re.DOTALL)[0]
    check(".ext-row carries no grid-template-columns outside a media query",
          "grid-template-columns" not in outside_media)
    media = re.search(r"@media \(min-width: (\d+)px\)\s*\{(.*)\}\s*$", block, re.DOTALL)
    check("a min-width query switches the figure to columns", bool(media))
    if media:
        body = media.group(2)
        check("…and it sets the three-column grid on the rows",
              body.count("grid-template-columns: 1fr 1fr 2fr") == 1, body)
        check("…complementing .slot-row's own max-width: 800px turn",
              media.group(1) == "801", media.group(1))
    for lang in ("en", "fr"):
        section = extends_section(lang)
        check(f"[{lang}] the table is the only element allowed to scroll on its own",
              section.count('class="table-wrap"') == 1)


# --- AC-8 ----------------------------------------------------------------------


def test_ac8_figure_is_not_the_only_carrier() -> None:
    print("AC-8 the four facts are also stated in prose, for a reader who cannot see the figure")
    for lang in ("en", "fr"):
        section = extends_section(lang)
        facts = re.search(r'<ul class="ext-facts">(.*?)</ul>', section, re.DOTALL)
        check(f"[{lang}] a prose fact list exists", bool(facts))
        if not facts:
            continue
        items = re.findall(r"<li>(.*?)</li>", facts.group(1), re.DOTALL)
        # Fact 4 (temporal, carried by position) is checked below, in the outro.
        check(f"[{lang}] the first three facts are stated", len(items) == 3, str(len(items)))
        joined = " ".join(items)
        check(f"[{lang}] the populated register is named in prose",
              f"<code>{bs.EXTENDS_FIGURE['populated']}</code>" in joined)
        check(f"[{lang}] the empty register is named in prose",
              f"<code>{bs.EXTENDS_FIGURE['empty']}</code>" in joined)

        outro = re.search(r"<p>(.*?)</p>\s*</section>", section, re.DOTALL)
        check(f"[{lang}] the outro states the fourth fact after the table it is about",
              bool(outro) and re.search(r"comput|calcul", outro.group(1), re.IGNORECASE))


# --- AC-10 -----------------------------------------------------------------


def test_ac10_no_count_that_rots() -> None:
    print("AC-10 no count of registers, modules or directives is hard-written into the copy")
    keys = ("ext_title", "ext_claim", "ext_col_declares", "ext_col_register", "ext_col_contributes",
            "ext_no_contribution", "ext_fact1", "ext_fact2_a", "ext_fact2_b", "ext_fact3_a", "ext_fact3_b",
            "ext_ask", "th_ext_directive", "th_ext_says", "th_ext_module", "ext_outro")
    for lang in ("en", "fr"):
        strings = json.loads((REPO / "site" / "i18n" / lang / "index.json").read_text(encoding="utf-8"))
        digits = {k: strings[k] for k in keys if k in strings and re.search(r"\d", strings[k])}
        check(f"[{lang}] no #extends copy string carries a digit", not digits, str(digits))
    check("the template writes no literal digit next to the figure's own classes",
          not re.search(r"\bext-(?:row|contributes|register)[^>]*>\s*\d", extends_section("en")))


def test_composition_shape_precedence() -> None:
    print("the composition is read in the shape order modular-composition's tech.md fixes")
    modules = {"tibs245/scrumia:scrumia-specs": {}, "local:acme-rules": {}}
    check("a modules: mapping resolves to the module half of each key",
          bs.declared_modules({"modules": modules}) == ["scrumia-specs", "acme-rules"],
          str(bs.declared_modules({"modules": modules})))
    check("modules: wins over a retired extends: left beside it",
          bs.declared_modules({"modules": modules, "extends": ["stale"]})
          == ["scrumia-specs", "acme-rules"])
    check("extends: is still read when it is the only shape present",
          bs.declared_modules({"extends": ["scrumia-specs"]}) == ["scrumia-specs"])
    # An empty answer is what would render a figure that is quietly no longer true.
    check("a composition declaring neither resolves to nothing",
          bs.declared_modules({"project": {}}) == [])
    check("modules: written with nothing under it resolves to nothing",
          bs.declared_modules({"modules": None}) == [])


def main() -> int:
    for test in (test_ac1_mechanism_not_a_bare_claim, test_ac2_every_name_is_real,
                 test_ac3_empty_register_is_named_not_omitted, test_ac4_reaches_reference_and_slots,
                 test_ac5_legible_with_no_script, test_ac6_tokens_only,
                 test_ac7_turns_rather_than_scrolls, test_ac8_figure_is_not_the_only_carrier,
                 test_ac10_no_count_that_rots, test_composition_shape_precedence):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
