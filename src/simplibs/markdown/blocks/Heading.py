import re
# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.helpers import as_inline
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._validations.heading import (
    raise_heading_empty_setext_error,
    raise_heading_level_out_of_range_error,
    raise_heading_multiline_error,
    raise_heading_setext_level_error,
)
from .enums import HeadingStyle


class Heading(Markdown):
    """A heading of level 1 to 6.

    Args:
        inner: The heading text (a string, an inline node or a list of them).
        level: The level, 1 (the biggest) to 6.
        style: How the heading is written. `SETEXT` supports levels 1 and 2.

    Raises:
        ParamError: If the level or the style is not valid, the text spans more
            lines, or a setext heading has no text.
    """

    __slots__ = ("inner", "level", "style")

    node_level = NodeLevel.BLOCK

    def __init__(
        self,
        inner,
        level: int = 1,
        style: HeadingStyle = HeadingStyle.ATX,
    ) -> None:

        # 1. Validation
        # 1.1 The level is an integer from 1 to 6; a bool is not accepted
        if isinstance(level, bool) or not isinstance(level, int) or not 1 <= level <= 6:
            raise_heading_level_out_of_range_error(level)

        # 1.2 The style and its limit
        if not isinstance(style, HeadingStyle):
            raise_param_invalid_type_error("style", style, HeadingStyle)
        if style is HeadingStyle.SETEXT and level > 2:
            raise_heading_setext_level_error(level)

        # 1.3 The text is one line
        inner = as_inline(inner)
        text = inner.to_text().strip()
        if "\n" in text:
            raise_heading_multiline_error(text)

        # 1.4 A setext heading needs text above its underline
        if style is HeadingStyle.SETEXT and not text:
            raise_heading_empty_setext_error()

        # 2. Assignment
        self.inner = inner
        self.level = level
        self.style = style

    def to_lines(self) -> tuple[str, ...]:

        # 1. The text without the edge whitespace
        text = self.inner.to_text().strip()

        # 2. Setext: the text and an underline at least as long as the text
        if self.style is HeadingStyle.SETEXT:
            underline = ("=" if self.level == 1 else "-") * max(3, len(text))
            return (text, underline)

        # 3. ATX: a run of '#' after a space (or the whole text) would be read as a closing
        #    mark, so its last '#' is escaped; a '#' after a letter (`C#`) is not a closing mark
        if re.search(r"(?:^|[ \t])#+$", text):
            text = text[:-1] + "\\#"
        hashes = "#" * self.level

        # 4. An empty ATX heading is just the hashes
        if not text:
            return (hashes,)

        # 5. The closed form repeats the hashes after the text
        if self.style is HeadingStyle.ATX_CLOSED:
            return (f"{hashes} {text} {hashes}",)
        return (f"{hashes} {text}",)


_DESIGN_NOTES = """
# Heading — Three Styles, One Node

## Purpose
`#`, `# text #` and an underlined text are one idea written three ways, so
they are one node with a `style`.

## Limits Checked at Construction
Six levels; setext only for levels 1 and 2; one line of text; text for a
setext heading. Each has its own card.

## The Trailing `#`
A run of `#` that follows a space closes an ATX heading, so `# a #` would give
the heading `a`. When the text ends like that, or is only `#`, its last `#`
is written as `\\#` (`# a \\#`).

A `#` that follows a letter is no closing mark: CommonMark needs a space
before it. `C#` is therefore written as it is (`# C#`). A `#` that is escaped
already (`a \\#`) has no space in front of it either, so it is left alone.

## `level` Is the Heading Level
It is not `node_level`, which says only whether the node is a block.
"""
