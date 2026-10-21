from typing import Final


LINE_START_ESCAPED: Final[frozenset[str]] = frozenset({"#", "+", "-", "="})
"""Characters that `escape_text` escapes only as the first one on a line."""


_DESIGN_NOTES = """
# LINE_START_ESCAPED — Characters That Matter Only at the Start

## Purpose
`#` starts a heading, `+` and `-` a list or a rule, `=` a setext underline.
In the middle of a line they are plain text, so escaping them there would only
add noise.

## Not Here
Ordered list numbers (`1.`) are handled by a pattern in `escape_text`; `>`
(a quote) is already in `ALWAYS_ESCAPED`.
"""
