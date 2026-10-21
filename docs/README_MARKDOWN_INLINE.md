# 🔤 `markdown/inline` — Nodes Inside a Line

The `inline` package holds every node that can stand **inside a line of text**: plain
text, emphasis, a code span, a link, an entity, a formula, a mention, a hard line
break — and the `InlineJoin` that `+` builds when several of them follow one another.
They are the leaves of the Markdown tree: a heading, a paragraph, a table cell or a list
item is made of them.

All of them extend [`InlineMarkdown`](README_MARKDOWN_CLASS.md#inlinemarkdown), so each one
writes a single method, `to_inline()`, and gets `to_text()` and `to_lines()` for free.
Several unify a whole syntax family the same way `Repeat` or `Group` do in
`simplibs-regex`: `Emphasis` covers four spellings (emphasis, strong, both,
strike-through), `Link` covers twelve (six forms × link/image), `Reference` covers six
kinds of automatic reference — each as one class plus a `Kind` enum.

```python
from ..base_class import InlineMarkdown

class Text(InlineMarkdown):
    ...
```

## A note on strings — what an "inline slot" accepts

Everywhere a node takes content (`Emphasis(inner)`, `Link(text)`, a heading, a table
cell) the same gate decides what is allowed, `as_inline`:

| You pass …                     | You get …                                              |
|--------------------------------|--------------------------------------------------------|
| a `str`                        | `Text(...)` — **escaped**, nothing in it is formatting |
| an inline node                 | the node itself                                        |
| a `list` / `tuple` of the above| an `InlineJoin` of them                                |
| a **block** node               | `ParamError` (`MARKDOWN_BLOCK_IN_INLINE`)              |
| anything else (`5`, `None`, …) | `ParamError` (`MARKDOWN_NODE_NOT_MARKDOWN`)            |

The consequence worth remembering: **a string is content, never Markdown.**
`Paragraph("a_b_c")` writes `a\_b\_c`, not emphasis. To write something that *is*
formatting, pass the node (`Emphasis("b")`), or — as the deliberate escape hatch —
`Text("...", escape=False)`.

---

## 🧭 Table of Contents

* [`Text`](#text)
* [`Emphasis`](#emphasis)
* [`InlineCode`](#inlinecode)
* [`Link`](#link)
* [`Entity`](#entity)
* [`Math`](#math)
* [`Reference`](#reference)
* [`LineBreak`](#linebreak)
* [`InlineJoin`](#inlinejoin)

[⬅️ Back to main README](../README.md#-inline--nodes-inside-a-line)

---

### `Text`

Plain text. Every character that Markdown could read as formatting is escaped, so the
text renders exactly as written. This is the node every string passed into the library
becomes.

**Parameters:**
* `value` (*str*): The text.
* `escape` (*bool*, default `True`): `False` writes the text as it is, so it can carry raw
  Markdown that was generated elsewhere. Nothing in the library sets it for you.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `value` is not a string.

**Example usage:**
```python
Text("2024. was a year").to_text()   # -> "2024\\. was a year"   (not a list)
Text("a_b_c *x*").to_text()          # -> "a\\_b\\_c \\*x\\*"
Text("# not a heading").to_text()    # -> "\\# not a heading"
Text("*raw*", escape=False).to_text()  # -> "*raw*"
```

**What is escaped** *(two kinds)*:

* Characters with a meaning **anywhere** in a line: `` \ ` * _ [ ] < > & ~ $ ``.
* Marks with a meaning **only at the start of a line** (after any indentation): `#`, `+`,
  `-`, `=`, and a number followed by `.` or `)` — the start of an ordered list.

```python
Text("a\n- b\n1) c").to_text()   # -> "a\n\\- b\n1\\) c"
```

**Under the hood** *(`to_inline`)*:
```python
def to_inline(self) -> str:
    return escape_text(self.value) if self.escape else self.value
```

> 💡 The list of always-escaped characters is deliberately cautious: `snake_case` becomes
> `snake\_case` and `a & b` becomes `a \& b`. Both render correctly; the extra backslashes
> only show in the source.

[▲ Back to top](#-table-of-contents)

---

### `Emphasis`

Emphasis, strong text, both, or strike-through around some content — one mechanism
(a marker repeated around the content) instead of four nodes.

**Parameters:**
* `inner` (*str | InlineMarkdown | list*): The content. See the note on
  [inline slots](#a-note-on-strings--what-an-inline-slot-accepts).
* `kind` (*EmphasisKind*, default `EmphasisKind.EM`): What kind of emphasis it is.
* `marker` (*EmphasisMarker | None*, default `None`): The character to wrap with. Defaults
  to `*`, or `~` for strike-through.

**`EmphasisKind` values:**

| Member      | Writes      | Marker repeated |
|-------------|-------------|-----------------|
| `EM`        | `*text*`    | 1×              |
| `STRONG`    | `**text**`  | 2×              |
| `STRONG_EM` | `***text***`| 3×              |
| `STRIKE`    | `~~text~~`  | 2× (`~`)        |

**`EmphasisMarker` values:** `ASTERISK` (`*`), `UNDERSCORE` (`_`), `TILDE` (`~`). The
value of the member **is** the character. `TILDE` belongs to `STRIKE` and only to it.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `kind` or `marker` has the wrong type.
* `ParamError` (`MARKDOWN_EMPHASIS_MARKER_KIND_MISMATCH`): a tilde with anything but
  `STRIKE`, or `STRIKE` with anything but a tilde.
* `ParamError` (`MARKDOWN_EMPHASIS_EMPTY_INNER`): the content has no visible text.
* `ParamError` (`MARKDOWN_BLOCK_IN_INLINE`): the content contains a block node.

**Example usage:**
```python
Emphasis("x").to_text()                              # -> "*x*"
Emphasis("x", EmphasisKind.STRONG).to_text()         # -> "**x**"
Emphasis("x", EmphasisKind.STRIKE).to_text()         # -> "~~x~~"
Emphasis("x", marker=EmphasisMarker.UNDERSCORE).to_text()   # -> "_x_"

Emphasis("x", EmphasisKind.STRIKE, EmphasisMarker.ASTERISK)
# -> raises: the marker ASTERISK cannot express STRIKE
```

**Whitespace at the edges moves outside.** `** text **` is not strong text in CommonMark,
so the leading and trailing whitespace of the content is written *outside* the markers:

```python
Emphasis(" x ", EmphasisKind.STRONG).to_text()   # -> " **x** "
```

**Under the hood** *(`to_inline`)*:
```python
def to_inline(self) -> str:
    text = self.inner.to_text()
    core = text.strip()
    lead = text[: len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]

    mark = self.marker.value * EMPHASIS_REPEAT[self.kind]
    return f"{lead}{mark}{core}{mark}{trail}"
```

`EMPHASIS_REPEAT` is a read-only table (`EM: 1`, `STRONG: 2`, `STRONG_EM: 3`,
`STRIKE: 2`) — the only thing that differs between the four kinds.

> ⚠️ An underscore marker does not work **inside a word** (`snake_case` stays text). The
> node sees only its own content, not the text around it, so it cannot warn about that.

[▲ Back to top](#-table-of-contents)

---

### `InlineCode`

A code span. The backticks around it are chosen to fit its content, so any text can be
code and nothing inside needs escaping.

**Parameters:**
* `text` (*str*): The code. Line breaks become spaces — a code span lives on one line,
  which also keeps table cells and headings valid.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `text` is not a string.
* `ParamError` (`MARKDOWN_INLINE_CODE_EMPTY`): `text` has no visible content.

**Example usage:**
```python
InlineCode("x = 1").to_text()     # -> "`x = 1`"
InlineCode("a`b").to_text()       # -> "``a`b``"
InlineCode("`a`").to_text()       # -> "`` `a` ``"
InlineCode("a\nb").to_text()      # -> "`a b`"
```

**How the delimiter is chosen.** The delimiter is one backtick longer than the longest run
of backticks inside the code. A space is added on both sides when the code starts or ends
with a backtick, or when it starts **and** ends with a space — CommonMark strips one space
from each side, so the padding is what keeps the original spaces alive.

**Under the hood** *(`choose_code_delimiter`)*:
```python
longest = max((len(run) for run in re.findall(r"`+", code)), default=0)
delimiter = "`" * (longest + 1)

needs_padding = (
    code.startswith("`")
    or code.endswith("`")
    or (code.startswith(" ") and code.endswith(" ") and code.strip(" ") != "")
)
return delimiter, (f" {code} " if needs_padding else code)
```

```python
InlineCode(" a ").to_text()       # -> "`  a  `"   (both spaces survive)
InlineCode("a``b`c").to_text()    # -> "```a``b`c```"
```

[▲ Back to top](#-table-of-contents)

---

### `Link`

A link or an image, in any of six forms — one node with a `kind` and an `image` flag
instead of twelve classes.

**Parameters:**
* `text` (*str | InlineMarkdown | list | None*, default `None`): The link text (or the alt
  text of an image). Not allowed for autolinks and bare URLs.
* `dest` (*str | None*, default `None`): The destination — a URL or a path.
* `title` (*str | None*, default `None`): An optional title (`INLINE` links only).
* `kind` (*LinkKind*, default `LinkKind.INLINE`): The syntax form.
* `image` (*bool*, default `False`): `True` writes an image (`!`) instead of a link.
* `label` (*str | None*, default `None`): The label of a
  [`LinkDefinition`](README_MARKDOWN_BLOCKS.md); required for `REFERENCE`.

**`LinkKind` values — and what each one needs:**

| Member      | Writes                         | Needs                       |
|-------------|--------------------------------|-----------------------------|
| `INLINE`    | `[text](dest "title")`         | `text`, `dest`              |
| `REFERENCE` | `[text][label]`                | `text`, `label`             |
| `COLLAPSED` | `[text][]`                     | `text` (the text is the label) |
| `SHORTCUT`  | `[text]`                       | `text` (the text is the label) |
| `AUTOLINK`  | `<dest>`                       | `dest` only                 |
| `BARE`      | `dest`, as it is               | `dest` only                 |

A parameter a kind does not use is ignored (`Link("a", dest="x", kind=LinkKind.SHORTCUT)`
writes `[a]`).

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `kind` is not a `LinkKind`; `dest`,
  `title` or `label` is not a string; or `text` is missing where it is needed.
* `ParamError` (`MARKDOWN_LINK_EMPTY_DESTINATION`): an `INLINE`, `AUTOLINK` or `BARE`
  link has no destination.
* `ParamError` (`MARKDOWN_LINK_KIND_REQUIRES_LABEL`): `REFERENCE` without a `label`.
* `ParamError` (`MARKDOWN_LINK_AUTOLINK_WITH_TEXT`): `text` given to an `AUTOLINK` or `BARE`.
* `ParamError` (`MARKDOWN_LINK_IMAGE_UNSUPPORTED_KIND`): `image=True` with an `AUTOLINK` or
  `BARE` — Markdown has no image form for them.

**Example usage:**
```python
Link("docs", "https://example.com").to_text()            # -> "[docs](https://example.com)"
Link("docs", "https://example.com", "Title").to_text()   # -> '[docs](https://example.com "Title")'
Link("alt", "img.png", image=True).to_text()             # -> "![alt](img.png)"

Link("docs", kind=LinkKind.REFERENCE, label="Foo  Bar").to_text()   # -> "[docs][Foo Bar]"
Link("docs", kind=LinkKind.COLLAPSED).to_text()          # -> "[docs][]"
Link(dest="https://example.com", kind=LinkKind.AUTOLINK).to_text() # -> "<https://example.com>"
Link(["see ", Emphasis("docs")], "x").to_text()          # -> "[see *docs*](x)"
```

**A destination that does not end early.** A plain destination is kept as it is, so
ordinary URLs stay readable. One with a space, a control character or unbalanced
parentheses is written between angle brackets; balanced parentheses stay plain.

```python
Link("a", "my file.pdf").to_text()                        # -> "[a](<my file.pdf>)"
Link("a", "https://en.wikipedia.org/wiki/A_(b)").to_text()   # -> "[a](https://en.wikipedia.org/wiki/A_(b))"
```

**A title in the right quotes.** Double quotes first; single quotes when the title
contains a double quote; escapes only when it contains both.

```python
Link("a", "x", 'say "hi"').to_text()    # -> "[a](x 'say \"hi\"')"
```

**Under the hood** *(`to_inline`)*:
```python
def to_inline(self) -> str:
    if self.kind is LinkKind.AUTOLINK:
        return f"<{self.dest}>"
    if self.kind is LinkKind.BARE:
        return self.dest

    bang = "!" if self.image else ""
    text = self.text.to_text()

    if self.kind is LinkKind.INLINE:
        title = f" {escape_link_title(self.title)}" if self.title else ""
        return f"{bang}[{text}]({escape_link_destination(self.dest)}{title})"
    if self.kind is LinkKind.REFERENCE:
        return f"{bang}[{text}][{normalize_label(self.label)}]"
    if self.kind is LinkKind.COLLAPSED:
        return f"{bang}[{text}][]"
    return f"{bang}[{text}]"
```

`normalize_label` collapses every run of whitespace into one space — CommonMark matches
`[Foo   Bar]` with `[foo bar]`, and a link and its definition write the label through the
same function, so they always agree. The same three helpers
(`escape_link_destination`, `escape_link_title`, `normalize_label`) are shared with
`LinkDefinition` in `blocks`.

[▲ Back to top](#-table-of-contents)

---

### `Entity`

An HTML entity, written by name (`&copy;`) or by code point (`&#169;`) — for characters
that are hard to type or invisible (`&nbsp;`, `&#8203;`).

**Parameters:**
* `name` (*str | None*, default `None`): The entity name, with or without `&` and `;`.
* `codepoint` (*int | None*, default `None`): The Unicode code point (`0` to `0x10FFFF`).
  A `bool` is refused.

Exactly **one** of the two must be given.

**Raises:**
* `ParamError` (`MARKDOWN_ENTITY_NAME_XOR_CODEPOINT`): both or neither were given.
* `ParamError` (`MARKDOWN_ENTITY_UNKNOWN_NAME`): the name is not in Python's HTML5 entity list.
* `ParamError` (`MARKDOWN_ENTITY_CODEPOINT_OUT_OF_RANGE`): not an integer inside the Unicode range.
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `name` is not a string.

**Example usage:**
```python
Entity("nbsp").to_text()           # -> "&nbsp;"
Entity("&copy;").to_text()         # -> "&copy;"
Entity(codepoint=169).to_text()    # -> "&#169;"

Entity("nbsq")                     # -> raises: not a known HTML entity
```

The name is checked against the list, so a typo is an error at construction — not a
literal `&nbsq;` in the finished document.

**Why not `Text`?** `Text` escapes `&`, so an entity passed as a string would be shown
as text instead of being rendered.

**Under the hood** *(`to_inline`)*:
```python
def to_inline(self) -> str:
    return f"&{self.name};" if self.name is not None else f"&#{self.codepoint};"
```

[▲ Back to top](#-table-of-contents)

---

### `Math`

A math expression in `$...$` (inline) or `$$...$$` (display).

**Parameters:**
* `expr` (*str*): The expression, written in LaTeX. Surrounding whitespace is stripped.
* `display` (*bool*, default `False`): `True` writes the display form.

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `expr` is not a string.
* `ParamError` (`MARKDOWN_MATH_EMPTY_EXPRESSION`): `expr` has no visible content.

**Example usage:**
```python
Math("a^2+b^2=c^2").to_text()            # -> "$a^2+b^2=c^2$"
Math("E=mc^2", display=True).to_text()   # -> "$$E=mc^2$$"
```

**Why not `Text`?** `Text` escapes `$`, so an expression written as a string would never
become math. This node writes the dollars on purpose.

**Under the hood** *(`to_inline`)*:
```python
def to_inline(self) -> str:
    mark = "$$" if self.display else "$"
    return f"{mark}{self.expr}{mark}"
```

> ⚠️ The expression is written as given. A `$` **inside** it is not escaped and can end
> the math early; GitHub expects `\$` there.

[▲ Back to top](#-table-of-contents)

---

### `Reference`

An automatic reference — a mention, an issue, a commit, an emoji. These are plain text in
CommonMark and links on GitHub; the node checks the **shape** of the value, so
`@some user` is an error and not a mention that silently never links.

**Parameters:**
* `kind` (*ReferenceKind*): What is being referenced.
* `value` (*str | int*): The value **without** the leading mark (`"octocat"`, `12`).

**`ReferenceKind` values:**

| Member       | Valid value                                       | Writes          |
|--------------|---------------------------------------------------|-----------------|
| `MENTION`    | a username: letters, digits, `-`, up to 39 chars  | `@octocat`      |
| `TEAM`       | `org/team-name`                                   | `@org/team-a`   |
| `ISSUE`      | a number                                          | `#12`           |
| `REPO_ISSUE` | `owner/repo#12`                                   | `owner/repo#12` |
| `COMMIT`     | a lowercase hex hash, 7 to 40 characters          | `a1b2c3d`       |
| `EMOJI`      | a lowercase name without colons                   | `:tada:`        |

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `kind` is not a `ReferenceKind`.
* `ParamError` (`MARKDOWN_REFERENCE_INVALID_VALUE`): `value` does not fit the kind — the
  error describes what a valid value looks like.

**Example usage:**
```python
Reference(ReferenceKind.MENTION, "octocat").to_text()          # -> "@octocat"
Reference(ReferenceKind.ISSUE, 12).to_text()                   # -> "#12"
Reference(ReferenceKind.REPO_ISSUE, "owner/repo#12").to_text() # -> "owner/repo#12"
Reference(ReferenceKind.EMOJI, "tada").to_text()               # -> ":tada:"

Reference(ReferenceKind.MENTION, "some user")   # -> raises: does not fit a mention
```

**Why not `Text`?** `Text` escapes a leading `#`, so `#12` written as a string would
become `\#12` and never link.

**Under the hood.** Everything that differs between the six kinds sits in **one** table,
`REFERENCE_FORMS` — a pattern, a template and the sentence that explains the pattern to
a user whose value was rejected. The node itself has no branch per kind:

```python
REFERENCE_FORMS[ReferenceKind.ISSUE] = (
    re.compile(r"\d+"),            # the shape of a valid value
    "#{}",                         # how it is written
    "A number, e.g. 12.",          # what the error tells the user
)

def to_inline(self) -> str:
    _, template, _ = REFERENCE_FORMS[self.kind]
    return template.format(self.value)
```

Adding a kind is one table entry and one enum member.

> 💡 The patterns check the shape, not whether the user, issue or commit exists.

[▲ Back to top](#-table-of-contents)

---

### `LineBreak`

A hard line break inside a paragraph. A single newline in a paragraph is just a space;
a hard break needs one of three spellings, and the author chooses it on purpose.

**Parameters:**
* `style` (*LineBreakStyle*, default `LineBreakStyle.SPACES`): How the break is written.

**`LineBreakStyle` values** *(shared with `blocks`, so it lives in `_common/enums`)*:

| Member      | Writes                    | Notes                                                 |
|-------------|---------------------------|-------------------------------------------------------|
| `SPACES`    | two spaces + newline      | invisible in an editor, often removed by one          |
| `BACKSLASH` | `\` + newline             | survives editors                                      |
| `HTML`      | `<br>`                    | the only one that stays **inside** the line — usable in a table cell |

**Raises:**
* `ParamError` (`MARKDOWN_PARAM_INVALID_TYPE`): `style` is not a `LineBreakStyle`.

**Example usage:**
```python
LineBreak().to_text()                          # -> "  \n"
LineBreak(LineBreakStyle.BACKSLASH).to_text()  # -> "\\\n"
LineBreak(LineBreakStyle.HTML).to_text()       # -> "<br>"

("a" + LineBreak() + "b").to_lines()           # -> ("a  ", "b")
```

**Under the hood.** The exact text of each style, newline included, sits in one read-only
table, so `to_inline` has no branches:

```python
LINE_BREAKS = MappingProxyType({
    LineBreakStyle.SPACES:    "  \n",
    LineBreakStyle.BACKSLASH: "\\\n",
    LineBreakStyle.HTML:      "<br>",
})

def to_inline(self) -> str:
    return LINE_BREAKS[self.style]
```

[▲ Back to top](#-table-of-contents)

---

### `InlineJoin`

Several inline nodes written one after another — what `+` gives for two inline operands
(see [`__add__`](README_MARKDOWN_CLASS.md#__add__--__radd__)). It can also be built
directly.

**Parameters:**
* `*parts` (*str | InlineMarkdown | list*): Strings, inline nodes or lists of them. Every
  part goes through the [inline gate](#a-note-on-strings--what-an-inline-slot-accepts).

**Raises:**
* `ParamError` (`MARKDOWN_BLOCK_IN_INLINE`): a part is a block node.
* `ParamError` (`MARKDOWN_NODE_NOT_MARKDOWN`): a part is not content at all.

**Example usage:**
```python
InlineJoin("Viz ", Link("docs", "x"), ".").to_text()   # -> "Viz [docs](x)."
"Viz " + Link("docs", "x") + "."                        # equivalent, via the + operator

InlineJoin(Paragraph("a"))    # -> raises: a block cannot stand inside a line
```

**Always flat.** A nested join gives up its own parts, so `(a + b) + c` and `a + (b + c)`
both end up as one sequence of three parts:

```python
InlineJoin(InlineJoin("a", "b"), "c").parts   # -> (Text('a'), Text('b'), Text('c'))
```

**Under the hood:**
```python
def __init__(self, *parts) -> None:
    flat = []
    for part in parts:
        node = as_inline(part)
        flat.extend(node.parts if isinstance(node, InlineJoin) else (node,))
    self.parts = tuple(flat)

def to_inline(self) -> str:
    return "".join(part.to_text() for part in self.parts)
```

The parts are written without any separator — spacing is the author's business, which is
why `"Viz "` carries its own space.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-inline--nodes-inside-a-line)
