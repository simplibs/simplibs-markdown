from types import MappingProxyType
from typing import Final
# Outers
from simplibs.markdown.inline.enums import EmphasisKind


EMPHASIS_REPEAT: Final = MappingProxyType({
    EmphasisKind.EM: 1,
    EmphasisKind.STRONG: 2,
    EmphasisKind.STRONG_EM: 3,
    EmphasisKind.STRIKE: 2,
})
"""How many times each emphasis kind repeats its marker (read-only)."""


_DESIGN_NOTES = """
# EMPHASIS_REPEAT — The Only Difference Between the Kinds

## Purpose
`*x*`, `**x**` and `***x***` differ only in the count, and `~~x~~` is two of
another character. A table of counts replaces four branches.

## Read-Only
A `MappingProxyType`, so nothing can change the table at runtime.
"""
