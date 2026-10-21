from .raise_footnote_label_has_whitespace_error import raise_footnote_label_has_whitespace_error
from .raise_footnote_reference_with_blocks_error import raise_footnote_reference_with_blocks_error


_DESIGN_NOTES = """
# Footnote Validations Sub-Package

## Purpose
Diagnostic raisers for the `Footnote` node.

## Internal Components Registry

| Component                                    | Type     | Description                                                   |
| :------------------------------------------- | :------- | :------------------------------------------------------------ |
| `raise_footnote_label_has_whitespace_error`  | Function | Raises `ParamError` when a label is empty, not a string or has whitespace. |
| `raise_footnote_reference_with_blocks_error` | Function | Raises `ParamError` when a footnote reference gets blocks.    |
"""
