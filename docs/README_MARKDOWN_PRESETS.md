# 🎁 `markdown/presets` — Names for the Things You Write Often

The `presets` package holds no logic of its own — every entry here is either a pre-built
node (`RULE`, `HARD_BREAK`) or a small factory function returning one (`H1(inner)`,
`BOLD(inner)`, `NOTE(*blocks)`), built directly on top of the nodes in `inline/`, `blocks/`
and `containers/`. The result is a document that reads like the Markdown it produces.
Grouped by module below; each section is the group's full list, signatures and examples.

```python
from simplibs.markdown.presets import H1, NOTE, BULLET_LIST, BOLD, RULE

doc = H1("Project") + NOTE("Back up your data first.") + BULLET_LIST("one", "two") + RULE
```

```python
def H1(inner: str | Markdown, style: HeadingStyle = HeadingStyle.ATX) -> Heading:
    return Heading(inner, level=1, style=style)

RULE = ThematicBreak()
```

## A note on scope and naming

Presets can be imported from **`simplibs.markdown`** directly or from **`simplibs.markdown.presets`**.
The root exports them for convenience, while `simplibs.markdown.presets` acts as a dedicated vocabulary,
the same way `rules` and `actions` are in other `simplibs` libraries.

Two conventions, the same as `ANY` and `ONE_OR_MORE` in `simplibs-regex`:

* A preset that **needs arguments** is a **function** with a capitalized name — `BOLD(...)`,
  `H2(...)`, `NOTE(...)`.
* A preset **without arguments** is a **ready instance** — `RULE`, `HARD_BREAK` — used
  *without* parentheses.

A preset only **calls a node**. Every check and every error card comes from that node, so a
preset adds nothing that could fail by itself: `H6("x", HeadingStyle.SETEXT)` raises the
`Heading` error (`MARKDOWN_HEADING_SETEXT_LEVEL`), `BULLET_LIST("a", marker=ListMarker.DOT)` raises the
`List` error (`MARKDOWN_LIST_MARKER_ORDERED_MISMATCH`). That is also why there is almost nothing
to test beyond "the arguments are passed on".

Anything more specific than a preset offers is expected to be composed directly from the
underlying nodes — `Emphasis`, `Link`, `List`, `Table` and the others stay deliberately open,
general mechanisms.

---

## 🧭 Table of Contents

