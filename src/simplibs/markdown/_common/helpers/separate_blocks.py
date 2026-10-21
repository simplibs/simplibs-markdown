from collections.abc import Iterable
from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...base_class import Markdown


def separate_blocks(
    blocks: "Iterable[Markdown]",
    gap: int = 1,
) -> tuple[str, ...]:
    """Render blocks as lines with blank lines between them.

    Args:
        blocks: The block nodes in order.
        gap: How many blank lines go between two blocks.

    Returns:
        All lines of all blocks.
    """

    # 1. Lazy (upward) — the blocks are above `_common` in the import graph
    from ...blocks.BlankLine import BlankLine
    from ...blocks.LinkDefinition import LinkDefinition

    # 2. Render block by block
    lines: list[str] = []
    previous = None
    for block in blocks:

        # 2.1 A separator goes between two blocks, with two exceptions:
        # next to an explicit BlankLine, and between link definitions, which stack
        if previous is not None and gap:
            skip = (
                isinstance(previous, BlankLine)
                or isinstance(block, BlankLine)
                or (isinstance(previous, LinkDefinition) and isinstance(block, LinkDefinition))
            )
            if not skip:
                lines.extend([""] * gap)

        # 2.2 Then the block itself
        lines.extend(block.to_lines())
        previous = block

    return tuple(lines)


_DESIGN_NOTES = """
# separate_blocks — Blank Lines Between Blocks

## Purpose
Blocks are joined with a blank line, so the author does not write one. A
`Document` uses `gap=1`, a tight list `gap=0`, a loose list `gap=1`.

## The Two Exceptions
* An explicit `BlankLine` already is the separator. Adding another would
  double it.
* Link definitions are written one under another, as people write them.

## Why It Lives in `_common`
Used by `Footnote` and `Html` (`blocks`) and by `Quote`, `ListItem` and
`Document` (`containers`).

## Lazy (Upward) Imports
`BlankLine` and `LinkDefinition` are blocks. The import sits inside the
function, so `_common` loads without any node.
"""
