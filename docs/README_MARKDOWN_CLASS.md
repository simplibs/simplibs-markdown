# 🧱 `Markdown` & `InlineMarkdown` — The Two Bases of Every Node

`Markdown` is the single foundation every node in `simplibs-markdown` is built on — from
the smallest inline piece (`Text`, `Emphasis`) to a whole composed document
(`Document(Heading(...), Paragraph(...), Table(...))`). It does not write any concrete
Markdown construct itself; instead it provides four things every node needs:

1. A minimal, mandatory contract every concrete node must fulfill (`to_lines`).
2. A second way to read the same result (`to_text`, `str()`, `repr()`), built purely on
   top of that one method.
3. A level tag (`node_level`) that tells every container whether a node lives *inside a
   line* or *as a block of its own* — the one value `+`, `as_inline` and the containers
   decide by.
4. Operator-based composition (`+`) that lets any two nodes — or a node and a plain
   string — combine into a new node, without either side needing to know anything about
   the other.

`InlineMarkdown` is a thin shortcut on top of it for the nodes that live inside a line
and render as one string.

```python
from abc import ABC, abstractmethod
from .enums import NodeLevel

class Markdown(ABC):
    ...

class InlineMarkdown(Markdown):
    ...
```

## A note on why `Markdown` is abstract

`Markdown` can never be instantiated directly — `to_lines` is declared with
`@abstractmethod` and carries no implementation of its own. This is deliberate:
`Markdown` only defines *what every node must be able to produce* (its own lines), never
*how* — that answer is always specific to the concrete node (`Heading`, `Table`,
`Link`, ...). Everything else the class provides (`to_text`, `__str__`, `__repr__`, the
operators) is built on top of that one abstract method, so any concrete node that
implements it correctly gets the rest of this interface for free.

```python
Markdown()
# -> TypeError: Can't instantiate abstract class Markdown without an implementation
#    for abstract method 'to_lines'
```

---

## 🧭 Table of Contents

