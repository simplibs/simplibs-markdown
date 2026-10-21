from .as_cells import as_cells
from .cell_text import cell_text
from .escape_pipes import escape_pipes
from .pad_cell import pad_cell
from .separator_cell import separator_cell


_DESIGN_NOTES = """
# Markdown Containers Helpers Sub-Package

## Purpose
Private helpers of `Table`. What a second domain needs lives in
`_common/helpers`.

## Internal Components Registry

| Component        | Type     | Description                                                    |
| :--------------- | :------- | :------------------------------------------------------------- |
| `as_cells`       | Function | Turns a row into a tuple of rendered cells.                    |
| `cell_text`      | Function | Renders one cell as a single line with escaped pipes.          |
| `escape_pipes`   | Function | Escapes the `|` characters that would end a cell.              |
| `pad_cell`       | Function | Pads a cell to the column width according to its alignment.    |
| `separator_cell` | Function | Writes the separator cell of a column, with its alignment colons. |
"""
