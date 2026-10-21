from .raise_table_align_width_mismatch_error import raise_table_align_width_mismatch_error
from .raise_table_cell_multiline_error import raise_table_cell_multiline_error
from .raise_table_no_columns_error import raise_table_no_columns_error
from .raise_table_row_width_mismatch_error import raise_table_row_width_mismatch_error


_DESIGN_NOTES = """
# Table Validations Sub-Package

## Purpose
Diagnostic raisers for the `Table` node.

## Internal Components Registry

| Component                                 | Type     | Description                                                 |
| :---------------------------------------- | :------- | :---------------------------------------------------------- |
| `raise_table_align_width_mismatch_error`  | Function | Raises `ParamError` when the alignments do not match the columns. |
| `raise_table_cell_multiline_error`        | Function | Raises `ParamError` when a cell contains a line break.      |
| `raise_table_no_columns_error`            | Function | Raises `ParamError` when the header has no column.          |
| `raise_table_row_width_mismatch_error`    | Function | Raises `ParamError` when a row is wider or narrower than the header. |
"""
