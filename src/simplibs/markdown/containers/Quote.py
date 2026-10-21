# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.helpers import flatten_blocks, prefix_lines, separate_blocks
from .._common.validations import raise_no_blocks_error
# Inners
from ._validations.quote import raise_quote_unknown_alert_error
from .enums import AlertKind


class Quote(Markdown):
    """A block quote, optionally a GitHub alert.

    Args:
        *blocks: The content: strings, nodes, documents, or lists of them.
        alert: When given, the quote is an alert (`> [!NOTE]`).

    Raises:
        ParamError: If `alert` is not an `AlertKind`, or a plain quote has no content.
    """

    __slots__ = ("blocks", "alert")

    node_level = NodeLevel.BLOCK

    def __init__(self, *blocks, alert: AlertKind | None = None) -> None:

        # 1. Validation
        if alert is not None and not isinstance(alert, AlertKind):
            raise_quote_unknown_alert_error(alert)
        flat = flatten_blocks(*blocks)
        if not flat and alert is None:
            raise_no_blocks_error("Quote")

        # 2. Assignment
        self.blocks = flat
        self.alert = alert

    def to_lines(self) -> tuple[str, ...]:

        # 1. The content, with a blank line between the blocks
        lines = separate_blocks(self.blocks, gap=1)

        # 2. An alert starts with its marker line
        if self.alert is not None:
            lines = (f"[!{self.alert.value}]", *lines)

        # 3. Every line gets the quote mark; an empty line becomes a bare '>'
        return prefix_lines(lines, "> ")


_DESIGN_NOTES = """
# Quote — Nesting by Prefix

## Purpose
A quote is its content with `> ` in front of every line. Lists, code and
other quotes inside it need no special case, because they already are lines.

## Alert
`> [!NOTE]` is a quote whose first line is a marker. An alert may be empty
(only the marker); a plain quote may not.

## Content Without a Blank Line After the Marker
GitHub wants the content on the lines right after `[!NOTE]`, so no blank line
is added there.
"""
