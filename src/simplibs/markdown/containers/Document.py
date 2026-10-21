# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.helpers import flatten_blocks, separate_blocks
from .._common.validations import raise_no_blocks_error, raise_param_invalid_type_error


class Document(Markdown):
    """A whole document: blocks separated by blank lines.

    Args:
        *blocks: The content: strings, nodes, documents, or lists of them.
        gap: How many blank lines go between two blocks.
        final_newline: `True` ends the text with a newline.

    Raises:
        ParamError: If `gap` is not a non-negative integer or there is no content.
    """

    __slots__ = ("blocks", "gap", "final_newline")

    node_level = NodeLevel.BLOCK

    def __init__(self, *blocks, gap: int = 1, final_newline: bool = True) -> None:

        # 1. Validation
        if isinstance(gap, bool) or not isinstance(gap, int) or gap < 0:
            raise_param_invalid_type_error("gap", gap, "non-negative int")
        flat = flatten_blocks(*blocks)
        if not flat:
            raise_no_blocks_error("Document")

        # 2. Assignment
        self.blocks = flat
        self.gap = gap
        self.final_newline = final_newline

    def to_lines(self) -> tuple[str, ...]:

        # 1. The blocks with the chosen gap between them
        return separate_blocks(self.blocks, self.gap)

    def to_text(self) -> str:

        # 1. The lines joined, with the newline a text file ends with
        text = "\n".join(self.to_lines())
        return text + "\n" if self.final_newline else text


_DESIGN_NOTES = """
# Document — The Root of Composition

## Purpose
Everything added with `+` that contains a block ends up here. The document
holds a flat tuple of blocks; documents never nest, because `flatten_blocks`
unpacks a document passed as content.

## `gap` and `final_newline`
Only the outermost document keeps them. A document that is joined with `+` or
passed into another container gives up its own `gap` and `final_newline`.

## `to_text()` Ends With a Newline
A text file is expected to. `to_lines()` has no trailing empty line either
way, so a container that nests the document is not affected.
"""
