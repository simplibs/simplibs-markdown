from enum import Enum


class FenceChar(Enum):
    """The character of a code fence. The value is the character."""

    BACKTICK = "`"
    TILDE = "~"


_DESIGN_NOTES = """
# FenceChar — The Character Itself

## Purpose
`.value` is written as it is, repeated as often as the code needs.

## Why Both
A backtick fence cannot have a backtick in its info string; a tilde fence
can. It is also the way out of code that contains both kinds of fence.

## Not `EmphasisMarker.TILDE`
The values are equal but the enums are different, so the two meanings cannot
be mixed up.
"""
