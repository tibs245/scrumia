#!/usr/bin/env python3
"""Build the bilingual static site from one template per page + one string file per language.

    site/templates/<page>.html      the structure, written once
    site/templates/partials/*.html  shared chrome ({{>head}}, {{>header}}, {{>footer}})
    site/i18n/<lang>/common.json    chrome strings (nav, footer, theme)
    site/i18n/<lang>/<page>.json    page strings
    design/tokens.css               the design vocabulary, mirrored into site/assets/

One module page per marketplace plugin is generated on top of that:

    .claude-plugin/marketplace.json     the enumerator and the fact source
    plugins/<name>/skills/*/SKILL.md    the skill list, same
    site/modules.json                   the language-neutral facts the manifest has no field for
    site/templates/module.html          the structure, written once for all of them
    site/i18n/<lang>/modules/<name>.json  the prose, one file per module per language

Output: site/<page>.html (en), site/fr/<page>.html (fr), site/modules/<name>.html,
site/fr/modules/<name>.html, site/assets/tokens.css, plus sitemap.xml.
A key missing in any language, or a page-level key no template reads, fails the build —
that is the anti-divergence guard, both directions.

Run from anywhere: python3 tools/build_site.py
Adding a language = add site/i18n/<lang>/ and one entry to LANGS below.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
TPL = SITE / "templates"
I18N = SITE / "i18n"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
MODULES_DATA = SITE / "modules.json"
PLUGINS_DIR = ROOT / "plugins"
SCRUMIA_CONFIG = ROOT / ".scrumia" / "config.yaml"
TOKENS_SRC = ROOT / "design" / "tokens.css"
TOKENS_OUT = SITE / "assets" / "tokens.css"
REPO_URL = "https://github.com/tibs245/scrumia"
SITE_URL = "https://tibs245.github.io/scrumia/"
PAGES = ["index", "workflow", "reference", "about"]
# The two registers #extends draws (#296) — named rather than auto-picked, re-checked
# against the live composition by extends_map_specials on every build.
EXTENDS_FIGURE = {"populated": "implement", "empty": "sprint"}
LANGS = {
    "en": {"out": SITE, "prefix": "", "root": ""},
    "fr": {"out": SITE / "fr", "prefix": "fr/", "root": "../"},
}

TOKEN = re.compile(r"\{\{([@>]?[A-Za-z0-9_.-]+)\}\}")
ERRORS: list[str] = []


def url_for(lang: str, page: str) -> str:
    base = SITE_URL + LANGS[lang]["prefix"]
    return base if page == "index" else base + page + ".html"


def specials(lang: str, page: str) -> dict[str, str]:
    # `page` is a path relative to the language root, so a nested page has to
    # climb back out of its directory before any relative link resolves.
    up = "../" * page.count("/")
    leaf = page.rsplit("/", 1)[-1]
    sp = {
        "@lang": lang,
        "@root": up + LANGS[lang]["root"],
        "@lroot": up,
        "@canonical": url_for(lang, page),
        "@url_en": url_for("en", page),
        "@url_fr": url_for("fr", page),
        "@to_en": (leaf + ".html") if lang == "en" else up + "../" + page + ".html",
        "@to_fr": (up + "fr/" + page + ".html") if lang == "en" else leaf + ".html",
        "@en_current": ' aria-current="true"' if lang == "en" else "",
        "@fr_current": ' aria-current="true"' if lang == "fr" else "",
    }
    for p in PAGES:
        sp["@cur_" + p] = ' aria-current="page"' if p == page else ""
    return sp


def load_strings(lang: str, page: str) -> dict[str, str]:
    strings: dict[str, str] = {}
    for name in ("common", page):
        path = I18N / lang / f"{name}.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            ERRORS.append(f"{path.relative_to(ROOT)}: missing")
            continue
        except json.JSONDecodeError as e:
            ERRORS.append(f"{path.relative_to(ROOT)}: invalid JSON — {e}")
            continue
        overlap = strings.keys() & data.keys()
        if overlap:
            ERRORS.append(f"{path.relative_to(ROOT)}: keys already in common.json: {sorted(overlap)}")
        strings.update(data)
    return strings


def render(template: str, strings: dict[str, str], sp: dict[str, str], origin: str, used: set[str]) -> str:
    def include(match: re.Match) -> str:
        name = match.group(1)
        path = TPL / "partials" / f"{name}.html"
        if not path.exists():
            ERRORS.append(f"{origin}: unknown partial {{{{>{name}}}}}")
            return ""
        return path.read_text(encoding="utf-8").rstrip("\n")

    # Partials first (one level is all we use), then tokens.
    template = re.sub(r"\{\{>([A-Za-z0-9_-]+)\}\}", include, template)

    def substitute(match: re.Match) -> str:
        key = match.group(1)
        if key.startswith("@"):
            if key not in sp:
                ERRORS.append(f"{origin}: unknown special {{{{{key}}}}}")
                return ""
            return sp[key]
        if key not in strings:
            ERRORS.append(f"{origin}: missing string '{key}'")
            return ""
        used.add(key)
        value = strings[key]
        # Non-string values (e.g. an object injected into a <script>) render as JSON.
        return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)

    return TOKEN.sub(substitute, template)


def skill_names(plugin: str) -> list[str]:
    return sorted(p.parent.name for p in (ROOT / "plugins" / plugin).glob("skills/*/SKILL.md"))


def load_modules() -> list[dict]:
    """Enumerate the marketplace's plugins and attach the facts a page needs.

    The manifest is the enumerator: a plugin absent from it has no page, and a
    page has no fact the manifest doesn't carry — except the two the schema has
    no field for, which site/modules.json owns alone.
    """
    try:
        market = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        ERRORS.append(f"{MARKETPLACE.relative_to(ROOT)}: unreadable — {e}")
        return []
    try:
        extra = json.loads(MODULES_DATA.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        ERRORS.append(f"{MODULES_DATA.relative_to(ROOT)}: unreadable — {e}")
        return []

    # JSON has no comments: an underscore key is how the file documents itself.
    extra = {k: v for k, v in extra.items() if not k.startswith("_")}
    entries = [p for p in market.get("plugins", []) if p.get("name")]
    named = {p["name"] for p in entries}
    rel = MODULES_DATA.relative_to(ROOT)
    for name in sorted(named - extra.keys()):
        ERRORS.append(f"{rel}: no entry for plugin '{name}'")
    for name in sorted(extra.keys() - named):
        ERRORS.append(f"{rel}: entry '{name}' is not a plugin of the marketplace")

    seen: dict[str, str] = {}
    modules = []
    for entry in entries:
        name = entry["name"]
        data = extra.get(name)
        if not isinstance(data, dict):
            if name in extra:
                ERRORS.append(f"{rel}: '{name}' is not an object")
            continue
        emoji = data.get("emoji")
        if not emoji:
            ERRORS.append(f"{rel}: '{name}' declares no emoji")
        elif emoji in seen:
            ERRORS.append(f"{rel}: '{name}' reuses the emoji of '{seen[emoji]}'")
        else:
            seen[emoji] = name
        skills = skill_names(name)
        if not skills:
            ERRORS.append(f"plugins/{name}: no skills/*/SKILL.md to list")
        modules.append({
            "name": name,
            "emoji": emoji or "",
            "slot": data.get("slot") or "",
            "version": entry.get("version", ""),
            "tags": entry.get("tags", []),
            "skills": skills,
        })
    return modules


def module_specials(module: dict, labels: dict[str, str]) -> dict[str, str]:
    """Manifest facts, injected as specials so no page can restate them by hand.

    Every fact here comes from marketplace.json or the skills tree — authored in
    this repo and gated by tools/validate.py today, but escaped anyway (#71):
    a fact heading into markup or an href attribute stays escaped the day the
    marketplace takes an outside contribution, instead of becoming a hole then.

    An empty slot is a stated fact, not a blank — and the only one of these that
    needs a word rather than a slug, hence the chrome string.
    """
    name = html.escape(module["name"])
    if module["slot"]:
        slot = f"<code>{html.escape(module['slot'])}</code>"
    else:
        slot = labels.get("mod_no_slot", "")
        if "mod_no_slot" not in labels:
            ERRORS.append(f"common.json: 'mod_no_slot' is needed by '{module['name']}', which fills none")
    return {
        "@mod_name": name,
        "@mod_emoji": html.escape(module["emoji"]),
        "@mod_slot": slot,
        "@mod_version": html.escape(module["version"]),
        "@mod_tags": " ".join(f"<li>{html.escape(t)}</li>" for t in module["tags"]),
        "@mod_skills": "".join(f"<li><code>{html.escape(s)}</code></li>" for s in module["skills"]),
        "@mod_install": f"/plugin install {name}@scrumia",
        "@mod_source": f"{REPO_URL}/tree/main/plugins/{name}",
    }


def module_link_specials(modules: list[dict]) -> dict[str, str]:
    """One `@modlink_<name>` per module — the URL a card links to, computed once
    per module name rather than hand-typed per card in the template (#70)."""
    return {f"@modlink_{m['name']}": f"modules/{m['name']}.html" for m in modules}


def load_project_modules() -> list[str]:
    """The modules this project runs, read from `.scrumia/config.yaml`'s `extends:`
    list — the same source `scrumia-extends` reads, so the figure never names a
    module this composition does not actually run."""
    try:
        import yaml
    except ImportError:
        ERRORS.append("PyYAML not installed — cannot read .scrumia/config.yaml for the extends map")
        return []
    try:
        cfg = yaml.safe_load(SCRUMIA_CONFIG.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        ERRORS.append(f"{SCRUMIA_CONFIG.relative_to(ROOT)}: missing")
        return []
    except yaml.YAMLError as e:
        ERRORS.append(f"{SCRUMIA_CONFIG.relative_to(ROOT)}: invalid YAML — {e}")
        return []
    return list(cfg.get("extends") or [])


def read_json_object(path: Path) -> dict:
    """A module's own `registers.json` or `extends.json`. Malformed is reported, not
    read as empty — a typo in an extension must not ship as a silent "contributes
    nothing" (mirrors `scrumia-extends`' own `read_json`)."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        ERRORS.append(f"{path.relative_to(ROOT)}: invalid JSON — {e}")
        return {}
    if not isinstance(data, dict):
        ERRORS.append(f"{path.relative_to(ROOT)}: not a JSON object")
        return {}
    return data


def load_extends_map() -> dict:
    """The registers this project's own modules open and extend, walked directly
    from `plugins/*/registers.json` and `extends.json` rather than shelled out to
    `scrumia-extends`: a build has no guarantee of a PATH carrying every module's
    `bin/`, which is a harness feature (ADR-0018), not a build-time one."""
    registers: dict[str, dict] = {}
    directives: dict[str, list[dict]] = {}
    for name in load_project_modules():
        root = PLUGINS_DIR / name
        for reg, info in read_json_object(root / "registers.json").items():
            registers[reg] = {"module": name, "skill": info.get("skill", "")}
        for reg, rows in read_json_object(root / "extends.json").items():
            if not isinstance(rows, list):
                ERRORS.append(f"plugins/{name}/extends.json: '{reg}' is not a list of directives")
                continue
            for row in rows:
                if not isinstance(row, dict):
                    ERRORS.append(f"plugins/{name}/extends.json: a '{reg}' entry is not an object")
                    continue
                directives.setdefault(reg, []).append({
                    "module": name,
                    "name": row.get("name", "(unnamed)"),
                    "summary": row.get("summary", ""),
                })
    return {"registers": registers, "directives": directives}


def extends_map_specials() -> dict[str, str]:
    """The `#extends` section's figure and table (#296): one populated register, one
    empty one. Both are re-verified against the live composition on every build —
    AC-2 (nothing invented) and AC-3 (the empty case is genuine) are guarded by the
    same check that produces the copy, so a composition drift fails the build
    instead of shipping a figure that is quietly no longer true."""
    data = load_extends_map()
    regs, dirs = data["registers"], data["directives"]

    def pick(reg: str, want_empty: bool):
        if reg not in regs:
            ERRORS.append(f"extends-map: register '{reg}' is opened by no module this project runs")
            return None
        contributors = dirs.get(reg, [])
        mods = sorted({d["module"] for d in contributors})
        if want_empty and mods:
            ERRORS.append(
                f"extends-map: '{reg}' was picked as the empty-register example but is now "
                f"extended by {mods} — pick a register that still carries no contribution")
            return None
        if not want_empty and len(mods) < 2:
            ERRORS.append(
                f"extends-map: '{reg}' was picked as the populated example but only {mods} "
                "extend it — pick a register more than one module contributes to")
            return None
        return {"module": regs[reg]["module"], "skill": regs[reg]["skill"],
                "contributors": contributors, "mods": mods}

    populated = pick(EXTENDS_FIGURE["populated"], want_empty=False)
    empty = pick(EXTENDS_FIGURE["empty"], want_empty=True)
    if populated is None or empty is None:
        return {}

    rows = sorted(populated["contributors"], key=lambda d: (d["module"], d["name"]))
    # A comma list, not "and"-joined: the prose that reads it runs in English and
    # French from the same special, and only one of them spells the conjunction "and".
    inline_mods = ", ".join(f"<code>{html.escape(m)}</code>" for m in populated["mods"])
    return {
        "@ext_full_register": EXTENDS_FIGURE["populated"],
        "@ext_full_module": populated["module"],
        "@ext_full_skill": populated["skill"],
        "@ext_full_contributors": "".join(f"<li>{html.escape(m)}</li>" for m in populated["mods"]),
        "@ext_full_contributors_inline": inline_mods,
        "@ext_empty_register": EXTENDS_FIGURE["empty"],
        "@ext_empty_module": empty["module"],
        "@ext_empty_skill": empty["skill"],
        "@ext_directive_rows": "".join(
            f"<tr><td><code>{html.escape(r['name'])}</code></td><td>{html.escape(r['summary'])}</td>"
            f"<td><code>{html.escape(r['module'])}</code></td></tr>" for r in rows),
    }


def load_common(lang: str) -> dict[str, str]:
    """Chrome strings, read outside the render path; load_strings reports a broken file."""
    try:
        return json.loads((I18N / lang / "common.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def check_orphan_prose(names: set[str]) -> None:
    """An i18n module file naming no plugin is a page nobody can reach."""
    for lang in LANGS:
        for path in sorted((I18N / lang / "modules").glob("*.json")):
            if path.stem not in names:
                ERRORS.append(f"{path.relative_to(ROOT)}: names no plugin of the marketplace")


def render_page(lang: str, cfg: dict, page: str, tpl_path: Path, extra: dict[str, str] | None = None) -> None:
    if not tpl_path.exists():
        ERRORS.append(f"{tpl_path.relative_to(ROOT)}: missing template")
        return
    strings = load_strings(lang, page)
    used: set[str] = set()
    origin = f"{page}.html [{lang}]"
    sp = specials(lang, page)
    sp.update(extra or {})
    html = render(tpl_path.read_text(encoding="utf-8"), strings, sp, origin, used)
    if "{{" in html:
        ERRORS.append(f"{origin}: unresolved '{{{{' left in output")
    page_json = I18N / lang / f"{page}.json"
    # Chrome keys are shared: only check unused-ness on page-level keys. A malformed
    # file is already reported by load_strings above — this reparse must not raise.
    try:
        page_keys = set(json.loads(page_json.read_text(encoding="utf-8")).keys()) if page_json.exists() else set()
    except json.JSONDecodeError:
        page_keys = set()
    for key in sorted({k for k in strings if k not in used} & page_keys):
        ERRORS.append(f"{origin}: unused string '{key}'")
    out = cfg["out"] / f"{page}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def copy_tokens() -> None:
    """Mirror the design tokens into the published tree.

    Pages serves site/ alone, so a stylesheet there cannot @import design/. The
    copy is committed and the header says where it came from — one vocabulary,
    two locations, and the generated one is never the file you edit.
    """
    try:
        source = TOKENS_SRC.read_text(encoding="utf-8")
    except FileNotFoundError:
        ERRORS.append(f"{TOKENS_SRC.relative_to(ROOT)}: missing — the design contract names it")
        return
    header = f"/* GENERATED by tools/build_site.py from {TOKENS_SRC.relative_to(ROOT)} — do not edit. */\n"
    TOKENS_OUT.write_text(header + source, encoding="utf-8")


def build() -> int:
    copy_tokens()
    modules = load_modules()
    check_orphan_prose({m["name"] for m in modules})
    emoji_specials = {f"@emoji_{m['name']}": m["emoji"] for m in modules}
    link_specials = module_link_specials(modules)
    extends_specials = extends_map_specials()
    module_pages = [f"modules/{m['name']}" for m in modules]

    for lang, cfg in LANGS.items():
        cfg["out"].mkdir(parents=True, exist_ok=True)
        labels = load_common(lang)
        for page in PAGES:
            # extends_specials feeds #extends alone; harmless to carry on other
            # pages since a special only surfaces where a template references it.
            extra = {**emoji_specials, **link_specials, **(extends_specials if page == "index" else {})}
            render_page(lang, cfg, page, TPL / f"{page}.html", extra)
        for module in modules:
            render_page(lang, cfg, f"modules/{module['name']}", TPL / "module.html",
                        module_specials(module, labels))

    urls = [url_for(lang, page) for page in PAGES + module_pages for lang in LANGS]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sitemap.append(f"  <url><loc>{u}</loc></url>")
    sitemap.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

    if ERRORS:
        for e in ERRORS:
            print(f"error: {e}")
        print(f"\nbuild failed: {len(ERRORS)} error(s)")
        return 1
    pages = (len(PAGES) + len(modules)) * len(LANGS)
    print(f"built {pages} pages ({len(modules) * len(LANGS)} module pages) "
          f"+ sitemap.xml + assets/tokens.css")
    return 0


if __name__ == "__main__":
    sys.exit(build())
