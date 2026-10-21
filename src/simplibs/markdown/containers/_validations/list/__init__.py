from .raise_list_item_not_list_item_error import raise_list_item_not_list_item_error
from .raise_list_marker_ordered_mismatch_error import raise_list_marker_ordered_mismatch_error
from .raise_list_no_items_error import raise_list_no_items_error
from .raise_list_start_negative_error import raise_list_start_negative_error
from .raise_list_start_on_bullet_error import raise_list_start_on_bullet_error


_DESIGN_NOTES = """
# List Validations Sub-Package

## Purpose
Diagnostic raisers for the `List` node.

## Internal Components Registry

| Component                                  | Type     | Description                                                   |
| :----------------------------------------- | :------- | :------------------------------------------------------------ |
| `raise_list_item_not_list_item_error`      | Function | Raises `ParamError` when an item is not usable as a list item. |
| `raise_list_marker_ordered_mismatch_error` | Function | Raises `ParamError` when the marker does not fit the list kind. |
| `raise_list_no_items_error`                | Function | Raises `ParamError` when a list has no items.                 |
| `raise_list_start_negative_error`          | Function | Raises `ParamError` when the start is not a non-negative integer. |
| `raise_list_start_on_bullet_error`         | Function | Raises `ParamError` when a bullet list gets a start number.   |
"""
