from .raise_inline_code_empty_error import raise_inline_code_empty_error


_DESIGN_NOTES = """
# Inline Code Validations Sub-Package

## Purpose
Diagnostic raisers for the `InlineCode` node.

## Internal Components Registry

| Component                      | Type     | Description                                      |
| :----------------------------- | :------- | :----------------------------------------------- |
| `raise_inline_code_empty_error`| Function | Raises `ParamError` when the code is empty.      |
"""
