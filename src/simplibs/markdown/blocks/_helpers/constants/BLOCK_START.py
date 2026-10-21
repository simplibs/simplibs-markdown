import re
from typing import Final


BLOCK_START: Final = re.compile(
    r"^ {0,3}(?:"
    r"#{1,6}(?:\s|$)"
    r"|>"
    r"|[-+*](?:\s|$)"
    r"|\d{1,9}[.)](?:\s|$)"
    r"|`{3,}[^`]*$"
    r"|~{3,}"
    r"|(?:[-*_]\s*){3,}$"
    r"|=+\s*$"
    r"|<!--"
    r")"
)
"""Pattern of a line that Markdown would read as the start of a block."""


_DESIGN_NOTES = """
# BLOCK_START — The Lines a Paragraph Must Not Start With

## Purpose
The beginnings that turn a line into a heading, a quote, a list item, a fence,
a rule, a setext underline or a comment.

## Up to Three Spaces
Four spaces make an indented code block, which is a block start of its own,
so the pattern allows an indent of 0 to 3. `Paragraph` removes the indent
anyway.

## Fences — Backticks Are Narrower Than Tildes
The info string of a backtick fence cannot contain a backtick (CommonMark),
so a run of three or more backticks starts a block only when no backtick
follows it: ```` ```py ```` is a fence, ```` ```a``b``` ```` is not.

The second form is what `InlineCode("a``b")` writes (the content holds two
backticks, so the delimiter is three). Escaping its first backtick would
break the code span, so the line has to be left alone.

A tilde fence has no such rule, so `~~~a`b` is a fence and is still escaped.
"""
