from .raise_thematic_break_invalid_char_error import raise_thematic_break_invalid_char_error
from .raise_thematic_break_too_short_error import raise_thematic_break_too_short_error


_DESIGN_NOTES = """
# Thematic Break Validations Sub-Package

## Purpose
Diagnostic raisers for the `ThematicBreak` node.

## Internal Components Registry

| Component                                | Type     | Description                                                |
| :--------------------------------------- | :------- | :--------------------------------------------------------- |
| `raise_thematic_break_invalid_char_error`| Function | Raises `ParamError` when the character is not a `BreakChar`. |
| `raise_thematic_break_too_short_error`   | Function | Raises `ParamError` when the break has fewer than 3 characters. |
"""
