from enum import Enum


class NodeLevel(Enum):
    """The level of a document at which a node can stand."""

    INLINE = "inline"
    BLOCK = "block"


_DESIGN_NOTES = """
# NodeLevel — A Line or a Block

## Purpose
Every node knows where it may stand. `INLINE` nodes live inside a line of
text (text, emphasis, a link). `BLOCK` nodes are lines of their own (a
heading, a list, a table). `+`, the containers and `as_inline` decide by this
one value.

## Counterpart in `simplibs-regex`
It does the job `Precedence` does there: one tag that lets the containers
refuse a nonsense combination when the node is built, not when the output
turns out wrong.

## Members
* `INLINE` — can be joined with other inline nodes by `+` into one line.
* `BLOCK` — is separated from its neighbours by a blank line.
"""