[**alerts**: `NOTE` · `TIP` · `IMPORTANT` · `WARNING` · `CAUTION`](#alerts)

[**code**: `MERMAID` · `GEOJSON` · `TOPOJSON` · `STL` · `MATH_BLOCK`](#code)

[**emphasis**: `BOLD` · `ITALIC` · `BOLD_ITALIC` · `STRIKETHROUGH`](#emphasis)

[**headings**: `H1` · `H2` · `H3` · `H4` · `H5` · `H6`](#headings)

[**html**: `DETAILS` · `SUP` · `SUB` · `MARK` · `KBD` · `COMMENT` · `ANCHOR`](#html)

[**links**: `IMAGE` · `AUTOLINK` · `BARE_URL`](#links)

[**lists**: `BULLET_LIST` · `NUMBERED_LIST` · `TASK_ITEM` · `DONE_ITEM`](#lists)

[**references**: `MENTION` · `ISSUE_REF` · `COMMIT_REF` · `EMOJI` · `COLOR_CHIP`](#references)

[**spacing**: `EMPTY_LINE` · `RULE` · `HARD_BREAK`](#spacing)

[⬅️ Back to main README](../README.md#-presets--names-for-the-things-you-write-often)

---

### `alerts`

Factory functions over [`Quote`](README_MARKDOWN_CONTAINERS.md#quote) with an `alert` kind —
block nodes. Every one takes `*blocks` (strings, nodes or lists of them; several blocks are
separated by a quoted blank line) and may be called with no content at all (only the marker).

| Preset      | Signature    | Renders                  | For                                   |
|-------------|--------------|--------------------------|---------------------------------------|
| `NOTE`      | `(*blocks)`  | `> [!NOTE]` + content    | information worth noticing            |
| `TIP`       | `(*blocks)`  | `> [!TIP]` + content     | helpful advice                        |
| `IMPORTANT` | `(*blocks)`  | `> [!IMPORTANT]` + content | information key to the reader's goal |
| `WARNING`   | `(*blocks)`  | `> [!WARNING]` + content | something that needs attention        |
| `CAUTION`   | `(*blocks)`  | `> [!CAUTION]` + content | a risk or a negative outcome          |

**Example usage:**
```python
NOTE("Back up your data first.")
# > [!NOTE]
# > Back up your data first.

NOTE("First paragraph.", "Second paragraph.")
# > [!NOTE]
# > First paragraph.
# >
# > Second paragraph.
```

> 💡 GitHub shows an alert as a highlighted box. Other renderers show an ordinary quote whose
> first line is `[!NOTE]`.

[▲ Back to top](#-table-of-contents)

---

### `code`

Factory functions over [`CodeBlock`](README_MARKDOWN_BLOCKS.md#codeblock) with the info string
filled in — block nodes. Each takes the content as **one string**. These are the fenced blocks
that GitHub draws as something other than source.

| Preset       | Signature   | Info string | GitHub draws          |
|--------------|-------------|-------------|-----------------------|
| `MERMAID`    | `(code)`    | `mermaid`   | a diagram             |
| `GEOJSON`    | `(code)`    | `geojson`   | an interactive map    |
| `TOPOJSON`   | `(code)`    | `topojson`  | an interactive map    |
| `STL`        | `(code)`    | `stl`       | a rotatable 3D model  |
| `MATH_BLOCK` | `(expr)`    | `math`      | a formula             |

**Example usage:**
```python
MERMAID("graph TD; A-->B")
# ```mermaid
# graph TD; A-->B
# ```

MATH_BLOCK("E = mc^2")
# ```math
# E = mc^2
# ```
```

The text itself is **not** checked — a broken diagram or a wrong GeoJSON is only discovered by
the renderer. A fence of backticks **inside** the code is handled by `CodeBlock` (the fence
becomes longer automatically). For a formula inside a line, use
[`Math`](README_MARKDOWN_INLINE.md#math).

[▲ Back to top](#-table-of-contents)

---

### `emphasis`

Factory functions over [`Emphasis`](README_MARKDOWN_INLINE.md#emphasis) with the kind filled in —
inline nodes, so they join with `+`.

| Preset          | Signature            | Renders        |
|-----------------|----------------------|----------------|
| `ITALIC`        | `(inner, marker=None)` | `*text*`     |
| `BOLD`          | `(inner, marker=None)` | `**text**`   |
| `BOLD_ITALIC`   | `(inner, marker=None)` | `***text***` |
| `STRIKETHROUGH` | `(inner)`            | `~~text~~`     |

`inner` is a string, an inline node or a list of them; it must not be empty. `marker` is an
`EmphasisMarker` — the asterisk by default, `EmphasisMarker.UNDERSCORE` for underscores.
`STRIKETHROUGH` has **no** `marker` parameter: only the tilde writes strike-through.

**Example usage:**
```python
"Read " + BOLD("this") + " first."          # -> "Read **this** first."
ITALIC("this", EmphasisMarker.UNDERSCORE)   # -> "_this_"
BOLD("this", EmphasisMarker.UNDERSCORE)     # -> "__this__"
"Price " + STRIKETHROUGH("10 EUR") + " 8 EUR"   # -> "Price ~~10 EUR~~ 8 EUR"
```

> ⚠️ Whitespace at the edges of the text moves **outside** the markers (`** text **` would not
> render as emphasis), and an underscore marker does not work inside a word (`snake_case`).

[▲ Back to top](#-table-of-contents)

---

### `headings`

Factory functions over [`Heading`](README_MARKDOWN_BLOCKS.md#heading) with the level filled in —
block nodes. All six share one signature.

| Preset | Signature                              | Renders        |
|--------|----------------------------------------|----------------|
| `H1`   | `(inner, style=HeadingStyle.ATX)`      | `# text`       |
| `H2`   | `(inner, style=HeadingStyle.ATX)`      | `## text`      |
| `H3`   | `(inner, style=HeadingStyle.ATX)`      | `### text`     |
| `H4`   | `(inner, style=HeadingStyle.ATX)`      | `#### text`    |
| `H5`   | `(inner, style=HeadingStyle.ATX)`      | `##### text`   |
| `H6`   | `(inner, style=HeadingStyle.ATX)`      | `###### text`  |

`inner` is a string, an inline node or a list of them, and has to stay on one line. `style` is a
`HeadingStyle`: `ATX` (`# text`), `ATX_CLOSED` (`# text #`) or `SETEXT` (underlined — **levels 1
and 2 only**).

**Example usage:**
```python
H1("Project")                            # -> "# Project"
H1("Project", HeadingStyle.SETEXT)       # -> "Project\n======="
H2("Sub", HeadingStyle.ATX_CLOSED)       # -> "## Sub ##"
H6("Version 22.04")                      # -> "###### Version 22.04"

H6("x", HeadingStyle.SETEXT)             # -> raises: setext supports levels 1 and 2
```

[▲ Back to top](#-table-of-contents)

---

### `html`

Factory functions over [`Html`](README_MARKDOWN_BLOCKS.md#html). The group is **mixed** — some
presets are blocks, some stay inside a line:

| Preset     | Signature                                    | Renders                            | Level  |
|------------|----------------------------------------------|------------------------------------|--------|
| `DETAILS`  | `(summary, *body, expanded=False)`           | `<details>` with `<summary>`       | block  |
| `COMMENT`  | `(text)`                                     | `<!-- text -->`                    | block  |
| `ANCHOR`   | `(name)`                                     | `<a id="name"></a>`                | inline |
| `KBD`      | `(inner)`                                    | `<kbd>…</kbd>`                     | inline |
| `MARK`     | `(inner)`                                    | `<mark>…</mark>`                   | inline |
| `SUB`      | `(inner)`                                    | `<sub>…</sub>`                     | inline |
| `SUP`      | `(inner)`                                    | `<sup>…</sup>`                     | inline |

**Example usage:**
```python
"Press " + KBD("Enter") + "."        # -> "Press <kbd>Enter</kbd>."
"H" + SUB("2") + "O"                 # -> "H<sub>2</sub>O"
"x" + SUP("2")                       # -> "x<sup>2</sup>"
"This is " + MARK("important") + "." # -> "This is <mark>important</mark>."

ANCHOR("top")                        # -> '<a id="top"></a>'   (link to it with [text](#top))
COMMENT("TODO: add an example")      # -> "<!-- TODO: add an example -->"

DETAILS("Show more", "Hidden text.", expanded=True)
# <details open>
#
# <summary>Show more</summary>
#
# Hidden text.
#
# </details>
```

`DETAILS` writes blank lines around its body, so Markdown inside it (a list, code) is read as
Markdown and not as HTML — `DETAILS("More", BULLET_LIST("a", "b"))` works as expected.
`expanded=True` adds the bare `open` attribute. `COMMENT` must not contain `-->` or start with `>`
or `->`, and it is also the way to keep two lists with the same marker apart.

[▲ Back to top](#-table-of-contents)

---

### `links`

Factory functions over [`Link`](README_MARKDOWN_INLINE.md#link) — inline nodes. For an ordinary
link, use `Link(text, dest)` directly.

| Preset     | Signature                    | Renders                         |
|------------|------------------------------|---------------------------------|
| `IMAGE`    | `(alt, src, title=None)`     | `![alt](src "title")`           |
| `AUTOLINK` | `(url)`                      | `<url>`                         |
| `BARE_URL` | `(url)`                      | `url`, written as it is         |

**Example usage:**
```python
IMAGE("Logo", "img/logo.png")                 # -> "![Logo](img/logo.png)"
IMAGE("Logo", "img/logo.png", "Our logo")     # -> '![Logo](img/logo.png "Our logo")'
IMAGE("Logo", "my logo.png")                  # -> "![Logo](<my logo.png>)"
AUTOLINK("https://example.com")               # -> "<https://example.com>"
BARE_URL("https://example.com")               # -> "https://example.com"
```

`AUTOLINK` works in every renderer, because the angle brackets say that it is a link. `BARE_URL`
is the shorter form: GitHub turns it into a link, strict CommonMark renderers leave it as text.
An address with spaces or unbalanced parentheses is wrapped in `<...>` automatically.

[▲ Back to top](#-table-of-contents)

---

### `lists`

Factory functions over [`List`](README_MARKDOWN_CONTAINERS.md#list) and
[`ListItem`](README_MARKDOWN_CONTAINERS.md#listitem) — block nodes (the two item presets give an
item that lives **inside** a list).

| Preset          | Signature                                              | Renders                     |
|-----------------|--------------------------------------------------------|-----------------------------|
| `BULLET_LIST`   | `(*items, marker=ListMarker.DASH, tight=True)`         | `- item`                    |
| `NUMBERED_LIST` | `(*items, start=1, marker=ListMarker.DOT, tight=True)` | `1. item`                   |
| `TASK_ITEM`     | `(*blocks)`                                            | an item with `[ ]`          |
| `DONE_ITEM`     | `(*blocks)`                                            | an item with `[x]`          |

**Example usage:**
```python
BULLET_LIST("first", "second")
# - first
# - second

NUMBERED_LIST("first", "second", start=3, marker=ListMarker.PAREN)
# 3) first
# 4) second

BULLET_LIST(DONE_ITEM("write code"), TASK_ITEM("write tests"))
# - [x] write code
# - [ ] write tests

BULLET_LIST("first", ListItem("second", BULLET_LIST("nested")))
# - first
# - second
#   - nested
```

`BULLET_LIST` accepts `DASH`, `ASTERISK` and `PLUS`; `NUMBERED_LIST` accepts `DOT` and `PAREN` — the
wrong kind raises at construction. Pass a `ListItem` to put several blocks into one item. The
checkbox goes in front of the first line of text, so an item that starts with code or a nested list
is refused (`MARKDOWN_LIST_ITEM_CHECKED_WITHOUT_CONTENT`).

> ⚠️ A list that follows another list with the **same marker** merges with it. Use another marker,
> or a `COMMENT`, between them.

[▲ Back to top](#-table-of-contents)

---

### `references`

Factory functions over [`Reference`](README_MARKDOWN_INLINE.md#reference) (and, for `COLOR_CHIP`,
[`InlineCode`](README_MARKDOWN_INLINE.md#inlinecode)) — inline nodes. The shape of the value is
checked, not whether the user, issue or commit exists.

| Preset       | Signature  | Value                                              | Renders     |
|--------------|------------|----------------------------------------------------|-------------|
| `MENTION`    | `(user)`   | username without `@`                               | `@user`     |
| `ISSUE_REF`  | `(number)` | number (`int` or `str`) without `#`                | `#12`       |
| `COMMIT_REF` | `(sha)`    | lowercase hex hash, 7 to 40 characters             | `a1b2c3d`   |
| `EMOJI`      | `(name)`   | lowercase name without colons                      | `:name:`    |
| `COLOR_CHIP` | `(color)`  | `#RRGGBB`, `rgb(...)` or `hsl(...)` — not checked  | `` `#0969DA` `` |

**Example usage:**
```python
"Thanks, " + MENTION("octocat") + "!"           # -> "Thanks, @octocat!"
"Fixes " + ISSUE_REF(12) + "."                  # -> "Fixes #12."
"Introduced in " + COMMIT_REF("a1b2c3d") + "."  # -> "Introduced in a1b2c3d."
"Released " + EMOJI("tada")                     # -> "Released :tada:"
COLOR_CHIP("#0969DA")                           # -> "`#0969DA`"

MENTION("some user")     # -> raises: does not fit a mention
```

Other kinds are built directly: an issue of another repository is
`Reference(ReferenceKind.REPO_ISSUE, "owner/repo#12")`, a team is
`Reference(ReferenceKind.TEAM, "org/team")`. GitHub links and notifies a mention, shortens and links a
commit hash, and draws a small colour swatch next to a `COLOR_CHIP`; other renderers show plain text
or code.

[▲ Back to top](#-table-of-contents)

---

### `spacing`

Mixed presets over [`BlankLine`](README_MARKDOWN_BLOCKS.md#blankline),
[`ThematicBreak`](README_MARKDOWN_BLOCKS.md#thematicbreak) and
[`LineBreak`](README_MARKDOWN_INLINE.md#linebreak).

| Preset       | Kind                       | Signature  | Renders                          | Level  |
|--------------|----------------------------|------------|----------------------------------|--------|
| `EMPTY_LINE` | function                   | `(count=1)`| `count` blank lines              | block  |
| `RULE`       | ready instance             | —          | `---`                            | block  |
| `HARD_BREAK` | ready instance             | —          | two spaces + line break          | inline |

**Example usage:**
```python
H1("A") + RULE + "text"
# # A
#
# ---
#
# text

"first" + HARD_BREAK + "second"       # -> "first  \nsecond"

H1("A") + EMPTY_LINE(3) + "text"
# # A
#
#
#
# text
```

`RULE` and `HARD_BREAK` are used **without** parentheses. For another character or length use
`ThematicBreak(BreakChar.ASTERISK, 5)`; for another break style use
`LineBreak(LineBreakStyle.HTML)` (`<br>`) — the spaces of `HARD_BREAK` are invisible in an editor.

`EMPTY_LINE` **replaces** the separator between two blocks instead of adding to it: `EMPTY_LINE(1)`
changes nothing, `EMPTY_LINE(3)` gives three blank lines in total.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-presets--names-for-the-things-you-write-often)
