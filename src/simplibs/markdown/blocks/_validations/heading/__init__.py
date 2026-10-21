from .raise_heading_empty_setext_error import raise_heading_empty_setext_error
from .raise_heading_level_out_of_range_error import raise_heading_level_out_of_range_error
from .raise_heading_multiline_error import raise_heading_multiline_error
from .raise_heading_setext_level_error import raise_heading_setext_level_error


_DESIGN_NOTES = """
# Heading Validations Sub-Package

## Purpose
Diagnostic raisers for the `Heading` node.

## Internal Components Registry

| Component                                | Type     | Description                                                   |
| :--------------------------------------- | :------- | :------------------------------------------------------------ |
| `raise_heading_empty_setext_error`       | Function | Raises `ParamError` when a setext heading has no text.        |
| `raise_heading_level_out_of_range_error` | Function | Raises `ParamError` when the level is not an integer from 1 to 6. |
| `raise_heading_multiline_error`          | Function | Raises `ParamError` when the heading text spans several lines. |
| `raise_heading_setext_level_error`       | Function | Raises `ParamError` when a setext heading has a level above 2. |
"""
