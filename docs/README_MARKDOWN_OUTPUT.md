# 📤 `markdown/output` — From a Node to Text and to a File

The `output` package is the **last layer**. Everything before it describes a document;
this is where the description becomes a result: a finished text you can print, iterate or
count — or a file on disk.

It holds two things: the `MarkdownText` class (the finished text of a node) and the
`to_file` function (one call from a string, a node or a finished text to a file).

```python
from simplibs.markdown import Heading, MarkdownText, to_file

doc = Heading("Title") + "Some text."

print(MarkdownText(doc))          # the text, ending with a newline
to_file(doc, "out/notes.md")      # the same, straight into a file
```

## A note on the one dependency

This package is the **only** place in `simplibs-markdown` that uses another `simplibs`
library: [`simplibs-file`](https://github.com/simplibs/simplibs-file) (`write_text`). The
writing itself — the draft that replaces the target in one atomic step, the folder created
when missing, the structured error cards — is entirely `write_text`'s business; nothing
here re-implements it. Because it is a plain function behind a plain call, a failed write
reports the file and what the OS said, exactly as everywhere else in `simplibs`.

Defaults worth knowing, inherited from `write_text`: **UTF-8 without a BOM** and **`"\n"`
line endings** on every platform — the same bytes on every machine.

---

## 🧭 Table of Contents

* [`MarkdownText`](#markdowntext)
* [`to_file`](#to_file)

[⬅️ Back to main README](../README.md#-output--from-a-node-to-text-and-to-a-file)

---

### `MarkdownText`

The finished Markdown text of a node. A node is a *description*; this is the *result*. The
text is rendered **once** and kept, so `str()`, iteration and `len()` never render again.

**Parameters:**
* `node` (*Markdown*): Any node. A `Document` is used as it is; anything else is wrapped in
  one (so a single `Heading`, a `Table` or even an inline node works).

**Attributes:**
* `document` (*Document*): The document that was rendered.
* `text` (*str*): The whole text, ending with a newline (unless the document has
  `final_newline=False`).
* `lines` (*tuple[str, ...]*): The lines of the text, without line endings.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `node` is not a Markdown node — a plain string
  is **not** accepted here (it is already text; use [`to_file`](#to_file) to write one).

**Example usage:**
```python
m = MarkdownText(Heading("T") + "text")

str(m)       # -> "# T\n\ntext\n"
len(m)       # -> 3
list(m)      # -> ["# T", "", "text"]
m.lines      # -> ("# T", "", "text")

str(MarkdownText(Heading("T")))                       # -> "# T\n"   (wrapped in a Document)
str(MarkdownText(Document("a", final_newline=False))) # -> "a"
str(MarkdownText(Document("a", "b", gap=2)))          # -> "a\n\n\nb\n"
```

A `Document` brings its **own** `gap` and `final_newline` into the result — this is the one place
where they take effect (see [`Document`](README_MARKDOWN_CONTAINERS.md#document)). A node that is
not a document is wrapped in a document with the defaults (`gap=1`, `final_newline=True`).

**Methods:**

| Method                 | Returns       | Description                                      |
|------------------------|---------------|--------------------------------------------------|
| `__str__()`            | `str`         | The text — so `print(m)` writes the document.    |
| `__iter__()`           | iterator      | Iterates the **lines**.                          |
| `__len__()`            | `int`         | The number of lines.                             |
| `to_file(path, ...)`   | `Path`        | Writes the text to a file — see below.           |

#### `to_file` (method)

Writes the finished text to a file.

**Parameters:**
* `path` (*str | Path*): The target file. Its folder is created when missing.
* `overwrite` (*bool*, keyword-only, default `True`): `False` raises instead of replacing an
  existing file.
* `**write_options`: Passed on to `write_text` (`encoding`, `errors`, `newline`, `use_draft`,
  `sync`, ...) — see
  [`README_FILE_WRITE`](https://github.com/simplibs/simplibs-file/blob/main/docs/logic/README_FILE_WRITE.md).

**Returns:**
* `Path`: The normalized path of the written file (so the call chains).

**Raises:**
* The errors of `write_text` — for example `AlreadyExistsError` when `overwrite=False` and the
  file exists.

**Example usage:**
```python
m.to_file("out/notes.md")                   # writes "# T\n\ntext\n", the folder "out" is created
m.to_file("out/notes.md", overwrite=False)  # -> raises: the file already exists
m.to_file("out/notes.md", newline="\r\n")   # explicit choice of line endings
```

**Under the hood:**
```python
def __init__(self, node: Markdown) -> None:
    if not isinstance(node, Markdown):
        raise_param_invalid_type_error("node", node, Markdown)

    document = node if isinstance(node, Document) else Document(node)

    self.document = document
    self.text = document.to_text()
    self.lines = document.to_lines()

def to_file(self, path, *, overwrite: bool = True, **write_options):
    return write_text(path, self.text, overwrite=overwrite, **write_options)
```

**Why a class and not a plain string?** Lines are as useful as the text (diffs, tests,
counting), and the file write belongs to the *finished* text, not to every node.

> 💡 The text is rendered at construction. Changing a node afterwards does not change an
> existing `MarkdownText` — build a new one.

[▲ Back to top](#-table-of-contents)

---

### `to_file`

One call from **anything** to a file.

**Parameters:**
* `source` (*str | Markdown | MarkdownText*): What to write — see the table below.
* `path` (*str | Path*): The target file.
* `overwrite` (*bool*, keyword-only, default `True`): `False` raises instead of replacing an
  existing file.
* `**write_options`: Passed on to `write_text` (`encoding`, `newline`, ...).

**What `source` can be:**

| `source`           | What happens                                                         |
|--------------------|----------------------------------------------------------------------|
| a `str`            | Written **as it is** — it already is the text (Markdown generated elsewhere). |
| a node             | Rendered through [`MarkdownText`](#markdowntext), then written.      |
| a `MarkdownText`   | Written as it is.                                                    |

**Returns:**
* `Path`: The normalized path of the written file.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `source` is not a string, a node or a
  `MarkdownText` (`5`, a `list`, ...).
* The errors of `write_text` — for example `AlreadyExistsError` when `overwrite=False` and the
  file exists.

**Example usage:**
```python
to_file(Heading("Title") + "text", "out/notes.md")   # a node
to_file("# raw\n", "out/raw.md")                     # a string that already is Markdown
to_file(MarkdownText(doc), "out/doc.md")             # a finished text

to_file(doc, "out/doc.md", overwrite=False)          # an error card if the file exists
to_file(5, "out/x.md")                               # -> raises: not a string, node or MarkdownText
```

A string is written **unchanged**, so a trailing newline is yours to add — only a node (through
its `Document`) gets the final newline for free.

**Under the hood:**
```python
def to_file(source, path, *, overwrite: bool = True, **write_options):
    # A string is already the text
    if isinstance(source, str):
        return write_text(path, source, overwrite=overwrite, **write_options)

    # A node is rendered first; anything else fails there with a clear card
    if not isinstance(source, MarkdownText):
        source = MarkdownText(source)

    # The finished text writes itself
    return source.to_file(path, overwrite=overwrite, **write_options)
```

`to_file` imports `MarkdownText`, and `MarkdownText.to_file` calls `write_text` itself rather than
importing `to_file` back — one direction only, so the two files never import each other.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-output--from-a-node-to-text-and-to-a-file)
