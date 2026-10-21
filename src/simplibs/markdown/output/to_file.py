from simplibs.file import write_text
# Inners
from .MarkdownText import MarkdownText


def to_file(source, path, *, overwrite: bool = True, **write_options):
    """Write Markdown to a file.

    Args:
        source: A string (written as it is), a node, or a `MarkdownText`.
        path: The target file.
        overwrite: `False` raises instead of replacing an existing file.
        **write_options: Passed to `write_text` (`encoding`, `newline`...).

    Returns:
        The normalized path of the written file.

    Raises:
        ParamError: If `source` is not a string, a node or a `MarkdownText`.
    """

    # 1. A string is already the text
    if isinstance(source, str):
        return write_text(path, source, overwrite=overwrite, **write_options)

    # 2. A node is rendered first; anything else fails there with a clear card
    if not isinstance(source, MarkdownText):
        source = MarkdownText(source)

    # 3. The finished text writes itself
    return source.to_file(path, overwrite=overwrite, **write_options)


_DESIGN_NOTES = """
# to_file — One Call From Anything to a File

## Purpose
`to_file(doc, "out/notes.md")` for a node, `to_file(text, path)` for a string
that already is Markdown, `to_file(markdown_text, path)` for a finished text.

## Overwrite
Replaces by default, as `write_text` does. `overwrite=False` turns an existing
file into an error card from `simplibs-file`.
"""
