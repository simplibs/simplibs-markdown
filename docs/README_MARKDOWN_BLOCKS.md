# 🧱 `markdown/blocks` — Nodes That Are Lines of Their Own

The `blocks` package holds every **leaf block**: a heading, a paragraph, a block of code,
a rule, a footnote, a YAML header, a raw HTML element, a link definition, an explicit
blank line. A block is a node that occupies lines of its own; it is separated from its
neighbours by a blank line, which the containers add — a block never writes it itself.

All of them extend [`Markdown`](README_MARKDOWN_CLASS.md) directly and implement
`to_lines()`. Several unify a whole syntax family the same way `Emphasis` does in
[`inline`](README_MARKDOWN_INLINE.md): `Heading` covers three styles, `CodeBlock` two
kinds of fence plus the indented form, `Html` a block, an inline tag and a comment — each
as one class plus a small enum.

```python
from ..base_class import Markdown

class Paragraph(Markdown):
    ...
```

## A note on block slots — what `*blocks` accepts

Where a node holds other blocks (`Footnote(label, *blocks)`, `Html(tag, content)`, and
every container in [`containers`](README_MARKDOWN_CONTAINERS.md)) the same gate decides
what is allowed, `flatten_blocks`:

| You pass …                       | You get …                                        |
|----------------------------------|--------------------------------------------------|
| a non-empty `str`                | a `Paragraph` (escaped, like all strings)        |
| an empty string `""`             | a `BlankLine`                                    |
| an inline node                   | a `Paragraph` around it                          |
| a block node                     | the node itself                                  |
| a `Document`                     | its blocks, unpacked — documents never nest      |
| a `list` / `tuple` of the above  | flattened, in order                              |
| `None`                           | skipped                                          |
| anything else (`5`, …)           | `ParamError` (`MARKDOWN_NODE_NOT_MARKDOWN`)      |

## A note on two nodes whose level depends on a parameter

