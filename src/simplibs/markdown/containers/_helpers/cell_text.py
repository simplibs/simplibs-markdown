from typing import Any
# Outers
from ..._common.helpers import as_inline
from .._validations.table import raise_table_cell_multiline_error
# Inners
from .escape_pipes import escape_pipes


def cell_text(cell: Any) -> str:
    """Render one table cell as a single line.

    Args:
        cell: A string, an inline node or a list of them.

    Returns:
        The rendered text with pipes escaped.

    Raises:
        ParamError: If the cell is not inline content or has a line break.
    """

    # 1. Render the content as inline text
    text = as_inline(cell).to_text()

    # 2. A row is one line, so the cell cannot have a line break
    if "\n" in text:
        raise_table_cell_multiline_error(text)

    # 3. A pipe that belongs to the text must not end the cell
    return escape_pipes(text)


_DESIGN_NOTES = """
# cell_text — One Cell, One Line

## Purpose
A cell goes through the same gate as any other inline slot (`as_inline`), so a
string is escaped and a node is written as it is. Then it must fit on one
line, with its pipes escaped.
"""
