from simplibs.file import write_text
# Outers
from ..base_class import Markdown
from .._common.validations import raise_param_invalid_type_error
from ..containers import Document


class MarkdownText:
    """The finished Markdown text of a node.

    Args:
        node: Any node. A node that is not a `Document` is wrapped in one.

    Attributes:
        document: The `Document` that was rendered.
        text: The whole text, ending with a newline.
        lines: The lines of the text.

    Raises:
        ParamError: If `node` is not a Markdown node.
    """

    __slots__ = ("document", "text", "lines")

    def __init__(self, node: Markdown) -> None:

        # 1. Validation
        if not isinstance(node, Markdown):
            raise_param_invalid_type_error("node", node, Markdown)

        # 2. Render once; a document is used as it is, anything else is wrapped
        document = node if isinstance(node, Document) else Document(node)

        # 3. Assignment
        self.document = document
        self.text = document.to_text()
        self.lines = document.to_lines()

    def __str__(self) -> str:
        return self.text

    def __iter__(self):
        return iter(self.lines)

    def __len__(self) -> int:
        return len(self.lines)

    def to_file(self, path, *, overwrite: bool = True, **write_options):
        """Write the text to a file.

        Args:
            path: The target file.
            overwrite: `False` raises instead of replacing an existing file.
            **write_options: Passed to `write_text` (`encoding`, `newline`...).

        Returns:
            The normalized path of the written file.
        """

        # 1. The writing, with its draft-and-swap and its error cards, is `write_text`
        return write_text(path, self.text, overwrite=overwrite, **write_options)


_DESIGN_NOTES = """
# MarkdownText — The End of the Node Tree

## Purpose
A node is a description; this is the result. The text is rendered once and
kept, so `str()`, iteration and `len()` do not render again.

## Why a Class and Not a Plain String
Lines are as useful as the text (diffs, tests, counting) and the file write
belongs to the finished text, not to every node.

## No Import of `to_file`
`MarkdownText.to_file` calls `write_text` itself, and the `to_file` function
imports `MarkdownText`. One direction only, so the two files do not import each
other.

## Dependency
`simplibs-file` is needed here and nowhere else.
"""
