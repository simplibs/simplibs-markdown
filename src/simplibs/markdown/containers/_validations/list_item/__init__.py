from .raise_list_item_checked_without_content_error import raise_list_item_checked_without_content_error


_DESIGN_NOTES = """
# List Item Validations Sub-Package

## Purpose
Diagnostic raisers for the `ListItem` node.

## Internal Components Registry

| Component                                       | Type     | Description                                              |
| :---------------------------------------------- | :------- | :------------------------------------------------------- |
| `raise_list_item_checked_without_content_error` | Function | Raises `ParamError` when a task item has no paragraph first. |
"""
