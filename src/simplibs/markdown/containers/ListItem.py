# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from ..blocks import Paragraph
from .._common.helpers import flatten_blocks, prefix_lines, separate_blocks
# Inners
from ._validations.list_item import raise_list_item_checked_without_content_error


class ListItem(Markdown):
    """One item of a list: any blocks, and an optional checkbox.

    Args:
        *blocks: The content: strings, nodes, documents, or lists of them.
        checked: `True` writes `[x]`, `False` writes `[ ]`, `None` no checkbox.

    Raises:
        ParamError: If `checked` is set and the content does not start with a paragraph.
    """

    __slots__ = ("blocks", "checked")

    node_level = NodeLevel.BLOCK

    def __init__(self, *blocks, checked: bool | None = None) -> None:

        # 1. Validation: the checkbox is written in front of the first line of text
        flat = flatten_blocks(*blocks)
        if checked is not None and (not flat or not isinstance(flat[0], Paragraph)):
            raise_list_item_checked_without_content_error()

        # 2. Assignment
        self.blocks = flat
        self.checked = checked

    @property
    def needs_loose(self) -> bool:
        """Whether two paragraphs follow each other, which only a loose list can write."""

        # 1. Look at every pair of neighbouring blocks
        pairs = zip(self.blocks, self.blocks[1:])
        return any(isinstance(first, Paragraph) and isinstance(second, Paragraph) for first, second in pairs)

    def content_lines(self, loose: bool) -> tuple[str, ...]:
        """Write the content of the item without its marker.

        Args:
            loose: `True` puts a blank line between the blocks of the item.

        Returns:
            The lines of the content, the first one with the checkbox if there is one.
        """

        # 1. The blocks, with or without blank lines between them
        lines = separate_blocks(self.blocks, gap=1 if loose else 0)

        # 2. The checkbox goes in front of the first line
        if self.checked is not None and lines:
            box = "[x] " if self.checked else "[ ] "
            lines = (box + lines[0], *lines[1:])

        return lines

    def to_lines(self) -> tuple[str, ...]:

        # 1. Alone, an item is written as a bullet item
        content = self.content_lines(self.needs_loose)

        # 2. An item without content is the bare marker
        if not content:
            return ("-",)

        # 3. The marker on the first line, indentation on the others
        return prefix_lines(content, "- ", "  ")


_DESIGN_NOTES = """
# ListItem — The Content of One Bullet

## Purpose
An item can hold several paragraphs, code, a nested list. The list decides the
marker and whether the items are tight or loose; the item writes its own
content (`content_lines`).

## Loose Lists
Two paragraphs inside one item cannot be written tightly. `needs_loose` tells
the list so, and the whole list is written loose.

## Alone
A bare `ListItem` is written as a bullet item. The draft built a one-item
`List` for that, which made `ListItem` and `List` import each other.

## Checkbox
Only in front of text, so the first block has to be a paragraph.
"""
