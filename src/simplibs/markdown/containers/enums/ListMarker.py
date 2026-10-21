from enum import Enum


class ListMarker(Enum):
    """The marker of a list. The value is the character written after the number or alone."""

    DASH = "-"
    ASTERISK = "*"
    PLUS = "+"
    DOT = "."
    PAREN = ")"


_DESIGN_NOTES = """
# ListMarker — Bullets and Number Endings

## Members
* `DASH`, `ASTERISK`, `PLUS` — the bullet of an unordered list.
* `DOT`, `PAREN` — what follows the number of an ordered list (`1.`, `1)`).

## Pairing
Which markers fit which list is checked when the `List` is built.

## Known Gap
Two lists of the same marker one after another merge into one list in
CommonMark, even with a blank line between them. Alternating the marker, or a
`Html` comment between the lists, keeps them apart.
"""
