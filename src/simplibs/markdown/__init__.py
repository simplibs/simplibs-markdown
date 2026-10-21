from ._common.enums import LineBreakStyle
from .base_class import InlineMarkdown, Markdown
from .base_class.enums import NodeLevel
from .blocks import (
    BlankLine,
    CodeBlock,
    Footnote,
    Frontmatter,
    Heading,
    Html,
    LinkDefinition,
    Paragraph,
    ThematicBreak,
)
from .blocks.enums import BreakChar, FenceChar, FootnoteRole, HeadingStyle, HtmlMode
from .containers import Document, List, ListItem, Quote, Table
from .containers.enums import AlertKind, ListMarker, TableAlign
from .inline import (
    Emphasis,
    Entity,
    InlineCode,
    InlineJoin,
    LineBreak,
    Link,
    Math,
    Reference,
    Text,
)
from .inline.enums import EmphasisKind, EmphasisMarker, LinkKind, ReferenceKind
from .output import MarkdownText, to_file
from . import presets as presets
from .presets import *
from .presets import __all__ as _presets_all


__all__ = [
    # base classes
    "InlineMarkdown", "Markdown", "NodeLevel",
    # inline nodes
    "Emphasis", "Entity", "InlineCode", "InlineJoin", "LineBreak", "Link", "Math", "Reference", "Text",
    # block nodes
    "BlankLine", "CodeBlock", "Footnote", "Frontmatter", "Heading", "Html", "LinkDefinition",
    "Paragraph", "ThematicBreak",
    # container nodes
    "Document", "List", "ListItem", "Quote", "Table",
    # enums
    "AlertKind", "BreakChar", "EmphasisKind", "EmphasisMarker", "FenceChar", "FootnoteRole",
    "HeadingStyle", "HtmlMode", "LineBreakStyle", "LinkKind", "ListMarker", "ReferenceKind", "TableAlign",
    # output
    "MarkdownText", "to_file",
    # presets
    *_presets_all,
]


_DESIGN_NOTES = """
# simplibs-markdown — Markdown Built From Nodes

A tree of named nodes that writes Markdown, so a document is Python and the
text cannot be malformed by a stray character. Content is escaped, structure
is checked when a node is built, and every mistake is an error card.

```python
from simplibs.markdown import Heading, Paragraph, Table, MarkdownText
from simplibs.markdown.presets import H1, BOLD, NOTE

doc = H1("Project") + Paragraph("It is " + BOLD("important") + ".") + NOTE("A draft.")
print(MarkdownText(doc))
```

## What the Root Exports
Nodes, base classes, enums, the output layer, and all presets imported
directly for convenience.

## Composition
`+` joins inline nodes into one line and anything with a block into a
`Document`. Strings are content: escaped text next to an inline node, a
paragraph next to a block.

## Layers
`_common` <- `base_class` <- `inline` <- `blocks` <- `containers` <- `output`
<- `presets`. Each layer imports only from those on its left.

## Internal Components Registry

| Component      | Type        | Description                                                        |
| :------------- | :---------- | :----------------------------------------------------------------- |
| `_common`      | Sub-package | Helpers, enums and diagnostic raisers used by more than one layer. |
| `base_class`   | Sub-package | `Markdown`, `InlineMarkdown`, `NodeLevel`.                         |
| `blocks`       | Sub-package | Leaf blocks: headings, paragraphs, code, rules, HTML, footnotes.   |
| `containers`   | Sub-package | `Document`, `Quote`, `List`, `ListItem`, `Table`.                  |
| `inline`       | Sub-package | Nodes inside a line: text, emphasis, links, code, references.      |
| `output`       | Sub-package | `MarkdownText` and `to_file`.                                      |
| `presets`      | Sub-package | Named shortcuts: `H1`, `BOLD`, `NOTE`, `BULLET_LIST`...            |
"""
