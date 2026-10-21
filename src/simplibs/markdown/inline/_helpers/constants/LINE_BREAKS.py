from types import MappingProxyType
from typing import Final
# Outers
from simplibs.markdown._common.enums import LineBreakStyle


LINE_BREAKS: Final = MappingProxyType({
    LineBreakStyle.SPACES: "  \n",
    LineBreakStyle.BACKSLASH: "\\\n",
    LineBreakStyle.HTML: "<br>",
})
"""The text of each line break style (read-only)."""


_DESIGN_NOTES = """
# LINE_BREAKS — What a Hard Break Looks Like in the Source

## Purpose
`SPACES` and `BACKSLASH` end the line, `HTML` stays inside it. The table
holds the exact text, including the newline, so `LineBreak` has no branches.

## Not the Same as the Paragraph Suffix
`Paragraph` appends the mark to the end of a line it has already split, so it
keeps its own table without the newline (`BREAK_SUFFIX` in `blocks`).
"""
