from .raise_reference_invalid_value_error import raise_reference_invalid_value_error


_DESIGN_NOTES = """
# Reference Validations Sub-Package

## Purpose
Diagnostic raisers for the `Reference` node (mentions, issues, commits...).

## Internal Components Registry

| Component                           | Type     | Description                                                   |
| :---------------------------------- | :------- | :------------------------------------------------------------ |
| `raise_reference_invalid_value_error`| Function | Raises `ParamError` when a value does not fit its kind of reference. |
"""
