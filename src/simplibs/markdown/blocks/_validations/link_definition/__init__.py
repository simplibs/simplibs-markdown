from .raise_link_definition_empty_destination_error import raise_link_definition_empty_destination_error
from .raise_link_definition_empty_label_error import raise_link_definition_empty_label_error


_DESIGN_NOTES = """
# Link Definition Validations Sub-Package

## Purpose
Diagnostic raisers for the `LinkDefinition` node.

## Internal Components Registry

| Component                                      | Type     | Description                                           |
| :--------------------------------------------- | :------- | :---------------------------------------------------- |
| `raise_link_definition_empty_destination_error`| Function | Raises `ParamError` when a definition has no destination. |
| `raise_link_definition_empty_label_error`      | Function | Raises `ParamError` when a definition has no label.   |
"""