* [`to_lines`](#to_lines)
* [`to_text`](#to_text)
* [`node_level`](#node_level)
* [`__add__` / `__radd__`](#__add__--__radd__)
* [`__str__` and `__repr__`](#__str__-and-__repr__)
* [`InlineMarkdown`](#inlinemarkdown)
* [`to_inline`](#to_inline)
* [The `NodeLevel` enum](#the-nodelevel-enum)

[⬅️ Back to main README](../README.md#-the-markdown-classes)

---

### `to_lines`

**Abstract.** The single true source of "what does this node look like in a Markdown
file" for every node in the library. Every other method that produces text — `to_text`,
`str()`, `repr()`, and every container's own `to_lines` (`Quote`, `List`, `Document`,
...) — ultimately reduces to calling this method somewhere.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `tuple[str, ...]`: The node's lines, **without line endings**. Always a tuple, never a
  single string — a tuple of lines is what can be nested safely: a `Quote` prefixes every
  line of the block inside it with `> `, a `List` indents every line of an item, and
  neither needs to parse text to do so.

**Example usage:**
```python
Paragraph("a", "b").to_lines()      # -> ("a", "b")
Text("a_b").to_lines()              # -> ("a\\_b",)
```

**Under the hood** *(the abstract declaration)*:
```python
@abstractmethod
def to_lines(self) -> tuple[str, ...]:
    """Render the node as lines without line endings."""
    raise NotImplementedError
```

> 💡 Lines are the single source of truth on purpose. Joining lines into text is trivial;
> splitting text back into lines safely is not — a text can contain a line break that
> belongs to a code block, a table cell, or an escape.

[▲ Back to top](#-table-of-contents)

---

### `to_text`

The same result as one string — the lines joined with `\n`. This is what `str(node)`
returns and what `MarkdownText` writes into a file.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `str`: The node's lines joined by `\n`. No trailing newline — a `Document` adds the
  final one itself (see [`README_MARKDOWN_CONTAINERS`](README_MARKDOWN_CONTAINERS.md)).

**Example usage:**
```python
Paragraph("a", "b").to_text()    # -> "a\nb"
```

**Under the hood:**
```python
def to_text(self) -> str:
    return "\n".join(self.to_lines())
```

Concrete nodes normally never override it. The one deliberate exception is
[`InlineMarkdown`](#inlinemarkdown), where the string already exists and going through
the lines would only split and join it again.

[▲ Back to top](#-table-of-contents)

---

### `node_level`

Usually a **class attribute**, not a method: a concrete node sets it once, to a
[`NodeLevel`](#the-nodelevel-enum) member, and nothing ever changes it afterwards.
The exceptions are `Footnote` (by `role`) and `Html` (by `mode`), which can stand either
inside a line or as a block; for them it is a read-only property.

**Type:**
* `NodeLevel`: `NodeLevel.INLINE` for nodes that stand inside a line of text, or
  `NodeLevel.BLOCK` for nodes that are lines of their own.

**Example usage:**
```python
Text("a").node_level        # -> NodeLevel.INLINE
Link("docs", "https://example.com").node_level   # -> NodeLevel.INLINE
Paragraph("a").node_level   # -> NodeLevel.BLOCK
Document(Paragraph("a")).node_level   # -> NodeLevel.BLOCK
```

It is the one value that `+`, `as_inline` and the containers use to decide what may stand
where — a heading inside bold text, or a table inside a link, is refused when the node is
built, not discovered later in a broken output.

> 💡 The attribute is called `node_level`, not `level`, because `Heading.level` already
> means "the number of the heading" (`#` vs `###`).

[▲ Back to top](#-table-of-contents)

---

### `__add__` / `__radd__`

Composes this node with another node — or with a plain string — via `+`. The method
behind every `Heading(...) + Paragraph(...)` and every `"See " + Link(...) + "."`.

**Parameters:**
* `other` (*Markdown | str*): The right-hand (or, via `__radd__`, left-hand) operand.

**Returns:**
* `InlineJoin | Document`, or `NotImplemented` if `other` is neither a node nor a string.

What the result is depends only on the levels of the two operands:

| Left            | Right           | Result                                          |
|-----------------|-----------------|-------------------------------------------------|
| inline node     | inline node     | `InlineJoin` — one line                         |
| `str`           | inline node     | `InlineJoin`; the string becomes escaped `Text` |
| inline node     | `str`           | `InlineJoin`; the string becomes escaped `Text` |
| block node      | anything        | `Document`                                      |
| `str`           | block node      | `Document`; the string becomes a `Paragraph`    |
| block node      | `str`           | `Document`; the string becomes a `Paragraph`    |
| a node          | `5`, `None`, …  | `NotImplemented` → Python raises `TypeError`    |

**Example usage:**
```python
line = "See " + Emphasis("this") + "."
type(line).__name__       # -> "InlineJoin"
line.to_text()            # -> "See *this*."

doc = H1("Title") + "text"
type(doc).__name__        # -> "Document"
doc.to_text()             # -> "# Title\n\ntext\n"

H1("Title") + 5           # -> TypeError: unsupported operand type(s) for +: ...
```

`__radd__` exists for exactly one case: a string on the left, because `str.__add__`
refuses a node and Python then asks the node. It uses the same rules, with the operands
swapped, so `"text" + H1("Title")` works just as `H1("Title") + "text"` does.

**Under the hood:**
```python
def __add__(self, other: Any) -> Any:
    return add_nodes(self, other)

def __radd__(self, other: Any) -> Any:
    return add_nodes(other, self)
```

Both methods hand the operands to **one** helper, `add_nodes` (in `_common/helpers`). That
is why `base_class` names no concrete node: the helper creates `InlineJoin`, `Document`,
`Text` and `Paragraph` with imports placed inside the function, so the base class stays
below every node in the import graph.

```python
def add_nodes(left, right):
    # A string takes the level of the node on the other side
    if isinstance(left, str) and isinstance(right, Markdown):
        left = Text(left) if right.node_level is NodeLevel.INLINE else Paragraph(left)
    elif isinstance(right, str) and isinstance(left, Markdown):
        right = Text(right) if left.node_level is NodeLevel.INLINE else Paragraph(right)

    # Two operands that are not both nodes are not ours to compose
    if not (isinstance(left, Markdown) and isinstance(right, Markdown)):
        return NotImplemented

    # Inline with inline stays one line; anything with a block becomes a document
    if left.node_level is NodeLevel.INLINE and right.node_level is NodeLevel.INLINE:
        return InlineJoin(left, right)
    return Document(left, right)
```

> 💡 `NotImplemented` is **returned**, not raised. That gives Python the chance to try the
> other operand's `__radd__` and, if nobody accepts the pair, to raise its own, familiar
> `TypeError`.

[▲ Back to top](#-table-of-contents)

---

### `__str__` and `__repr__`

Two debugging conveniences, both built on `to_text`. Nodes have no `==`; to compare
two nodes, compare their `to_text()`.

**Returns:**
* `__str__` → `str`: exactly `to_text()`.
* `__repr__` → `str`: `ClassName('<to_text()>')`.

**Example usage:**
```python
str(Paragraph("x"))           # -> "x"
repr(Paragraph("x"))          # -> "Paragraph('x')"
repr("Viz " + Emphasis("zde") + ".")   # -> "InlineJoin('Viz *zde*.')"
```

**Under the hood:**
```python
def __str__(self) -> str:
    return self.to_text()

def __repr__(self) -> str:
    return f"{type(self).__name__}({self.to_text()!r})"
```

`repr` shows the **rendered Markdown**, not the constructor arguments — in a debugger or a
test failure the first thing you want to see is what the node would write.

[▲ Back to top](#-table-of-contents)

---

### `InlineMarkdown`

The shortcut base for every node that lives **inside a line** — `Text`, `Emphasis`,
`InlineCode`, `Link`, `Entity`, `Math`, `Reference`, `LineBreak`, `InlineJoin`. These nodes
only differ in how they write themselves, so each implements one method, `to_inline()`, and
gets `to_text()` and `to_lines()` for free.

**What it sets:**
* `node_level = NodeLevel.INLINE` — so a subclass never has to repeat it.

**What it provides:**
* `to_text()` — returns `to_inline()` as it is.
* `to_lines()` — splits `to_inline()` on `\n`, so only text with a line break inside gives
  more than one line.

**Example usage:**
```python
Text("a_b").to_text()            # -> "a\\_b"
Text("a_b").to_lines()           # -> ("a\\_b",)
Text("a\nb").to_lines()          # -> ("a", "b")
```

**Under the hood:**
```python
class InlineMarkdown(Markdown):
    __slots__ = ()
    node_level = NodeLevel.INLINE

    @abstractmethod
    def to_inline(self) -> str: ...

    def to_text(self) -> str:
        return self.to_inline()

    def to_lines(self) -> tuple[str, ...]:
        return tuple(self.to_inline().split("\n"))
```

`to_text` does **not** go through the lines here: the base version would split the string
into lines only to join them again, so an inline node returns the string it already has.

[▲ Back to top](#-table-of-contents)

---

### `to_inline`

**Abstract** (on `InlineMarkdown` only). The one method an inline node has to write.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `str`: The node as a string that can stand inside a line — for example `"*zde*"` for
  `Emphasis("zde")`, or `"a\\_b"` for `Text("a_b")`.

**Under the hood** *(as implemented by a concrete node, e.g. `InlineJoin`)*:
```python
def to_inline(self) -> str:
    return "".join(part.to_text() for part in self.parts)
```

Block nodes do not have this method — they implement `to_lines` directly, because a block
is by nature more than one string.

[▲ Back to top](#-table-of-contents)

---

## The `NodeLevel` enum

Two members, used exclusively as the value of `node_level`:

| Member   | Value      | Meaning                                                                    | Examples                                  |
|----------|------------|----------------------------------------------------------------------------|-------------------------------------------|
| `INLINE` | `"inline"` | Lives inside a line of text; `+` joins it with other inline nodes.         | `Text`, `Emphasis`, `Link`, `InlineCode`  |
| `BLOCK`  | `"block"`  | Is a line (or lines) of its own; separated from its neighbours by a blank line. | `Heading`, `Paragraph`, `List`, `Table`, `Document` |

**Example usage:**
```python
from simplibs.markdown import NodeLevel

Text("a").node_level is NodeLevel.INLINE   # -> True
```

It does here the job `Precedence` does in `simplibs-regex`: one tag that lets the
containers refuse a nonsense combination at construction time instead of producing wrong
output.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-the-markdown-classes)
