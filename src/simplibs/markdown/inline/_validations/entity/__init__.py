from .raise_entity_codepoint_out_of_range_error import raise_entity_codepoint_out_of_range_error
from .raise_entity_name_xor_codepoint_error import raise_entity_name_xor_codepoint_error
from .raise_entity_unknown_name_error import raise_entity_unknown_name_error


_DESIGN_NOTES = """
# Entity Validations Sub-Package

## Purpose
Diagnostic raisers for the `Entity` node.

## Internal Components Registry

| Component                                   | Type     | Description                                                    |
| :------------------------------------------ | :------- | :------------------------------------------------------------- |
| `raise_entity_codepoint_out_of_range_error` | Function | Raises `ParamError` when a code point is not a valid Unicode value. |
| `raise_entity_name_xor_codepoint_error`     | Function | Raises `ParamError` unless exactly one of name and code point is given. |
| `raise_entity_unknown_name_error`           | Function | Raises `ParamError` when a name is not an HTML5 entity.        |
"""
