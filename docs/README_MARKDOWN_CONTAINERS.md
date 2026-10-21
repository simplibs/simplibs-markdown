# 📦 `markdown/containers` — Nodes That Hold Other Blocks

The `containers` package holds every node that **contains other blocks**: the document
itself, a quote, a list with its items, and a table. This is also where the `+` operator
ends up whenever a block is involved — everything added with `+` that contains a block
becomes a `Document`.

Containers have no syntax of their own to speak of. They share one idea: **nesting is
prefixing.** A quote is its content with `> ` in front of every line; a list item is its
content with a marker in front of the first line and indentation in front of the others.
Lists, code and quotes inside a container need no special case, because by the time a
container sees them they already are lines.

```python
from ..base_class import Markdown

class Document(Markdown):
    ...
```

## A note on the two mechanisms every container is built from

Both live in `_common/helpers` and are shared with `Footnote` and `Html` from
[`blocks`](README_MARKDOWN_BLOCKS.md):

* **`separate_blocks(blocks, gap)`** writes blocks one after another with `gap` blank lines
  between them. It writes **no** separator next to an explicit `BlankLine` (which already is
  one) and **none** between two consecutive `LinkDefinition`s (which stack).
* **`prefix_lines(lines, first, rest)`** puts `first` before the first line and `rest` before
  every other. An empty line keeps the prefix but loses the trailing spaces, so a quoted
  blank line is a bare `>`, not `> `.

The whole nesting of Markdown is these two functions applied from the inside out.

