# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.enums import LineBreakStyle
from .._common.helpers import as_inline
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import BREAK_SUFFIX, escape_block_start
from ._validations.paragraph import raise_paragraph_empty_error


class Paragraph(Markdown):
    """One or more lines of inline content.

    Args:
        *lines: Each argument is one line: a string, an inline node or a list
            of them.
        break_style: When given, every line but the last ends with a hard
            break of this style. Without it the lines are joined by the
            renderer into one flowing paragraph.

    Raises:
        ParamError: If there is no line with text, `break_style` has the wrong
            type, or a line is a block node.
    """

    __slots__ = ("lines", "break_style")

    node_level = NodeLevel.BLOCK

    def __init__(self, *lines, break_style: LineBreakStyle | None = None) -> None:

        # 1. Validation
        nodes = tuple(as_inline(line) for line in lines)
        if not any(node.to_text().strip() for node in nodes):
            raise_paragraph_empty_error()
        if break_style is not None and not isinstance(break_style, LineBreakStyle):
            raise_param_invalid_type_error("break_style", break_style, LineBreakStyle)

        # 2. Assignment
        self.lines = nodes
        self.break_style = break_style

    def to_lines(self) -> tuple[str, ...]:

        # 1. Collect the lines of all nodes
        rendered = []
        for node in self.lines:
            for line in node.to_lines():

                # 1.1 Indentation would make a code block, an empty line would end the paragraph
                line = line.lstrip()
                if not line:
                    continue

                # 1.2 A line that would start a block is escaped
                rendered.append(escape_block_start(line))

        # 2. A hard break goes to the end of every line but the last
        if self.break_style is not None:
            suffix = BREAK_SUFFIX[self.break_style]
            rendered = [line + suffix for line in rendered[:-1]] + rendered[-1:]

        return tuple(rendered)


_DESIGN_NOTES = """
# Paragraph — Arguments Are Lines

## Purpose
`Paragraph("one", "two")` is two lines of one paragraph. Inline nodes are
joined with `+` inside a line: `Paragraph("See " + Link(...) + ".")`.

## Lines Without a Break
Without `break_style` the two lines are one flowing paragraph; a renderer
replaces the newline with a space. Pass a style when the break must show.

## What the Renderer Would Misread
A line is stripped of its indentation and empty lines are dropped. A line that
would still start a block is escaped (`escape_block_start`), which only happens
with unescaped text.
"""
