from .raise_code_block_indented_with_info_error import raise_code_block_indented_with_info_error
from .raise_code_block_info_has_backtick_error import raise_code_block_info_has_backtick_error


_DESIGN_NOTES = """
# Code Block Validations Sub-Package

## Purpose
Diagnostic raisers for the `CodeBlock` node.

## Internal Components Registry

| Component                                   | Type     | Description                                                   |
| :------------------------------------------ | :------- | :------------------------------------------------------------ |
| `raise_code_block_indented_with_info_error` | Function | Raises `ParamError` when an indented block gets an info string. |
| `raise_code_block_info_has_backtick_error`  | Function | Raises `ParamError` when a backtick fence has a backtick in its info. |
"""
