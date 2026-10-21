from typing import Any
# Outers
from ..._common.validations import raise_param_invalid_type_error
from ...base_class import Markdown
# Inners
from .cell_text import cell_text


def as_cells(row: Any, name: str = "row") -> tuple[str, ...]:
    """Turn a row into a tuple of rendered cells.

    Args:
        row: A list or tuple of cells, or one string or node (a row of one cell).
        name: The parameter name shown in the error card.

    Returns:
        The rendered cells.

    Raises:
        ParamError: If the row is not a string, a node, a list or a tuple.
    """

    # 1. A string or a node is a row of one cell
    if isinstance(row, (str, Markdown)):
        row = (row,)

    # 2. Anything else has to be a list or a tuple of cells
    elif not isinstance(row, (list, tuple)):
        raise_param_invalid_type_error(name, row, "str, list or tuple")

    # 3. Render each cell
    return tuple(cell_text(cell) for cell in row)


_DESIGN_NOTES = """
# as_cells — A Row in Any Form

## Purpose
`Table("name", ["a", "b"])` has a one-column header and rows of one cell
given as plain strings. The header and every row use this one function.

## Added Since the Draft
A check of the row's type with the parameter name in the card. In the draft
a number as a row failed with an unrelated `TypeError`.
"""
