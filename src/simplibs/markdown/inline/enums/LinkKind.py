from enum import Enum


class LinkKind(Enum):
    """The syntax form of a link."""

    INLINE = "inline"
    REFERENCE = "reference"
    COLLAPSED = "collapsed"
    SHORTCUT = "shortcut"
    AUTOLINK = "autolink"
    BARE = "bare"


_DESIGN_NOTES = """
# LinkKind — Six Spellings of a Link

## Purpose
A link and an image are the same node in different forms; the kind says which
form is written.

## Members
* `INLINE` — `[text](destination "title")`.
* `REFERENCE` — `[text][label]`, the destination is in a `LinkDefinition`.
* `COLLAPSED` — `[text][]`, the label is the text.
* `SHORTCUT` — `[text]`, the label is the text.
* `AUTOLINK` — `<destination>`.
* `BARE` — the destination written as it is (GitHub makes it a link).
"""
