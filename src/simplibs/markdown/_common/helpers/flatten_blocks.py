from typing import Any, TYPE_CHECKING
# Outers
from ..validations import raise_node_not_markdown_error
# Annotations
if TYPE_CHECKING:
    from ...base_class import Markdown


def flatten_blocks(*items: Any) -> "tuple[Markdown, ...]":
    """Turn anything fit for a block slot into a flat tuple of block nodes.

    Args:
        *items: Strings, nodes, documents, or lists and tuples of them.
            `None` is skipped.

    Returns:
        The block nodes in order.

    Raises:
        ParamError: If an item is not a string and not a node.
    """

    # 1. Lazy (upward) — the blocks and the document are above `_common`
    from ...base_class.enums import NodeLevel
    from ...base_class.Markdown import Markdown
    from ...blocks.BlankLine import BlankLine
    from ...blocks.Paragraph import Paragraph
    from ...containers.Document import Document

    # 2. Walk the items in order
    blocks: list[Markdown] = []
    for item in items:

        # 2.1 Nothing to add
        if item is None:
            continue

        # 2.2 A nested collection is flattened by recursion
        if isinstance(item, (list, tuple)):
            blocks.extend(flatten_blocks(*item))

        # 2.3 A string is a paragraph, an empty string is a blank line
        elif isinstance(item, str):
            blocks.append(BlankLine(1) if item == "" else Paragraph(item))

        # 2.4 Anything else has to be a node
        elif not isinstance(item, Markdown):
            raise_node_not_markdown_error(item)

        # 2.5 A document brings its own blocks, so documents never nest
        elif isinstance(item, Document):
            blocks.extend(item.blocks)

        # 2.6 An inline node gets a paragraph around it
        elif item.node_level is NodeLevel.INLINE:
            blocks.append(Paragraph(item))

        # 2.7 A block node goes in as it is
        else:
            blocks.append(item)

    return tuple(blocks)


_DESIGN_NOTES = """
# flatten_blocks — One Rule for Every Block Slot

## Purpose
`Quote("text")`, `Quote(Paragraph("text"))`, `Quote(["a", "b"])` and
`Quote(Document(...))` are all meant to work. This function turns each of
them into the same thing: a flat tuple of block nodes.

## Decisions
* `""` becomes a `BlankLine`, which is the explicit empty line.
* A string or an inline node in a block slot is wrapped into a `Paragraph`
  silently. A strict variant that refuses it is possible, but it makes the
  common `Quote("text")` longer for no gain.
* A `Document` is unpacked, not nested. The `gap` and `final_newline` of the
  inner document are therefore lost.

## Why It Lives in `_common`
Used by `Footnote` and `Html` (`blocks`) and by `Quote`, `ListItem` and
`Document` (`containers`).

## Lazy (Upward) Imports
`BlankLine`, `Paragraph` and `Document` are above `_common`; the imports sit
inside the function.
"""
