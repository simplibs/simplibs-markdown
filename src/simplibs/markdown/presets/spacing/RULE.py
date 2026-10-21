# Outers
from ...blocks import ThematicBreak


RULE = ThematicBreak()
"""Horizontal rule.

Init Params:
    (no parameters)

Markdown:
    Three dashes on a line of their own (`---`).

Example:
    H1("A") + RULE + "text"
    # Writes:
    # # A
    #
    # ---
    #
    # text

Note:
    A ready instance, used without parentheses. For another character or length, use
    `ThematicBreak(BreakChar.ASTERISK, 5)`.
"""
