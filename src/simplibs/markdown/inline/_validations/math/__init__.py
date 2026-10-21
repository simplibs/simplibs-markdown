from .raise_math_empty_expression_error import raise_math_empty_expression_error


_DESIGN_NOTES = """
# Math Validations Sub-Package

## Purpose
Diagnostic raisers for the `Math` node.

## Internal Components Registry

| Component                         | Type     | Description                                         |
| :-------------------------------- | :------- | :-------------------------------------------------- |
| `raise_math_empty_expression_error`| Function | Raises `ParamError` when the expression is empty.   |
"""
