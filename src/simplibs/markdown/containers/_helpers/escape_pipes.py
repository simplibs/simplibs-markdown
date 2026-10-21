import re


def escape_pipes(text: str) -> str:
    """Escape the `|` characters that would end a table cell.

    Args:
        text: The rendered text of a cell.

    Returns:
        The text with every unescaped `|` written as `\\|`.
    """

    # 1. A pipe is escaped when an even number of backslashes (possibly none)
    #    stands before it; an odd number means it is escaped already
    return re.sub(r"(?<!\\)((?:\\\\)*)\|", r"\1\\|", text)


_DESIGN_NOTES = """
# escape_pipes — A Pipe Inside a Cell

## Purpose
In a table, `|` separates cells, so a pipe that belongs to the text is written
`\\|`.

## Counting Backslashes
`a\\|b` is escaped already, but `a\\\\|b` is a backslash followed by a pipe
that is not. The text a cell receives has its own backslashes escaped
(`\\\\`), so a lookbehind for a single backslash is not enough: the pipe is
escaped only when an even number of backslashes stands before it.

## Fixed Since the Draft
The draft skipped any pipe after a backslash, so a cell with a backslash
right before a pipe lost its pipe and broke the row.
"""