Every container takes its content through the same
[block-slot gate](README_MARKDOWN_BLOCKS.md#a-note-on-block-slots--what-blocks-accepts):
a string becomes a `Paragraph`, `""` a `BlankLine`, an inline node gets a `Paragraph`
around it, a `Document` is unpacked (documents never nest), lists are flattened and `None`
is skipped.

---

## 🧭 Table of Contents

* [`Document`](#document)
* [`Quote`](#quote)
* [`List`](#list)
* [`ListItem`](#listitem)
* [`Table`](#table)

[⬅️ Back to main README](../README.md#-containers--nodes-that-hold-other-blocks)

---

### `Document`

A whole document: blocks separated by blank lines. The root of composition — it is what you
get from `H1("Title") + "text"`, and what `MarkdownText` and `to_file` write out.

**Parameters:**
* `*blocks` (*str | Markdown | list*): The content. At least one block is required.
* `gap` (*int*, keyword-only, default `1`): How many blank lines go between two blocks.
  A non-negative integer; `bool` is refused.
* `final_newline` (*bool*, keyword-only, default `True`): `True` ends `to_text()` with a
  newline — the way a text file is expected to end.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `gap` is not a non-negative integer.
* `ParamError` (`MARKDOWN_NO_BLOCKS`): there is no content.
* `ParamError` (`MARKDOWN_NODE_NOT_MARKDOWN`): an item is neither a string nor a node.

**Example usage:**
```python
Document(Heading("T"), "text", Heading("S", 2), "more").to_text()
# -> "# T\n\ntext\n\n## S\n\nmore\n"

Document("a", "b", gap=2).to_text()               # -> "a\n\n\nb\n"
Document("a", final_newline=False).to_text()      # -> "a"
Document(None, ["a", ["b"]]).to_lines()           # -> ("a", "", "b")
```

**Documents never nest.** A document passed into another document (or any container) gives
up its blocks and **its own `gap` and `final_newline`** — only the outermost document keeps
them:

```python
Document(Document("a", "b"), "c", gap=2).blocks
# -> (Paragraph('a'), Paragraph('b'), Paragraph('c'))   # all three separated by gap=2

(Document("a", "b", gap=3) + "c").to_text()       # -> "a\n\nb\n\nc\n"   # the new document: gap=1
```

**`to_lines()` and `to_text()` differ in one thing.** `to_lines()` never ends with an empty
line, so a container that nests the document is not affected; only `to_text()` adds the
final newline.

```python
Document("a").to_lines()    # -> ("a",)
Document("a").to_text()     # -> "a\n"
```

**Under the hood:**
```python
def to_lines(self) -> tuple[str, ...]:
    return separate_blocks(self.blocks, self.gap)

def to_text(self) -> str:
    text = "\n".join(self.to_lines())
    return text + "\n" if self.final_newline else text
```

> ⚠️ `gap=0` puts blocks on consecutive lines, and two paragraphs on consecutive lines are
> **one** paragraph for a renderer (`"a\nb"` renders as "a b"). Use it for blocks that stay
> distinct on their own — definitions, headings — not for prose.

[▲ Back to top](#-table-of-contents)

---

### `Quote`

A block quote, optionally a GitHub alert (`> [!NOTE]`).

**Parameters:**
* `*blocks` (*str | Markdown | list*): The content. Required for a plain quote; an alert may
  be empty (only the marker).
* `alert` (*AlertKind | None*, keyword-only, default `None`): When given, the quote is an alert.

**`AlertKind` values:** `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION` — the value is the
word written between the brackets, in capitals as GitHub requires.

**Raises:**
* `ParamError` (`MARKDOWN_QUOTE_UNKNOWN_ALERT`): `alert` is not an `AlertKind`.
* `ParamError` (`MARKDOWN_NO_BLOCKS`): a plain quote with no content.

**Example usage:**
```python
Quote("text").to_lines()                       # -> ("> text",)
Quote("a", "b").to_lines()                     # -> ("> a", ">", "> b")
Quote("a", Quote("b")).to_lines()              # -> ("> a", ">", "> > b")
Quote("Careful.", alert=AlertKind.WARNING).to_lines()
# -> ("> [!WARNING]", "> Careful.")
Quote(alert=AlertKind.TIP).to_lines()          # -> ("> [!TIP]",)

Quote(Paragraph("a"), CodeBlock("x", "py")).to_lines()
# -> ("> a", ">", "> ```py", "> x", "> ```")
```

Lists, code and other quotes inside a quote need no special handling — they already are lines,
and the quote only prefixes them. An alert's content follows the marker **directly**, with no
blank line between (that is what GitHub wants).

**Under the hood:**
```python
def to_lines(self) -> tuple[str, ...]:
    lines = separate_blocks(self.blocks, gap=1)

    if self.alert is not None:
        lines = (f"[!{self.alert.value}]", *lines)

    return prefix_lines(lines, "> ")
```

> ⚠️ Other renderers show an alert as an ordinary quote whose first line is `[!NOTE]`.

[▲ Back to top](#-table-of-contents)

---

### `List`

A bullet or an ordered list — one node for both kinds.

**Parameters:**
* `*items` (*ListItem | str | Markdown*): The items. A `ListItem` is used as it is; a string or
  a node becomes an item of its own. At least one is required.
* `ordered` (*bool*, keyword-only, default `False`): `True` writes a numbered list.
* `marker` (*ListMarker | None*, keyword-only, default `None`): The marker. Defaults to `-`
  for bullets and `.` for numbers.
* `start` (*int*, keyword-only, default `1`): The number of the first item of an ordered list.
* `tight` (*bool*, keyword-only, default `True`): `False` puts a blank line between the items.

**`ListMarker` values:**

| Member     | Writes   | For           |
|------------|----------|---------------|
| `DASH`     | `- a`    | bullet lists  |
| `ASTERISK` | `* a`    | bullet lists  |
| `PLUS`     | `+ a`    | bullet lists  |
| `DOT`      | `1. a`   | ordered lists |
| `PAREN`    | `1) a`   | ordered lists |

`ordered` and the marker must agree — a `DOT` marker on a bullet list is an error at
construction, not a quietly different list.

**Raises:**
* `ParamError` (`MARKDOWN_LIST_NO_ITEMS`): no items.
* `ParamError` (`MARKDOWN_LIST_ITEM_NOT_LIST_ITEM`): an item is not a string, a node or a
  `ListItem` — including a Python `list` of them: every item is its own argument.
* `ParamError` (`MARKDOWN_LIST_MARKER_ORDERED_MISMATCH`): the marker does not fit the kind of list.
* `ParamError` (`MARKDOWN_LIST_START_NEGATIVE`): `start` is not a non-negative integer.
* `ParamError` (`MARKDOWN_LIST_START_ON_BULLET`): `start` other than 1 on a bullet list.
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `marker` is not a `ListMarker`.

**Example usage:**
```python
List("a", "b", "c").to_lines()                      # -> ("- a", "- b", "- c")
List("a", "b", ordered=True).to_lines()             # -> ("1. a", "2. b")
List("a", "b", ordered=True, start=5).to_lines()    # -> ("5. a", "6. b")
List("a", "b", ordered=True, marker=ListMarker.PAREN).to_lines()   # -> ("1) a", "2) b")
List("a", "b", marker=ListMarker.ASTERISK).to_lines()              # -> ("* a", "* b")

List("a", ordered=True, marker=ListMarker.DASH)    # -> raises: marker and kind disagree
```

**Tight and loose.** Tight items stand on consecutive lines; loose items have a blank line
between them (and renderers wrap their paragraphs in `<p>`). A list is loose when asked to be
(`tight=False`) **or when one of its items cannot be tight** — see [`ListItem`](#listitem).

```python
List("a", "b", tight=False).to_lines()      # -> ("- a", "", "- b")
```

**Nesting is done through `ListItem`.** A list passed as an *item* is a new item; to put a list
*inside* an item, pass it as a block of a `ListItem`:

```python
List("a", List("b", "c"), "d").to_lines()
# -> ("- a", "- - b", "  - c", "- d")           # the inner list is an item of its own

List(ListItem("a", List("b", "c")), "d").to_lines()
# -> ("- a", "  - b", "  - c", "- d")           # the inner list belongs to "a"
```

**Indentation follows the marker.** Every line after the first of an item is indented by the
width of **its own** marker (`1. ` is 3, `10. ` is 4), so nested content always stays inside
the item:

```python
List(ListItem("a", List("b")), "c", ordered=True).to_lines()
# -> ("1. a", "   - b", "2. c")

List(*[f"i{n}" for n in range(1, 11)], ordered=True).to_lines()[8:]
# -> ("9. i9", "10. i10")
```

**Under the hood** *(`to_lines`)*:
```python
loose = not self.tight or any(item.needs_loose for item in self.items)

lines = []
for index, item in enumerate(self.items):
    if self.ordered:
        marker = f"{self.start + index}{self.marker.value} "
    else:
        marker = f"{self.marker.value} "
    content = item.content_lines(loose)

    if index and loose:
        lines.append("")

    if content:
        lines.extend(prefix_lines(content, marker, " " * len(marker)))
    else:
        lines.append(marker.rstrip())
return tuple(lines)
```

An item without content is the bare marker (`-`, `1.`).

> ⚠️ Two lists with the **same marker** one after another merge into one list in CommonMark,
> even with a blank line between them. Use a different marker, or an `Html` comment
> (`Html(content="", mode=HtmlMode.COMMENT)`) between them.

[▲ Back to top](#-table-of-contents)

---

### `ListItem`

One item of a list: any blocks, and an optional checkbox. The list decides the marker and
whether items are tight or loose; the item writes its **own content**.

**Parameters:**
* `*blocks` (*str | Markdown | list*): The content — several paragraphs, code, a nested list.
* `checked` (*bool | None*, keyword-only, default `None`): `True` writes `[x]`, `False` writes
  `[ ]`, `None` writes no checkbox.

**Raises:**
* `ParamError` (`MARKDOWN_LIST_ITEM_CHECKED_WITHOUT_CONTENT`): `checked` is set but the content
  does not **start with a paragraph** — the checkbox is written in front of text.

**Example usage:**
```python
ListItem("todo", checked=False).to_lines()        # -> ("- [ ] todo",)
ListItem("done", checked=True).to_lines()         # -> ("- [x] done",)
List(ListItem("T1", checked=True), ListItem("T2", checked=False)).to_lines()
# -> ("- [x] T1", "- [ ] T2")

ListItem(CodeBlock("x"), checked=True)    # -> raises: a checkbox needs text in front
```

**Members used by `List`:**

* `needs_loose` (*property*, `bool`): `True` when two paragraphs follow each other inside the
  item — which a tight list cannot write. `List` reads it and writes the **whole** list loose.
* `content_lines(loose)` (*method*): the lines of the content without the marker. `loose=True`
  puts a blank line between the item's blocks; the checkbox goes in front of the first line.

```python
ListItem("a", "b").needs_loose               # -> True
ListItem("a", CodeBlock("x")).needs_loose    # -> False

ListItem("a", "b").content_lines(True)       # -> ("a", "", "b")
ListItem("a", "b").content_lines(False)      # -> ("a", "b")
```

**Alone, an item is a bullet item.** A bare `ListItem` writes itself with a `-` marker:

```python
ListItem("a", "b").to_lines()    # -> ("- a", "", "  b")
ListItem().to_lines()            # -> ("-",)
```

**Under the hood:**
```python
def to_lines(self) -> tuple[str, ...]:
    content = self.content_lines(self.needs_loose)
    if not content:
        return ("-",)
    return prefix_lines(content, "- ", "  ")
```

`ListItem` writes its content itself instead of building a one-item `List`, so the two classes
do not import each other.

[▲ Back to top](#-table-of-contents)

---

### `Table`

A GFM table: a header, a separator row that carries the alignment, and rows.

**Parameters:**
* `head`: The header — a list of cells, or one string (or node) for a one-column table.
* `rows` (default `()`): The rows. Any iterable that is **not** a string; each row a list of
  cells, or one string for a one-column table.
* `align` (*list[TableAlign] | tuple[TableAlign, ...] | None*, default `None`): One alignment per
  column. Defaults to no alignment.

A **cell** is a string, an inline node or a list of them — it goes through the same
[inline gate](README_MARKDOWN_INLINE.md#a-note-on-strings--what-an-inline-slot-accepts) as every
other inline slot, so a string is escaped. A number is not a cell: write `str(30)`.

**`TableAlign` values:** `NONE`, `LEFT`, `CENTER`, `RIGHT`. The values are identifiers only; the
form of the separator cell is `Table`'s business.

| Member   | Separator cell | Padding of the cell |
|----------|----------------|---------------------|
| `NONE`   | `---`          | on the right        |
| `LEFT`   | `:--`          | on the right        |
| `CENTER` | `:-:`          | on both sides       |
| `RIGHT`  | `--:`          | on the left         |

**Raises:**
* `ParamError` (`MARKDOWN_TABLE_NO_COLUMNS`): the header is empty.
* `ParamError` (`MARKDOWN_TABLE_ROW_WIDTH_MISMATCH`): a row has another width than the header.
* `ParamError` (`MARKDOWN_TABLE_ALIGN_WIDTH_MISMATCH`): `align` has another width than the header.
* `ParamError` (`MARKDOWN_TABLE_CELL_MULTILINE`): a cell contains a line break.
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `rows` is a string or not iterable, `align` is not
  a list/tuple of `TableAlign`, or a row is not a string, node, list or tuple.
* `ParamError` (`MARKDOWN_NODE_NOT_MARKDOWN`): a cell is not content (e.g. a number).

A wrong row width is an **error**, because GFM would pad or cut such a row without a word.

**Example usage:**
```python
Table(["Name", "Age"], [["Ann", "30"], ["Bob", "4"]]).to_lines()
# -> ("| Name | Age |",
#     "| ---- | --- |",
#     "| Ann  | 30  |",
#     "| Bob  | 4   |")

Table(
    ["Name", "Age", "City"],
    [["Ann", "30", "Praha"]],
    align=[TableAlign.LEFT, TableAlign.RIGHT, TableAlign.CENTER],
).to_lines()
# -> ("| Name | Age |  City |",
#     "| :--- | --: | :---: |",
#     "| Ann  |  30 | Praha |")

Table("Name", ["Ann", "Bob"]).to_lines()           # a one-column table
Table(["a", "b"]).to_lines()                       # -> header and separator only
Table([InlineCode("x"), Emphasis("y")], [[Link("d", "u"), "z"]]).to_lines()
# -> ("| `x`    | *y* |", "| ------ | --- |", "| [d](u) | z   |")
```

**Pipes.** In a table `|` separates cells, so a pipe that belongs to the text is written `\|`.
Because the text a cell receives already has its own backslashes escaped (`\\`), a pipe is
escaped **only when an even number of backslashes (possibly none) stands before it** — an odd
number means it is escaped already.

```python
Table(["a", "b"], [["x|y", "p\\|q"]]).to_lines()[2]
# -> "| x\\|y | p\\\\\\|q |"      # the cell "p\|q" keeps its backslash AND its pipe
```

**Under the hood** *(`to_lines`)*:
```python
# Each column is as wide as its longest cell, and at least 3 (the separator needs it)
widths = [
    max(3, len(title), *(len(row[index]) for row in self.rows))
    for index, title in enumerate(self.head)
]

def line(cells):
    padded = (pad_cell(cell, width, align) for cell, width, align in zip(cells, widths, self.align))
    return "| " + " | ".join(padded) + " |"

separator = "| " + " | ".join(
    separator_cell(width, align) for width, align in zip(widths, self.align)
) + " |"

return (line(self.head), separator, *(line(row) for row in self.rows))
```

The padding exists only so the **source** lines up in an editor — the table renders identically
without it. `separator_cell` writes `:` on each side the alignment asks for (`CENTER` needs three
characters, which is why no column is narrower than 3).

> ⚠️ The width is `len` — the number of characters. Wide characters (CJK) and combining marks
> occupy another width on screen, so such a table is not aligned in the source. The rendered
> table is not affected.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-containers--nodes-that-hold-other-blocks)
