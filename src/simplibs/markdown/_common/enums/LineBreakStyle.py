from enum import Enum


class LineBreakStyle(Enum):
    """How a hard line break is written."""

    SPACES = "spaces"
    BACKSLASH = "backslash"
    HTML = "html"


_DESIGN_NOTES = """
# LineBreakStyle — Three Ways to Break a Line

## Purpose
The values are identifiers only; the text of each form lives in the tables
that use it (`LINE_BREAKS` in `inline`, `BREAK_SUFFIX` in `blocks`).

## Members
* `SPACES` — two spaces at the end of the line (invisible in an editor).
* `BACKSLASH` — a backslash at the end of the line.
* `HTML` — `<br>`; the only form that stays on one line of the source, which
  is why a table cell can use it.

## Why It Lives in `_common`
Used by `LineBreak` (`inline`) and `Paragraph` (`blocks`). It moved here from
`inline/enums`.
"""
