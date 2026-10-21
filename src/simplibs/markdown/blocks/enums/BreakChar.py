from enum import Enum


class BreakChar(Enum):
    """The character of a thematic break. The value is the character."""

    DASH = "-"
    ASTERISK = "*"
    UNDERSCORE = "_"


_DESIGN_NOTES = """
# BreakChar — The Pen That Draws the Rule

## Purpose
`.value` is repeated to the requested length (`---`, `***`, `___`).

## Why Not a Plain String
A free string would let `+++` or `===` through, and `===` under a line of
text is a heading underline.
"""
