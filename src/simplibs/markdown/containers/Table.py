from collections.abc import Iterable
# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import as_cells, pad_cell, separator_cell
from ._validations.table import (
    raise_table_align_width_mismatch_error,
    raise_table_no_columns_error,
    raise_table_row_width_mismatch_error,
)
from .enums import TableAlign


class Table(Markdown):
    """A table with a header, rows and column alignment.

    Args:
        head: The header: a list of cells, or one string for a one-column table.
        rows: The rows, each a list of cells (or one string for a one-column table).
        align: One `TableAlign` per column. Defaults to no alignment.

    Raises:
        ParamError: If the header is empty, a row or the alignment has another
            width than the header, a cell has a line break, or a type is wrong.
    """

    __slots__ = ("head", "rows", "align")

    node_level = NodeLevel.BLOCK

    def __init__(self, head, rows=(), align=None) -> None:

        # 1. Validation
        # 1.1 The header sets the number of columns
        head_cells = as_cells(head, "head")
        if not head_cells:
            raise_table_no_columns_error()

        # 1.2 Every row has as many cells as the header
        if isinstance(rows, str) or not isinstance(rows, Iterable):
            raise_param_invalid_type_error("rows", rows, "a list of rows")
        body = []
        for row in rows:
            cells = as_cells(row, "rows")
            if len(cells) != len(head_cells):
                raise_table_row_width_mismatch_error(cells, len(head_cells))
            body.append(cells)

        # 1.3 One alignment per column
        if align is None:
            align = (TableAlign.NONE,) * len(head_cells)
        elif not isinstance(align, (list, tuple)):
            raise_param_invalid_type_error("align", align, "a list of TableAlign")
        else:
            align = tuple(align)
            for column_align in align:
                if not isinstance(column_align, TableAlign):
                    raise_param_invalid_type_error("align", column_align, TableAlign)
        if len(align) != len(head_cells):
            raise_table_align_width_mismatch_error(align, len(head_cells))

        # 2. Assignment
        self.head = head_cells
        self.rows = tuple(body)
        self.align = align

    def to_lines(self) -> tuple[str, ...]:

        # 1. Each column is as wide as its longest cell, and at least 3 (the separator needs it)
        widths = [
            max(3, len(title), *(len(row[index]) for row in self.rows))
            for index, title in enumerate(self.head)
        ]

        # 2. A line is its cells padded to the column widths
        def line(cells: tuple[str, ...]) -> str:
            padded = (pad_cell(cell, width, align) for cell, width, align in zip(cells, widths, self.align))
            return "| " + " | ".join(padded) + " |"

        # 3. The separator row carries the alignment
        separator = "| " + " | ".join(
            separator_cell(width, align) for width, align in zip(widths, self.align)
        ) + " |"

        # 4. Header, separator, rows
        return (line(self.head), separator, *(line(row) for row in self.rows))


_DESIGN_NOTES = """
# Table — Cells Are Inline Content

## Purpose
A GFM table: a header, a separator row with the alignment, and rows. Each cell
goes through `as_inline`, so strings are escaped and nodes are written as they
are, and it has to stay on one line.

## Checked at Construction
Width of every row and of the alignment, the type of each alignment and each
cell. GFM would pad or cut a wrong row without a word.

## Changed From the Draft
* `rows` must be a non-string iterable (the draft accepted a string and
  iterated over its characters).
* Alignments must be `TableAlign` members.
* A pipe after a backslash is escaped correctly (see `escape_pipes`).

## Known Limit
The width is `len`, so a table with wide characters is not aligned in the
source (see `pad_cell`).
"""
