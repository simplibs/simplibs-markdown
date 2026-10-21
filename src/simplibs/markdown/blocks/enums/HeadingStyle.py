from enum import Enum


class HeadingStyle(Enum):
    """How a heading is written."""

    ATX = "atx"
    ATX_CLOSED = "atx_closed"
    SETEXT = "setext"


_DESIGN_NOTES = """
# HeadingStyle — Three Ways to Write a Heading

## Members
* `ATX` — `# text`, levels 1 to 6.
* `ATX_CLOSED` — `# text #`, the same with closing hashes.
* `SETEXT` — the text with an underline of `=` or `-`; only levels 1 and 2.
"""
