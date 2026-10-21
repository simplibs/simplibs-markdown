from enum import Enum


class EmphasisMarker(Enum):
    """The character that wraps emphasized text. The value is the character."""

    ASTERISK = "*"
    UNDERSCORE = "_"
    TILDE = "~"


_DESIGN_NOTES = """
# EmphasisMarker — The Character Itself

## Purpose
`.value` is the character that is written, so the node repeats it
(`marker.value * 2`) without a lookup table.

## Which Marker Fits Which Kind
`TILDE` belongs to `STRIKE`, the other two to the rest. The pairing is checked
when the node is built.

## Known Limit
An underscore does not work inside a word (`snake_case` stays text). The node
sees only its own content, not the text around it, so that case is not
checked.
"""
