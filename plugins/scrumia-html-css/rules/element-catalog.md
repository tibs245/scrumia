# Element catalog

*Refusal.* A deprecated element when a current one carries the same intent; a generic `<div>` or `<span>` when a semantic element names what the content is. The catalog below is the project-wide reference: every HTML element MDN recognises, what it is for, and — when the element is deprecated — what to write instead.

## How to read the table

- **Element** — the tag name.
- **Category** — MDN's grouping (root, metadata, sectioning, text content, phrasing, embedded, scripting, tabular, forms, interactive, web components).
- **Recommended use** — when to reach for it. A element that is "current" is one MDN ships today and recommends; reach for it as the default.
- **Status** — `Current`, or `Deprecated — replaced by <X>` when an element is obsolete. The replacement is what MDN names today.

## The catalog

| Element | Category | Recommended use | Status |
|---|---|---|---|
| `html` | Root | The root element of an HTML document. All other elements descend from it. | Current |
| `base` | Document metadata | The base URL used to resolve every relative URL in the document. One per document. | Current |
| `head` | Document metadata | Machine-readable metadata about the document: title, scripts, styles, links. | Current |
| `link` | Document metadata | A relationship to an external resource (CSS, favicon, alternate forms). | Current |
| `meta` | Document metadata | Metadata that no other meta element can express (charset, viewport, OpenGraph, robots). | Current |
| `style` | Document metadata | CSS the document itself carries. | Current |
| `title` | Document metadata | The document's title (browser tab, bookmark, search result). | Current |
| `body` | Sectioning root | The document's main content. One per document. | Current |
| `address` | Content sectioning | Contact information for a person or organisation. | Current |
| `article` | Content sectioning | A self-contained composition that could be distributed independently (post, product card, comment). | Current |
| `aside` | Content sectioning | Content tangentially related to the main content (sidebars, callouts, related links). | Current |
| `footer` | Content sectioning | The footer of a section or of the document (author, copyright, related links). | Current |
| `header` | Content sectioning | Introductory content (titles, logo, search, author name). | Current |
| `h1`–`h6` | Content sectioning | The six levels of section heading. | Current |
| `hgroup` | Content sectioning | A title grouped with subtitle-level headings (the W3C HTML spec currently lists this as withdrawn-from-spec; MDN keeps it as a transitional element). | Current |
| `main` | Content sectioning | The dominant content of the document body. One per document. | Current |
| `nav` | Content sectioning | A section of navigation links (menus, tables of contents, breadcrumbs). | Current |
| `section` | Content sectioning | A standalone section with its own heading. Reach for it over a bare `<div>` whenever the region has a name that is a heading. | Current |
| `search` | Content sectioning | A region containing search or filtering controls. | Current |
| `blockquote` | Text content | A long quotation, indented by default. | Current |
| `dd` | Text content | The description of a term in a description list (`<dl>`). | Current |
| `div` | Text content | A generic flow-content container with no semantics. Use only when no semantic element fits — see `element-follows-purpose`. | Current |
| `dl` | Text content | A description list: groups of term/definition pairs. | Current |
| `dt` | Text content | A term being defined in a description list (`<dl>`). | Current |
| `figcaption` | Text content | A caption for the parent `<figure>`. | Current |
| `figure` | Text content | Self-contained content with an optional caption (image, code listing, diagram). | Current |
| `hr` | Text content | A thematic break between paragraphs. | Current |
| `li` | Text content | A list item — child of `<ol>`, `<ul>`, or `<menu>`. | Current |
| `menu` | Text content | A semantic alternative to `<ul>` for an unordered list of commands. | Current |
| `ol` | Text content | An ordered (numbered) list. | Current |
| `p` | Text content | A paragraph. | Current |
| `pre` | Text content | Preformatted text in a monospace font. | Current |
| `ul` | Text content | An unordered (bulleted) list. | Current |
| `a` | Inline text | A hyperlink (with `href`). For navigation, not for in-page actions — those are `<button>`. | Current |
| `abbr` | Inline text | An abbreviation or acronym. | Current |
| `b` | Inline text | Text set apart stylistically without extra importance (bold). | Current |
| `bdi` | Inline text | Text isolated from the surrounding bidirectional algorithm. | Current |
| `bdo` | Inline text | Text whose bidirectional direction is overridden. | Current |
| `br` | Inline text | A line break — only when the line break is part of the content (a poem, an address). Never for layout. | Current |
| `cite` | Inline text | The title of a cited creative work. | Current |
| `code` | Inline text | A fragment of code in a monospace font. | Current |
| `data` | Inline text | Content bound to a machine-readable value (via `value`). | Current |
| `dfn` | Inline text | A term being defined in its surrounding context. | Current |
| `em` | Inline text | Stressed emphasis (a different *pronunciation*). | Current |
| `i` | Inline text | Text set apart for a distinct reason — technical terms, foreign phrases, taxonomic names. | Current |
| `kbd` | Inline text | User input — keyboard, voice, or other input. | Current |
| `mark` | Inline text | Text marked for reference or relevance. | Current |
| `q` | Inline text | A short inline quotation. | Current |
| `rp` | Inline text | Fallback parentheses for browsers without ruby annotation support. | Current |
| `rt` | Inline text | A ruby annotation — pronunciation, translation. | Current |
| `ruby` | Inline text | A ruby annotation for East-Asian typography. | Current |
| `s` | Inline text | Text that is no longer accurate or relevant (strikethrough). | Current |
| `samp` | Inline text | Sample output from a program. | Current |
| `small` | Inline text | Side comments, legal fine print — text that is small *by relevance*, not always by rendering. | Current |
| `span` | Inline text | A generic inline container with no semantics. Use only when no semantic element fits. | Current |
| `strong` | Inline text | Strong importance (bold). | Current |
| `sub` | Inline text | Subscript text. | Current |
| `sup` | Inline text | Superscript text. | Current |
| `time` | Inline text | A specific time period (with a `datetime` attribute for machine reading). | Current |
| `u` | Inline text | Text annotated non-textually — proper names in Chinese, misspellings flagged in review. | Current |
| `var` | Inline text | A variable name — mathematical or programmatic. | Current |
| `wbr` | Inline text | A word-break opportunity — a place a line may break if needed. | Current |
| `area` | Image and multimedia | A clickable region inside an image map (`<map>`). | Current |
| `audio` | Image and multimedia | Embedded sound content. | Current |
| `img` | Image and multimedia | An image. The `alt` attribute is mandatory and carries the accessible name. | Current |
| `map` | Image and multimedia | An image map — paired with one or more `<area>` elements. | Current |
| `track` | Image and multimedia | A timed text track (subtitles, captions) for `<audio>` or `<video>`. | Current |
| `video` | Image and multimedia | An embedded video player. | Current |
| `embed` | Embedded content | An external content plug-in or application. | Current |
| `fencedframe` | Embedded content | A nested browsing context with stronger privacy guarantees. | Current |
| `iframe` | Embedded content | A nested browsing context (a page inside a page). | Current |
| `object` | Embedded content | An external resource — image, iframe, plug-in. | Current |
| `picture` | Embedded content | A container of `<source>` and one `<img>` for responsive image sources. | Current |
| `source` | Embedded content | One of several media resources for `<picture>`, `<audio>`, or `<video>`. | Current |
| `svg` | SVG and MathML | The root container for inline SVG content. | Current |
| `math` | SVG and MathML | The root element for MathML. | Current |
| `canvas` | Scripts | A drawing surface for the Canvas/WebGL APIs. | Current |
| `noscript` | Scripts | Fallback content for browsers without script support. | Current |
| `script` | Scripts | Executable code (usually JavaScript) or data. | Current |
| `del` | Edits | Text deleted from the document. | Current |
| `ins` | Edits | Text inserted into the document. | Current |
| `caption` | Tabular data | A title or caption for a `<table>`. | Current |
| `col` | Tabular data | One or more columns inside a `<colgroup>`. | Current |
| `colgroup` | Tabular data | A group of columns inside a `<table>`. | Current |
| `table` | Tabular data | Tabular data — rows of cells in columns. Not for layout. | Current |
| `tbody` | Tabular data | The body of a `<table>` — the rows of data. | Current |
| `td` | Tabular data | A data cell in a `<table>` row. | Current |
| `tfoot` | Tabular data | The footer rows of a `<table>`. | Current |
| `th` | Tabular data | A header cell in a `<table>`. | Current |
| `thead` | Tabular data | The header rows of a `<table>`. | Current |
| `tr` | Tabular data | A row of cells in a `<table>`. | Current |
| `button` | Forms | An interactive button. Carries keyboard activation and focus natively. | Current |
| `datalist` | Forms | Suggested values for another form control (autocomplete-style). | Current |
| `fieldset` | Forms | A group of form controls with their shared `<legend>`. | Current |
| `form` | Forms | A section of interactive controls that can be submitted. | Current |
| `input` | Forms | A form control — text, checkbox, radio, range, file, etc., depending on `type`. | Current |
| `label` | Forms | A caption for a form control; click target expands to the control. | Current |
| `legend` | Forms | A caption for a `<fieldset>`. | Current |
| `meter` | Forms | A scalar value inside a known range — gauge-style. | Current |
| `optgroup` | Forms | A group of `<option>` inside a `<select>`. | Current |
| `option` | Forms | One option inside `<select>`, `<optgroup>`, or `<datalist>`. | Current |
| `output` | Forms | The result of a calculation or user action. | Current |
| `progress` | Forms | A completion progress indicator. | Current |
| `select` | Forms | A drop-down menu of `<option>` elements. | Current |
| `selectedcontent` | Forms | The displayed content of the currently selected `<option>` inside a closed `<select>`. | Current |
| `textarea` | Forms | A multi-line plain-text editor. | Current |
| `details` | Interactive elements | A disclosure widget — collapsed or expanded content with a `<summary>`. | Current |
| `dialog` | Interactive elements | A dialog box or modal. | Current |
| `summary` | Interactive elements | The caption of a `<details>` element; the disclosure handle. | Current |
| `geolocation` | Interactive elements | A control that shares the user's geolocation when activated. | Current |
| `slot` | Web Components | A placeholder inside a Web Component's shadow tree, filled by the consumer. | Current |
| `template` | Web Components | Inert HTML held for later instantiation by JavaScript. | Current |
| `acronym` | Obsolete | Old acronym element. | Deprecated — replaced by `abbr` |
| `big` | Obsolete | Larger text. | Deprecated — replaced by CSS `font-size` |
| `center` | Obsolete | Horizontal centering of block content. | Deprecated — replaced by CSS |
| `content` | Obsolete | Old Shadow-DOM insertion point. | Deprecated — replaced by `slot` |
| `dir` | Obsolete | Directory listing. | Deprecated — replaced by `ul` |
| `font` | Obsolete | Font size, colour, face. | Deprecated — replaced by CSS |
| `frame` | Obsolete | A sub-frame inside a `<frameset>`. | Deprecated — replaced by `iframe` |
| `frameset` | Obsolete | A set of `<frame>` elements. | Deprecated — replaced by `iframe` |
| `image` | Obsolete | Predecessor of `<img>`. | Deprecated — replaced by `img` |
| `marquee` | Obsolete | Scrolling text. | Deprecated — non-standard, use CSS animation |
| `menuitem` | Obsolete | A menu command. | Deprecated — replaced by `<button>` inside `<menu>` |
| `nobr` | Obsolete | Prevents line wrapping. | Deprecated — replaced by CSS `white-space` |
| `noembed` | Obsolete | Fallback for browsers without `<embed>`. | Deprecated |
| `noframes` | Obsolete | Fallback for browsers without `<frame>`. | Deprecated |
| `param` | Obsolete | Parameters for `<object>`. | Deprecated |
| `plaintext` | Obsolete | Raw text without HTML interpretation. | Deprecated |
| `rb` | Obsolete | Old ruby base element. | Deprecated — replaced by direct `<ruby>` children |
| `rtc` | Obsolete | Old ruby annotation container. | Deprecated — replaced by `<rt>` |
| `shadow` | Obsolete | Old Shadow-DOM insertion point. | Deprecated — replaced by `slot` |
| `strike` | Obsolete | Strikethrough text. | Deprecated — replaced by `s` or `del` |
| `tt` | Obsolete | Monospace text. | Deprecated — replaced by CSS `font-family: monospace` |
| `xmp` | Obsolete | Uninterpreted monospace text. | Deprecated — replaced by `<pre><code>` |

## What this catalog is not

- It is not a permission slip for every element in the *Current* column. Some current elements — `<div>`, `<span>`, `<i>`, `<b>` — are intentional last-resort carriers that `element-follows-purpose` still refuses in favour of a more semantic alternative when one fits.
- It is not exhaustive of every HTML feature MDN ships — form-validation pseudo-classes, ARIA roles, microdata — all live outside the element table by design.
- It is not a substitute for reading the linked MDN page when an element's behaviour matters. The table is the project's *single-page reference*; the MDN page is the long form.

## Sources complémentaires

`https://developer.mozilla.org/fr/docs/Web/HTML/Reference/Elements` — MDN Web Docs, *Référence des éléments HTML*. CC BY-SA 4.0. The element grouping, current/obsolete distinction, and replacement recommendations are MDN's; the prose in the *Recommended use* column is this project's transcription, with the bias a project owns: reach for the semantic element, refuse the generic when an intent is named.
