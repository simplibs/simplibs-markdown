from typing import Final


ALWAYS_ESCAPED: Final[frozenset[str]] = frozenset("\\`*_[]<>&~$")
"""Characters that `escape_text` escapes wherever they stand in a text."""


_DESIGN_NOTES = """
# ALWAYS_ESCAPED — Characters With a Meaning Anywhere

## Purpose
Each of these can start emphasis, code, a link, a tag, an entity,
strike-through or math in the middle of a line.

## Known Noise
The list is cautious: `snake_case` becomes `snake\\_case` and `a & b`
becomes `a \\& b`. Both render correctly. A leaner list is a round-2 topic,
to be checked against a Markdown parser.
"""
