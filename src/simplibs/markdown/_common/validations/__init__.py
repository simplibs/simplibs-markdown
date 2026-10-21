from .raise_block_in_inline_error import raise_block_in_inline_error
from .raise_no_blocks_error import raise_no_blocks_error
from .raise_node_not_markdown_error import raise_node_not_markdown_error
from .raise_param_invalid_type_error import raise_param_invalid_type_error


_DESIGN_NOTES = """
# Markdown Common Validations Sub-Package

## Purpose
Diagnostic raisers used by more than one domain (`base_class`, `inline`,
`blocks`, `containers`, `output`). Without this folder each of them would
exist in several copies.

## Placement Rule
A validation used by one element stays in that element's own `_validations/`
folder. Once a second domain needs it, it moves here.

## Internal Components Registry

| Component                       | Type     | Description                                                          |
| :------------------------------ | :------- | :------------------------------------------------------------------- |
| `raise_block_in_inline_error`   | Function | Raises `ParamError` when a block element is placed inside inline content. |
| `raise_no_blocks_error`         | Function | Raises `ParamError` when a container is created without any content.     |
| `raise_node_not_markdown_error` | Function | Raises `ParamError` when a value is neither a string nor a Markdown node. |
| `raise_param_invalid_type_error`| Function | Raises `ParamError` when a parameter has an unusable type.                |
"""
