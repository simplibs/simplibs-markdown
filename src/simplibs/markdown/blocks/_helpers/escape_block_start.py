import re
# Inners
from simplibs.markdown.blocks._helpers.constants.BLOCK_START import BLOCK_START


def escape_block_start(line: str) -> str:
    """Escape a line that Markdown would read as the start of a block.

    Args:
        line: One line of text without indentation.

    Returns:
        The line unchanged when it starts no block, otherwise escaped so that
        it stays text.
    """

    # 1. A line that starts no block stays as it is
    if not BLOCK_START.match(line):
        return line

    # 2. A number is escaped at its delimiter: "2024. y" -> "2024\. y"
    number = re.match(r"\d{1,9}(?=[.)])", line)
    if number:
        return line[: number.end()] + "\\" + line[number.end():]

    # 3. Everything else is escaped at its first character: "# x" -> "\# x"
    return "\\" + line


_DESIGN_NOTES = """
# escape_block_start — A Second Line of Defence

## Purpose
`Text` already escapes the characters that start a block. This function
catches the lines that arrive unescaped (`Text(..., escape=False)`, raw HTML),
so a paragraph never turns into something else by accident.

## Where the Backslash Goes
A backslash before a punctuation mark escapes it (`\\#`, `\\>`, `\\-`).
Before a digit it is only a backslash, so a numbered line is escaped at the
dot instead: `2024\\. y`.

## Already Escaped Lines Pass
`\\#` does not match the pattern, so an escaped line is not escaped twice.
"""
