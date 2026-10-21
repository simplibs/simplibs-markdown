from enum import Enum


class EmphasisKind(Enum):
    """What the emphasis says about its text."""

    EM = "em"
    STRONG = "strong"
    STRONG_EM = "strong_em"
    STRIKE = "strike"


_DESIGN_NOTES = """
# EmphasisKind — Four Shapes of One Mechanism

## Purpose
All four are a marker repeated around text, so they are one node with a kind,
not four nodes.

## Members
* `EM` — `*text*`, one marker.
* `STRONG` — `**text**`, two markers.
* `STRONG_EM` — `***text***`, three markers.
* `STRIKE` — `~~text~~`, two markers of a different character.
"""