[`node_level`](README_MARKDOWN_CLASS.md#node_level) is a fixed class attribute for every
node in this package — except two. `Footnote` and `Html` can stand either *inside a line*
or *as a block*, depending on one parameter, so for them `node_level` is a read-only
**property**:

| Node       | Inline when …                   | Block when …                        |
|------------|---------------------------------|-------------------------------------|
| `Footnote` | `role=FootnoteRole.REFERENCE`   | `role=FootnoteRole.DEFINITION`      |
| `Html`     | `mode=HtmlMode.INLINE`          | `mode=HtmlMode.BLOCK` or `COMMENT`  |

That is what lets `"text" + Footnote("1", role=FootnoteRole.REFERENCE) + "."` stay one
line while the matching definition becomes a block at the end of the document.

---

## 🧭 Table of Contents

* [`Paragraph`](#paragraph)
* [`Heading`](#heading)
* [`CodeBlock`](#codeblock)
* [`ThematicBreak`](#thematicbreak)
* [`BlankLine`](#blankline)
* [`LinkDefinition`](#linkdefinition)
* [`Footnote`](#footnote)
* [`Frontmatter`](#frontmatter)
* [`Html`](#html)

[⬅️ Back to main README](../README.md#-blocks--nodes-that-are-lines-of-their-own)

---

### `Paragraph`

One or more lines of inline content. **Every argument is one line.**

**Parameters:**
* `*lines` (*str | InlineMarkdown | list*): Each argument is one line — a string, an inline
  node or a list of them (see [inline slots](README_MARKDOWN_INLINE.md#a-note-on-strings--what-an-inline-slot-accepts)).
  Inline nodes are joined **within** a line with `+`.
* `break_style` (*LineBreakStyle | None*, keyword-only, default `None`): When given, every
  line but the last ends with a hard break of this style. Without it the renderer joins the
  lines into one flowing paragraph.

**Raises:**
* `ParamError` (`MARKDOWN_PARAGRAPH_EMPTY`): there is no line with visible text.
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `break_style` has the wrong type.
* `ParamError` (`MARKDOWN_BLOCK_IN_INLINE`): a line is a block node.

**Example usage:**
```python
Paragraph("one", "two").to_lines()                  # -> ("one", "two")
Paragraph("See " + Link("docs", "x") + ".").to_lines()   # -> ("See [docs](x).",)

Paragraph("one", "two", break_style=LineBreakStyle.SPACES).to_lines()     # -> ("one  ", "two")
Paragraph("one", "two", break_style=LineBreakStyle.BACKSLASH).to_lines()  # -> ("one\\", "two")
Paragraph("one", "two", break_style=LineBreakStyle.HTML).to_lines()       # -> ("one<br>", "two")
```

**What a renderer would misread is cleaned up.** Every line is stripped of its indentation
(four spaces would make a code block), empty lines are dropped (they would end the
paragraph), and a line that would still *start a block* — `#`, `>`, `- `, `1.`, a fence, a
rule, a setext underline, `<!--` — is escaped. Normally `Text` has already escaped these; the
check is a second line of defence for text that arrives unescaped
(`Text(..., escape=False)`, raw HTML).

```python
Paragraph(Text("# raw", escape=False), Text("2024. y", escape=False)).to_lines()
# -> ("\\# raw", "2024\\. y")
```

**Under the hood** *(`to_lines`)*:
```python
rendered = []
for node in self.lines:
    for line in node.to_lines():
        line = line.lstrip()
        if not line:
            continue
        rendered.append(escape_block_start(line))

if self.break_style is not None:
    suffix = BREAK_SUFFIX[self.break_style]
    rendered = [line + suffix for line in rendered[:-1]] + rendered[-1:]
return tuple(rendered)
```

`BREAK_SUFFIX` is **not** the same table as `LineBreak`'s: the paragraph has already split
its content into lines, so the mark is appended to the end of each line but the last and no
newline is written (`SPACES: "  "`, `BACKSLASH: "\\"`, `HTML: "<br>"`).

[▲ Back to top](#-table-of-contents)

---

### `Heading`

A heading of level 1 to 6, in one of three styles — one idea written three ways.

**Parameters:**
* `inner` (*str | InlineMarkdown | list*): The heading text.
* `level` (*int*, default `1`): `1` (the biggest) to `6`. A `bool` is refused.
* `style` (*HeadingStyle*, default `HeadingStyle.ATX`): How the heading is written.

**`HeadingStyle` values:**

| Member       | Writes                  | Levels |
|--------------|-------------------------|--------|
| `ATX`        | `## Title`              | 1–6    |
| `ATX_CLOSED` | `## Title ##`           | 1–6    |
| `SETEXT`     | `Title` + underline     | 1–2 only (`=` for 1, `-` for 2) |

**Raises:**
* `ParamError` (`MARKDOWN_HEADING_LEVEL_OUT_OF_RANGE`): `level` is not an integer from 1 to 6.
* `ParamError` (`MARKDOWN_HEADING_SETEXT_LEVEL`): `SETEXT` with a level above 2.
* `ParamError` (`MARKDOWN_HEADING_MULTILINE`): the text spans more than one line.
* `ParamError` (`MARKDOWN_HEADING_EMPTY_SETEXT`): a `SETEXT` heading with no text.
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `style` has the wrong type.

**Example usage:**
```python
Heading("Title").to_lines()                                 # -> ("# Title",)
Heading("Title", 2).to_lines()                              # -> ("## Title",)
Heading("Title", 2, HeadingStyle.ATX_CLOSED).to_lines()     # -> ("## Title ##",)
Heading("Title", 1, HeadingStyle.SETEXT).to_lines()         # -> ("Title", "=====")
Heading(["API ", InlineCode("v2")], 3).to_lines()           # -> ("### API `v2`",)
```

The underline of a setext heading is at least as long as the text (and never shorter than
three characters).

**The trailing `#`.** A run of `#` after a space closes an ATX heading, so `# a #` would give
the heading `a`. When the text ends like that, the last `#` is written as `\#`; a `#` that
follows a letter (`C#`) is not a closing mark and stays as it is:

```python
Heading("a #").to_lines()   # -> ("# a \\#",)
Heading("C#").to_lines()    # -> ("# C#",)
```

**Under the hood** *(`to_lines`)*:
```python
text = self.inner.to_text().strip()

if self.style is HeadingStyle.SETEXT:
    underline = ("=" if self.level == 1 else "-") * max(3, len(text))
    return (text, underline)

if text.endswith("#") and not text.endswith("\\#"):
    text = text[:-1] + "\\#"
hashes = "#" * self.level

if not text:
    return (hashes,)
if self.style is HeadingStyle.ATX_CLOSED:
    return (f"{hashes} {text} {hashes}",)
return (f"{hashes} {text}",)
```

> 💡 `level` is the **heading** level (`#` vs `###`). It has nothing to do with
> [`node_level`](README_MARKDOWN_CLASS.md#node_level), which only says whether a node is a block.

[▲ Back to top](#-table-of-contents)

---

### `CodeBlock`

A block of code, fenced or indented. The code is written exactly as given; the only thing
that can go wrong is the fence, so it is chosen to fit.

**Parameters:**
* `code` (*str*): The code. **One** trailing newline is ignored — `"print(1)\n"` and
  `"print(1)"` are the same block, so a file read from disk gets no empty last line.
* `info` (*str | None*, default `None`): The info string after the opening fence, usually
  the language. Stripped of edge whitespace.
* `fence` (*FenceChar*, default `FenceChar.BACKTICK`): The fence character.
* `indented` (*bool*, default `False`): `True` writes an indented block (four spaces per
  non-empty line) instead of a fenced one.

**`FenceChar` values:** `BACKTICK` (`` ` ``), `TILDE` (`~`). The value of the member **is**
the character. A backtick fence cannot have a backtick in its info string; a tilde fence can.
It is also the way out of code that contains both kinds of fence.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `code`, `info` or `fence` has the wrong type.
* `ParamError` (`MARKDOWN_CODE_BLOCK_INDENTED_WITH_INFO`): an indented block has no fence to
  carry an info string.
* `ParamError` (`MARKDOWN_CODE_BLOCK_INFO_HAS_BACKTICK`): a backtick fence with a backtick in `info`.

**Example usage:**
```python
CodeBlock("print(1)", "python").to_lines()
# -> ("```python", "print(1)", "```")

CodeBlock("x", "py", fence=FenceChar.TILDE).to_lines()
# -> ("~~~py", "x", "~~~")

CodeBlock("a\n\nb", indented=True).to_lines()
# -> ("    a", "", "    b")
```

**A fence that the code cannot close.** A code block that shows another code block (this
documentation, for one) cannot be fenced with three backticks. The fence is one longer than
the longest run of its own character inside the code, and never shorter than three:

```python
CodeBlock("x\n```\ny\n```", "md").to_lines()
# -> ("````md", "x", "```", "y", "```", "````")
```

**Under the hood** *(`to_lines` and `choose_fence`)*:
```python
def to_lines(self) -> tuple[str, ...]:
    body = self.code[:-1] if self.code.endswith("\n") else self.code
    rows = body.split("\n") if body else []

    if self.indented:
        return tuple("    " + row if row else "" for row in rows)

    fence = choose_fence(self.code, self.fence.value)
    return (fence + (self.info or ""), *rows, fence)


def choose_fence(code: str, char: str = "`") -> str:
    runs = re.findall(re.escape(char) + "+", code)
    longest = max((len(run) for run in runs), default=0)
    return char * max(3, longest + 1)
```

Only runs of the **chosen** character count — a tilde fence is not closed by backticks.

> ⚠️ A line break inside `info` is not checked; it would end the fence line.

[▲ Back to top](#-table-of-contents)

---

### `ThematicBreak`

A horizontal rule.

**Parameters:**
* `char` (*BreakChar*, default `BreakChar.DASH`): The character that draws the rule.
* `length` (*int*, default `3`): How many characters to write; at least `3`. A `bool` is refused.

**`BreakChar` values:** `DASH` (`-`), `ASTERISK` (`*`), `UNDERSCORE` (`_`). Deliberately an
enum and not a free string: `+++` or `===` would let through something that is not a rule,
and `===` under a line of text is a heading underline.

**Raises:**
* `ParamError` (`MARKDOWN_THEMATIC_BREAK_INVALID_CHAR`): `char` is not a `BreakChar`.
* `ParamError` (`MARKDOWN_THEMATIC_BREAK_TOO_SHORT`): `length` is below 3 or not an integer.

**Example usage:**
```python
ThematicBreak().to_lines()                          # -> ("---",)
ThematicBreak(BreakChar.ASTERISK, 5).to_lines()     # -> ("*****",)
```

A dash rule right under a line of text would be a setext underline — but a blank line always
separates a block from the previous one, so a `ThematicBreak` never turns the line above it
into a heading.

**Under the hood:**
```python
def to_lines(self) -> tuple[str, ...]:
    return (self.char.value * self.length,)
```

[▲ Back to top](#-table-of-contents)

---

### `BlankLine`

One or more explicit empty lines — the number of blank lines **at its place** is set by the
author. It is also what `""` becomes in a [block slot](#a-note-on-block-slots--what-blocks-accepts).

**Parameters:**
* `count` (*int*, default `1`): How many empty lines. A positive integer; `bool` is refused.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `count` is not a positive integer.

**Example usage:**
```python
BlankLine().to_lines()      # -> ("",)
BlankLine(3).to_lines()     # -> ("", "", "")
```

**It replaces the separator, it does not add to it.** Blocks are separated by one blank line
automatically, but `separate_blocks` writes **no** separator next to a `BlankLine`. So
`BlankLine(1)` gives the same single blank line as no node at all, and `BlankLine(3)` gives
three blank lines in total — not four.

**Under the hood:**
```python
def to_lines(self) -> tuple[str, ...]:
    return ("",) * self.count
```

[▲ Back to top](#-table-of-contents)

---

### `LinkDefinition`

The target of reference links: `[label]: destination "title"`. It is invisible in the rendered
document; a [`Link`](README_MARKDOWN_INLINE.md#link) of kind `REFERENCE`, `COLLAPSED` or
`SHORTCUT` finds it by its label.

**Parameters:**
* `label` (*str*): The label that reference links use. Runs of whitespace are collapsed.
* `dest` (*str*): The destination — a URL or a path.
* `title` (*str | None*, default `None`): An optional title.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `label`, `dest` or `title` has the wrong type.
* `ParamError` (`MARKDOWN_LINK_DEFINITION_EMPTY_LABEL`): the label is empty (judged **after**
  its whitespace is collapsed).
* `ParamError` (`MARKDOWN_LINK_DEFINITION_EMPTY_DESTINATION`): the destination is empty.

**Example usage:**
```python
LinkDefinition("docs", "https://example.com").to_lines()
# -> ("[docs]: https://example.com",)

LinkDefinition("Foo   Bar", "https://example.com", "Title").to_lines()
# -> ('[Foo Bar]: https://example.com "Title"',)

LinkDefinition("a[1]", "my file.pdf").to_lines()
# -> ("[a\\[1\\]]: <my file.pdf>",)
```

The label is normalized once, when the node is built, and a `Link` writes its own label
through the same `normalize_label` — so a link and its definition always agree, even if the
author typed different whitespace. Brackets and backslashes in the label are escaped (they
would end it early); the destination and the title use the same helpers as `Link` (angle
brackets for a destination with spaces, the quotes that fit the title).

**Definitions stack.** `separate_blocks` puts **no** blank line between two consecutive
definitions, so a list of them reads the way people write it.

**Under the hood:**
```python
def to_lines(self) -> tuple[str, ...]:
    label = self.label.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
    title = f" {escape_link_title(self.title)}" if self.title else ""
    return (f"[{label}]: {escape_link_destination(self.dest)}{title}",)
```

[▲ Back to top](#-table-of-contents)

---

### `Footnote`

A footnote — **the marker in the text** or **the note itself**. They are two nodes of
different levels that belong together by one label, so one class with a `role` keeps the label
and the pairing in one place.

**Parameters:**
* `label` (*str*): The label that ties the marker to the note. Non-empty, no whitespace.
* `*blocks` (*str | Markdown | list*): The content of the note. Only for a definition —
  accepted by the [block-slot gate](#a-note-on-block-slots--what-blocks-accepts).
* `role` (*FootnoteRole*, keyword-only, default `FootnoteRole.DEFINITION`): Which part it is.

**`FootnoteRole` values:**

| Member       | Writes              | `node_level` |
|--------------|---------------------|--------------|
| `REFERENCE`  | `[^label]`          | `INLINE`     |
| `DEFINITION` | `[^label]: content` | `BLOCK`      |

**Raises:**
* `ParamError` (`MARKDOWN_FOOTNOTE_LABEL_INVALID`): the label is not a non-empty string
  without whitespace.
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `role` has the wrong type.
* `ParamError` (`MARKDOWN_FOOTNOTE_REFERENCE_WITH_BLOCKS`): a `REFERENCE` was given content.
* `ParamError` (`MARKDOWN_NO_BLOCKS`): a `DEFINITION` has no content.

**Example usage:**
```python
Footnote("1", "The note.").to_lines()
# -> ("[^1]: The note.",)

Footnote("1", role=FootnoteRole.REFERENCE).to_lines()
# -> ("[^1]",)

("Text" + Footnote("1", role=FootnoteRole.REFERENCE) + ".").to_text()
# -> "Text[^1]."
```

**A note with several blocks.** The blocks are separated by blank lines; the first line
follows `[^label]: `, every other line is indented by four spaces so the note stays one
footnote:

```python
Footnote("1", "First.", "Second.").to_lines()
# -> ("[^1]: First.", "", "    Second.")

Footnote("n", Paragraph("a"), CodeBlock("x", "py")).to_lines()
# -> ("[^n]: a", "", "    ```py", "    x", "    ```")
```

**Under the hood** *(`to_lines`)*:
```python
def to_lines(self) -> tuple[str, ...]:
    if self.role is FootnoteRole.REFERENCE:
        return (f"[^{self.label}]",)

    body = separate_blocks(self.blocks, gap=1)
    return prefix_lines(body, f"[^{self.label}]: ", "    ")
```

`prefix_lines` is the one mechanism behind **all** nesting in the library: a footnote, a quote
(`> `) and a list item (marker, then spaces) differ only in the prefixes they pass. An empty
line keeps the prefix but loses the spaces behind it, so no trailing whitespace appears.

[▲ Back to top](#-table-of-contents)

---

### `Frontmatter`

A YAML header between two `---` lines, for the start of a document — read by static site
generators, Obsidian and GitHub.

**Parameters:**
* `data` (*dict*): The header. Keys: strings. Values: strings, numbers, bools, `None`, and
  lists or dictionaries of them (nesting is fine).

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `data` is not a dictionary.
* `ConversionError` (`MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE`): a key is not a string, or a
  value cannot be written as YAML (a `set`, `NaN`, infinity, a date, …).

**Example usage:**
```python
Frontmatter({"title": "Hi", "tags": ["a", "b"], "draft": False}).to_lines()
# -> ("---",
#     'title: "Hi"',
#     "tags:",
#     '  - "a"',
#     '  - "b"',
#     "draft: false",
#     "---")

Frontmatter({"x": {1, 2}})    # -> raises ConversionError: a set has no YAML form here
```

**Written at construction.** The YAML is produced once, in `__init__`, so an unsupported
value fails **where the data is passed** and not in the middle of writing a file. The cost:
changing the dictionary afterwards does not change the output.

**A small writer, not a YAML library.** Front matter is a few keys and lists, and a writer for
exactly that is shorter than a dependency — and every choice in it is visible:

* **Strings are always quoted** (`"yes"`, `"2024-01-01"`, `"1.0"` would otherwise become a
  boolean, a date and a number). `ensure_ascii=False`, so `"název"` stays `"název"`.
* **Keys are bare when safe** (`[A-Za-z_][\w-]*`) and quoted otherwise. A key YAML 1.1 reads
  as a value — `true`, `false`, `null`, `yes`, `no`, `on`, `off`, `y`, `n`, in any case — is
  quoted too: `"yes": "no"`.
* **Empty collections** stay on the key's line (`e: []`, `d: {}`).
* **A dash with a nested collection** stands alone on its line and the content follows one
  level deeper — valid YAML that avoids the alignment rules of `- key: value`:

```python
Frontmatter({"l": [{"a": 1, "b": 2}, 3]}).to_lines()
# -> ("---", "l:", "  -", "    a: 1", "    b: 2", "  - 3", "---")
```

* No anchors, no multi-line strings, no sets, no dates — outside the supported types is an
  error, not a guess.

**Under the hood:**
```python
def __init__(self, data: dict) -> None:
    if not isinstance(data, dict):
        raise_param_invalid_type_error("data", data, dict)

    lines = ("---", *yaml_lines(data), "---")
    self.data = data
    self.lines = lines

def to_lines(self) -> tuple[str, ...]:
    return self.lines
```

[▲ Back to top](#-table-of-contents)

---

### `Html`

Raw HTML written through validated parts: a **block**, an **inline** tag or a **comment**.
The tag and attribute names are checked and the values escaped, so a string from outside
cannot break the tag.

**Parameters:**
* `tag` (*str | None*, default `None`): The tag name (`[A-Za-z][A-Za-z0-9-]*` — custom
  elements such as `my-tag` are fine). Stored lowercase. Ignored for a comment.
* `content` (*str | Markdown | list | None*, default `None`): The content. For a comment it
  must be a string.
* `attrs` (*dict | None*, default `None`): The attributes.
* `mode` (*HtmlMode*, default `HtmlMode.BLOCK`): How the node stands in the document.

**`HtmlMode` values:**

| Member    | Writes                         | `node_level` |
|-----------|--------------------------------|--------------|
| `BLOCK`   | `<details>…</details>`         | `BLOCK`      |
| `INLINE`  | `<kbd>Ctrl</kbd>` inside a line| `INLINE`     |
| `COMMENT` | `<!-- text -->`                | `BLOCK`      |

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `mode` is not an `HtmlMode`, `attrs` not a
  dictionary, or the content of a comment not a string.
* `ParamError` (`MARKDOWN_HTML_INVALID_TAG`): a missing or invalid tag name.
* `ParamError` (`MARKDOWN_HTML_INVALID_ATTRIBUTE`): an attribute name outside the HTML
  specification (a space, a quote or `=` can never get through).
* `ParamError` (`MARKDOWN_HTML_VOID_TAG_WITH_CONTENT`): content for a tag that cannot hold
  any (`br`, `img`, `hr`, `meta`, …).
* `ParamError` (`MARKDOWN_HTML_COMMENT_TERMINATOR`): a comment that would end early (`-->`
  inside it, or a start with `>` / `->`).
* `ParamError` (`MARKDOWN_BLOCK_IN_INLINE`): an inline tag was given a block.

**Attribute values:** escaped with `html.escape(..., quote=True)`. `True` writes a bare
attribute (`open`); `False` and `None` mean "not set" and leave the attribute out — so a
condition can be passed directly.

```python
Html("details", attrs={"open": True, "hidden": False, "id": None, "class": "x"}).to_lines()
# -> ('<details open class="x"></details>',)

Html("img", attrs={"src": "a.png", "alt": 'say "hi"'}).to_lines()
# -> ('<img src="a.png" alt="say &quot;hi&quot;">',)
```

**One line, or blocks.** A string or an inline node stays on the line of the tag; anything
else is read as blocks and gets lines of its own. Block content is wrapped in blank lines —
`<details>` followed directly by a Markdown list is read as HTML to the end of the block,
unless a blank line separates them.

```python
Html("div", "text").to_lines()
# -> ("<div>text</div>",)

Html("details", [Html("summary", "More"), Paragraph("Body")]).to_lines()
# -> ("<details>", "", "<summary>More</summary>", "", "Body", "", "</details>")
```

**An inline tag takes a list of inline items**, so it can be built into a line with `+`:

```python
Html("kbd", "Ctrl", mode=HtmlMode.INLINE).to_lines()     # -> ("<kbd>Ctrl</kbd>",)
("Press " + Html("kbd", ["Ctrl", " + ", "C"], mode=HtmlMode.INLINE) + ".").to_text()
# -> "Press <kbd>Ctrl \\+ C</kbd>."
```

**Void tags and empty tags.** A void tag is only the opening tag; a normal tag without
content is the opening and the closing tag:

```python
Html("br").to_lines()    # -> ("<br>",)
Html("p").to_lines()     # -> ("<p></p>",)
```

**Comments.** One line, or the text between two marker lines when it has several:

```python
Html(content="note", mode=HtmlMode.COMMENT).to_lines()      # -> ("<!-- note -->",)
Html(content="a\nb", mode=HtmlMode.COMMENT).to_lines()      # -> ("<!--", "a", "b", "-->")
Html(mode=HtmlMode.COMMENT).to_lines()                      # -> ("<!-- -->",)
```

**Under the hood** *(`to_lines`)*:
```python
def to_lines(self) -> tuple[str, ...]:
    if self.mode is HtmlMode.COMMENT:
        if "\n" in self.content:
            return ("<!--", *self.content.split("\n"), "-->")
        return (f"<!-- {self.content} -->" if self.content else "<!-- -->",)

    opening = build_html_open_tag(self.tag, self.attrs)
    if self.tag in VOID_TAGS:
        return (opening,)

    closing = f"</{self.tag}>"
    if self.content is None:
        return (opening + closing,)

    if not isinstance(self.content, tuple):
        return (f"{opening}{self.content.to_text()}{closing}",)

    body = separate_blocks(self.content, gap=1)
    return (opening, "", *body, "", closing)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-blocks--nodes-that-are-lines-of-their-own)
