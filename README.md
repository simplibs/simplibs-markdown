# 📝 `simplibs-markdown`

[![PyPI](https://img.shields.io/pypi/v/simplibs-markdown)](https://pypi.org/project/simplibs-markdown/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-markdown/blob/main/LICENSE)
[![tests](https://github.com/simplibs/simplibs-markdown/actions/workflows/tests.yml/badge.svg)](https://github.com/simplibs/simplibs-markdown/actions)

**Write Markdown as Python — escaped, checked and always well-formed.**

A lightweight Python library that builds Markdown out of small, named `Markdown` objects
instead of hand-assembled strings. Nodes combine with the plain `+` operator, each syntax
*family* of Markdown (emphasis, links, headings, lists, references) collapses into one
parameterized mechanism instead of dozens of special cases, and the finished tree writes
ordinary Markdown text — to the screen, to a string or straight to a file.

```python
from simplibs.markdown import Paragraph, MarkdownText
from simplibs.markdown.presets import H1, BOLD, NOTE, BULLET_LIST

doc = (
    H1("simplibs")
    + Paragraph("Tiny libraries, " + BOLD("one job each") + ".")
    + NOTE("This text was written by Python.")
    + BULLET_LIST("regex", "markdown", "file")
)
print(MarkdownText(doc))
```

```markdown
# simplibs

Tiny libraries, **one job each**.

> [!NOTE]
> This text was written by Python.

- regex
- markdown
- file
```

> `simplibs-markdown` builds directly on the same architectural pattern as
> [`simplibs-regex`](https://pypi.org/project/simplibs-regex/) (a base class + composable
> containers + presets) and
> [`simplibs-rules`](https://pypi.org/project/simplibs-rules/) — if either of those is
> familiar, this library's shape will be too.

---

## 🧭 The Core Philosophy

Markdown written by hand is a string, and a string cannot tell a heading from a sentence that
happens to start with `#`. A user name with an underscore turns half a paragraph into italics,
a `|` inside a table cell splits the cell, and a code sample that contains three backticks ends
its own block. `simplibs-markdown` replaces the string with a small tree of ordinary Python
objects: each node is independently named, typed and validated, and the tree composes with `+`
the way a sentence is built from words.

* **A string is content, never Markdown.** Everything you pass as a string is escaped, so
  `Paragraph("snake_case and *not emphasis*")` writes exactly that text. To write formatting, pass
  a node (`BOLD("this")`); the one deliberate way out is `Text(..., escape=False)`.
* **One mechanism per family.** Four spellings of emphasis become one `Emphasis(kind, marker)`.
  Twelve link forms become one `Link(kind, image)`. Three heading styles become one
  `Heading(level, style)`. The goal is never a new class for every piece of syntax, but the
  smallest set of genuinely different mechanisms, with every variant a parameter or a named preset.
* **Structure is checked when you build it.** A heading inside bold text, a table inside a link, a
  setext heading of level 3, a list marker that does not fit the kind of list, a table row of the
  wrong width — each is rejected the moment you write it, with a message that names what is wrong,
  and not discovered later as a broken page.
* **Delimiters that fit.** A code span and a code fence are chosen to be one backtick longer than
  anything inside them, a link destination with a space is wrapped in `<...>`, a table cell's pipe
  is escaped — the text you give is the text you get.
* **Nesting is prefixing.** A quote is its content with `> ` in front of every line; a list item is
  its content under a marker. Lists, code and quotes inside each other need no special case.
* **Layers that only look left.**
  `_common` ← `base_class` ← `inline` ← `blocks` ← `containers` ← `output` ← `presets` — every layer
  imports only from those before it.

```python
Heading("Title", 1, HeadingStyle.SETEXT)       # -> "Title\n====="
Link("docs", kind=LinkKind.REFERENCE, label="Foo  Bar")   # -> "[docs][Foo Bar]"
CodeBlock("x\n```\ny\n```", "md")              # a fence of four backticks — the code cannot close it
```

---

## 📦 Installation

```bash
pip install simplibs-markdown
```

Requires Python 3.11+. Runtime dependencies (installed automatically): the simplibs `exception`
library (structured error messages) and the simplibs `file` library (the atomic write behind
`to_file`).

---

## 🚀 Quick Start in 60 Seconds

### Level 1: Compose with `+` and print

```python
from simplibs.markdown import Paragraph, MarkdownText
from simplibs.markdown.presets import H1, BOLD, NOTE, BULLET_LIST

doc = (
    H1("simplibs")
    + Paragraph("Tiny libraries, " + BOLD("one job each") + ".")
    + NOTE("This text was written by Python.")
    + BULLET_LIST("regex", "markdown", "file")
)
print(MarkdownText(doc))
```

Inline nodes joined with `+` stay one line; anything joined with a block becomes a `Document`.

### Level 2: Strings are safe, tables are checked

```python
from simplibs.markdown import InlineCode, Link, MarkdownText, Paragraph, Table

print(MarkdownText(Paragraph("snake_case and *not emphasis* and # not a heading")))
# snake\_case and \*not emphasis\* and # not a heading

table = Table(
    ["Library", "Does"],
    [
        [InlineCode("regex"), "Patterns without regex syntax"],
        [Link("markdown", "https://github.com/simplibs/simplibs-markdown"), "This one"],
    ],
)
print(MarkdownText(table))
# | Library                                                   | Does                          |
# | --------------------------------------------------------- | ----------------------------- |
# | `regex`                                                   | Patterns without regex syntax |
# | [markdown](https://github.com/simplibs/simplibs-markdown) | This one                      |
```

### Level 3: A whole file — front matter, checklists, code — written to disk

```python
from simplibs.markdown import CodeBlock, Document, Frontmatter, to_file
from simplibs.markdown.presets import H1, BULLET_LIST, DONE_ITEM, TASK_ITEM

report = Document(
    Frontmatter({"title": "Release notes", "draft": False}),
    H1("Release 0.1.0"),
    BULLET_LIST(DONE_ITEM("write code"), TASK_ITEM("write tests")),
    CodeBlock("pip install simplibs-markdown", "bash"),
)

to_file(report, "out/RELEASE.md")      # the folder is created; the write is atomic
```

````markdown
---
title: "Release notes"
draft: false
---

# Release 0.1.0

- [x] write code
- [ ] write tests

```bash
pip install simplibs-markdown
```
````

---

## 🛠️ Architecture & Package Structure

```
src/simplibs/markdown/
├── _common/               ◄── Helpers, enums and diagnostic raisers shared by more than one layer
├── base_class/            ◄── Abstract base classes Markdown & InlineMarkdown, the NodeLevel enum
├── inline/                ◄── Nodes inside a line (Text, Emphasis, InlineCode, Link, Entity, Math,
│                              Reference, LineBreak, InlineJoin)
├── blocks/                ◄── Leaf blocks (Paragraph, Heading, CodeBlock, ThematicBreak, BlankLine,
│                              LinkDefinition, Footnote, Frontmatter, Html)
├── containers/            ◄── Nodes that hold other blocks (Document, Quote, List, ListItem, Table)
├── output/                ◄── MarkdownText and to_file — from a node to text and to a file
└── presets/               ◄── Named shortcuts over nodes (alerts, code, emphasis, headings, html,
                               links, lists, references, spacing)
```

The root of the package exports the nodes, base classes, enums, the output layer, and all presets
so they can be used directly from the root or via `simplibs.markdown.presets`:

```python
from simplibs.markdown import Heading, Table, Link, EmphasisKind, MarkdownText    # nodes, enums, output
from simplibs.markdown import H1, BOLD, NOTE, BULLET_LIST, RULE                   # presets from root
from simplibs.markdown.presets import H1, BOLD, NOTE, BULLET_LIST, RULE
```

---

## 🧩 The `Markdown` Classes

Every node in this library inherits from `Markdown`. It defines the mandatory contract
(`to_lines`), the text forms built on it, the level tag and `+` composition out of the box.
`InlineMarkdown` is the shortcut for nodes that live inside a line and render as one string.

```python
class Markdown(ABC):
    node_level: NodeLevel                      # INLINE or BLOCK

    @abstractmethod
    def to_lines(self) -> tuple[str, ...]:
        """Return this node as lines, without line endings."""
        raise NotImplementedError

    def to_text(self) -> str: ...              # the lines joined with "\n"
    def __add__(self, other) -> "Markdown": ...    # -> InlineJoin or Document


class InlineMarkdown(Markdown):
    @abstractmethod
    def to_inline(self) -> str:
        """Return this node as one string that can stand inside a line."""
```

➡️ Full method-by-method reference: [README_MARKDOWN_CLASS](https://github.com/simplibs/simplibs-markdown/blob/main/docs/README_MARKDOWN_CLASS.md)

### What `+` returns

| Left         | Right        | Result                                          |
|--------------|--------------|-------------------------------------------------|
| inline node  | inline node  | `InlineJoin` — one line                         |
| `str`        | inline node  | `InlineJoin`; the string becomes escaped `Text` |
| block node   | anything     | `Document`                                      |
| `str`        | block node   | `Document`; the string becomes a `Paragraph`    |
| a node       | `5`, `None`… | `TypeError`                                     |

---

## 📖 Quick Reference

### 🔤 `inline/` — Nodes inside a line

| Class        | Description / Parameters                                                                       |
|--------------|------------------------------------------------------------------------------------------------|
| `Text`       | Plain text, every formatting character escaped (`value, escape`).                              |
| `Emphasis`   | Emphasis, strong, both and strike-through in one node (`inner, kind, marker`).                 |
| `InlineCode` | A code span; the delimiter and padding fit any content (`text`).                               |
| `Link`       | Six forms × link or image: inline, reference, collapsed, shortcut, autolink, bare URL (`text, dest, title, kind, image, label`). |
| `Entity`     | An HTML entity by name or by code point (`name` or `codepoint`).                               |
| `Math`       | An inline `$…$` or display `$$…$$` formula (`expr, display`).                                  |
| `Reference`  | Mention, team, issue, repository issue, commit, emoji (`kind, value`).                         |
| `LineBreak`  | A hard line break in three styles (`style`).                                                   |
| `InlineJoin` | Several inline nodes in a row — what `+` builds; always flat.                                  |

➡️ [README_MARKDOWN_INLINE](https://github.com/simplibs/simplibs-markdown/blob/main/docs/README_MARKDOWN_INLINE.md)

### 🧱 `blocks/` — Nodes that are lines of their own

| Class            | Description / Parameters                                                              |
|------------------|---------------------------------------------------------------------------------------|
| `Paragraph`      | Lines of inline content, optional hard-break style (`*lines, break_style`).           |
| `Heading`        | Levels 1–6 in three styles: ATX, closed ATX, setext (`inner, level, style`).          |
| `CodeBlock`      | Fenced (backtick or tilde) or indented; the fence fits the code (`code, info, fence, indented`). |
| `ThematicBreak`  | A horizontal rule (`char, length`).                                                   |
| `BlankLine`      | Explicit empty lines that replace the separator (`count`).                            |
| `LinkDefinition` | `[label]: destination "title"` (`label, dest, title`).                                |
| `Footnote`       | The marker in the text or the note itself (`label, *blocks, role`).                   |
| `Frontmatter`    | A YAML header between two `---` lines (`data`).                                       |
| `Html`           | A block, an inline tag or a comment with validated names (`tag, content, attrs, mode`). |

➡️ [README_MARKDOWN_BLOCKS](https://github.com/simplibs/simplibs-markdown/blob/main/docs/README_MARKDOWN_BLOCKS.md)

### 📦 `containers/` — Nodes that hold other blocks

| Class      | Description / Parameters                                                                 |
|------------|------------------------------------------------------------------------------------------|
| `Document` | Blocks separated by blank lines; the root of composition (`*blocks, gap, final_newline`). |
| `Quote`    | A block quote or a GitHub alert (`*blocks, alert`).                                      |
| `List`     | A bullet or an ordered list, tight or loose (`*items, ordered, marker, start, tight`).   |
| `ListItem` | One item: any blocks and an optional checkbox (`*blocks, checked`).                      |
| `Table`    | A GFM table with per-column alignment (`head, rows, align`).                             |

➡️ [README_MARKDOWN_CONTAINERS](https://github.com/simplibs/simplibs-markdown/blob/main/docs/README_MARKDOWN_CONTAINERS.md)

### 📤 `output/` — From a node to text and to a file

* `MarkdownText(node)` — the finished text of a node, rendered once: `text`, `lines`, `str()`,
  iteration, `len()` and `to_file(path)`.
* `to_file(source, path, *, overwrite=True)` — one call from a string, a node or a `MarkdownText` to
  a file; atomic, UTF-8, `"\n"` line endings.

➡️ [README_MARKDOWN_OUTPUT](https://github.com/simplibs/simplibs-markdown/blob/main/docs/README_MARKDOWN_OUTPUT.md)

### 🎁 `presets/` — Names for the things you write often

* **`alerts`**: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`
* **`code`**: `MERMAID`, `GEOJSON`, `TOPOJSON`, `STL`, `MATH_BLOCK`
* **`emphasis`**: `BOLD`, `ITALIC`, `BOLD_ITALIC`, `STRIKETHROUGH`
* **`headings`**: `H1`, `H2`, `H3`, `H4`, `H5`, `H6`
* **`html`**: `DETAILS`, `SUP`, `SUB`, `MARK`, `KBD`, `COMMENT`, `ANCHOR`
* **`links`**: `IMAGE`, `AUTOLINK`, `BARE_URL`
* **`lists`**: `BULLET_LIST`, `NUMBERED_LIST`, `TASK_ITEM`, `DONE_ITEM`
* **`references`**: `MENTION`, `ISSUE_REF`, `COMMIT_REF`, `EMOJI`, `COLOR_CHIP`
* **`spacing`**: `EMPTY_LINE`, `RULE`, `HARD_BREAK`

A preset only calls a node, so every check and every error comes from the node itself.

➡️ [README_MARKDOWN_PRESETS](https://github.com/simplibs/simplibs-markdown/blob/main/docs/README_MARKDOWN_PRESETS.md)

---

## ⚠️ Known Limitations

To keep the library lightweight and robust, a few design trade-offs apply in version 0.1.0:
* **Escaping is cautious:** Characters like `_`, `&`, or `$` are escaped broadly even when contextually safe (e.g., `snake_case` becomes `snake\_case`)[cite: 10].
* **Node equality:** Nodes do not implement `__eq__` (`==`); to compare two nodes, compare their `to_text()` or `to_lines()`[cite: 12].
* **Frontmatter serialization:** `Frontmatter` data is serialized once at construction time; subsequent modifications to the source dictionary are not reflected[cite: 13].
* **List merging:** Two consecutive lists with the exact same marker will merge in CommonMark renderers; use an explicit `COMMENT` or a different marker between them[cite: 11].

---

## ⚠️ Exceptions

Nodes raise structured [`simplibs.exception`](https://pypi.org/project/simplibs-exception/) cards
at construction time — a mistake never reaches the output. Every error name starts with
`MARKDOWN_`, and each is documented next to the node that raises it.

| Exception         | Raised when                                                                                         |
|-------------------|-----------------------------------------------------------------------------------------------------|
| `ParamError`      | An argument has the wrong type or an unusable value or combination (`Heading` level 7, a setext heading of level 3, a table row of the wrong width, a block inside bold text, `@some user` as a mention). |
| `ConversionError` | A `Frontmatter` value cannot be written as YAML (a set, `NaN`, a date, a key that is not a string). |

Writing a file (`to_file`) raises the errors of
[`simplibs-file`](https://pypi.org/project/simplibs-file/) — for example `AlreadyExistsError` when
`overwrite=False` and the file exists.

---

## 🔗 Related libraries

* **[`simplibs-exception`](https://pypi.org/project/simplibs-exception/)** — the structured exception cards behind every error here.
* **[`simplibs-file`](https://pypi.org/project/simplibs-file/)** — the atomic file write behind `to_file`.
* **[`simplibs-regex`](https://pypi.org/project/simplibs-regex/)** — the sister library: the same architecture (base class, containers, presets) for regular expressions.

---

## ☯️ About simplibs

All libraries in the **simplibs** (Simple Libraries) ecosystem share a common
engineering philosophy:

* **Dyslexia-friendly:**
We actively minimize cognitive load. Code is atomized into small, self-contained units,
files are named directly after the logical task they perform, and explanations describe
*why* something is designed, not just *what* it is.
* **Programmer's Zen:**
Nothing should be missing, and nothing should be superfluous. We value clean execution
paths and robust, understandable code architectures over rushed, messy feature sets.
* **Defensive Style:**
We actively anticipate edge cases and failure modes so that only safe operational paths
remain. Our code is built to degrade gracefully rather than crash unexpectedly.
* **Minimalism:**
Find the most direct path to the goal in as few operational steps as possible without
taking shortcuts on safety, readability, or completeness.
* **Code as Craft:**
Code should be pleasant to look at, readable at a glance, and evoke structural harmony.
We treat software engineering as a precision trade.

---

### 🤝 Contributing & Community

This is an **open-source project** built with love and care. We strongly believe in
community collaboration and welcome any feedback, bug reports, or feature ideas!

* **Want to contribute?** Feel free to open an Issue or submit a Pull Request.
* **Want to get in touch?** If you'd like to discuss the project further, collaborate,
  or just say hello, feel free to open a GitHub Issue or start a Discussion.

---

### 📝 License

This library is released under the **MIT License**. Build great things!

---

[▲ Back to Top](#-simplibs-markdown)
