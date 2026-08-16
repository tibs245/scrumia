# Element obsolete to avoid

*Refusal.* A deprecated HTML element when the replacement is well-known. Each row names the obsolete element, what it used to do, and what to write today. The replacement column is the project's instruction, not a description — read it as a directive.

## When to reach for this file

This file is **not** part of the implementation pass. The implementation reference is `element-catalog.md` — every element MDN ships today lives there. The obsolete table exists for one reason: when a reviewer reads a diff and meets a tag that is **not** in `element-catalog.md`, they check this file before raising a finding. If the tag is here, the finding names the replacement; if the tag is in neither file, the finding is something else entirely (a typo, an experimental element, an in-flight draft).

The split keeps implementation reading short — the catalog is the only file an implementer needs open — and review reading surgical — the obsolete file is what a reviewer opens only when the diff has a tag the catalog does not name.

## How to read the table

- **Element** — the obsolete tag.
- **What it was** — the role the element used to play.
- **Replace with** — the directive: the modern element, the CSS property, or "no replacement" when the element is simply gone.

## The obsolete table

| Element | What it was | Replace with |
|---|---|---|
| `acronym` | Old acronym element. | `<abbr>` |
| `big` | Larger text. | CSS `font-size` |
| `center` | Horizontal centering of block content. | CSS `margin` / `text-align` |
| `content` | Old Shadow-DOM insertion point. | `<slot>` |
| `dir` | Directory listing. | `<ul>` |
| `font` | Font size, colour, face. | CSS `font-size`, `color`, `font-family` |
| `frame` | A sub-frame inside a `<frameset>`. | `<iframe>` |
| `frameset` | A set of `<frame>` elements. | `<iframe>` (or a normal page) |
| `image` | Predecessor of `<img>`. | `<img>` |
| `marquee` | Scrolling text. | CSS animation, or remove the effect |
| `menuitem` | A menu command. | `<button>` inside `<menu>` |
| `nobr` | Prevents line wrapping. | CSS `white-space: nowrap` |
| `noembed` | Fallback for browsers without `<embed>`. | No replacement — `<embed>` is supported everywhere now |
| `noframes` | Fallback for browsers without `<frame>`. | No replacement — `<frame>` is gone |
| `param` | Parameters for `<object>`. | No replacement — `<object>` no longer takes parameters this way |
| `plaintext` | Raw text without HTML interpretation. | `<pre><code>` with a `Content-Type` set on the response, or escape the markup |
| `rb` | Old ruby base element. | The bare text node inside `<ruby>` |
| `rtc` | Old ruby annotation container. | `<rt>` directly inside `<ruby>` |
| `shadow` | Old Shadow-DOM insertion point. | `<slot>` |
| `strike` | Strikethrough text. | `<s>` for non-relevant content, `<del>` for deleted content |
| `tt` | Monospace text. | CSS `font-family: monospace`, or `<code>` |
| `xmp` | Uninterpreted monospace text. | `<pre><code>` |

## What to do when a diff contains one of these

1. Name the obsolete element.
2. Cite the row above as the rule source.
3. Cite the replacement column as the directive.
4. If the obsolete element was inside a third-party snippet or vendored library that the project does not control, mark the finding `out of scope — third-party` and stop. The directive applies to code the project owns.

## What this file is not

- It is not an exhaustive list of every retired HTML tag the W3C has ever shipped. It is the subset MDN still surfaces as deprecated and a covered app is likely to encounter. Vendor-specific retired elements (Netscape `<blink>`, `<multicol>`, `<spacer>`) are not in scope — they were never in the HTML spec.
- It is not a discussion of *why* each element was retired. The replacement column is a directive, not an essay; the linked MDN page carries the long form when a reviewer needs it.
- It is **not** a license to keep an obsolete element with a comment explaining why. The replacement is the answer; a comment is, at best, a comment on a finding.

## Sources

`https://developer.mozilla.org/fr/docs/Web/HTML/Reference/Elements` — MDN Web Docs, *Reference of HTML elements*. CC BY-SA 4.0. The "obsolete" grouping and the W3C-recognised replacements are MDN's; the directive column is the project's transcription — a row in this table is a finding, not a description.
