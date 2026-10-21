# Outers
from ...inline import LineBreak


HARD_BREAK = LineBreak()
"""Hard line break inside a paragraph.

Init Params:
    (no parameters)

Markdown:
    Two spaces at the end of the line, followed by the line break.

Example:
    "first" + HARD_BREAK + "second"
    # Writes: "first  \\nsecond"

Note:
    A ready instance, used without parentheses. The spaces are invisible in an editor;
    another style is `LineBreak(LineBreakStyle.HTML)` (`<br>`).
"""
