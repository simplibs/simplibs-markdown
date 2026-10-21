from types import MappingProxyType
from typing import Final
# Outers
from simplibs.markdown._common.enums import LineBreakStyle


BREAK_SUFFIX: Final = MappingProxyType({
    LineBreakStyle.SPACES: "  ",
    LineBreakStyle.BACKSLASH: "\\",
    LineBreakStyle.HTML: "<br>",
})
"""What `Paragraph` appends to a line to make a hard break after it (read-only)."""


_DESIGN_NOTES = """
# BREAK_SUFFIX — The End of a Line That Is Not the Last

## Purpose
A paragraph has already split its content into lines, so the mark goes to the
end of each line but the last and no newline is written.

## Not `LINE_BREAKS`
`LineBreak` in `inline` writes the mark together with the newline, because it
sits in the middle of a line of content.
"""
