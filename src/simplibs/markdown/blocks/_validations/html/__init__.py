from .raise_html_comment_terminator_error import raise_html_comment_terminator_error
from .raise_html_invalid_attribute_error import raise_html_invalid_attribute_error
from .raise_html_invalid_tag_error import raise_html_invalid_tag_error
from .raise_html_void_tag_with_content_error import raise_html_void_tag_with_content_error


_DESIGN_NOTES = """
# Html Validations Sub-Package

## Purpose
Diagnostic raisers for the `Html` node.

## Internal Components Registry

| Component                                | Type     | Description                                                    |
| :--------------------------------------- | :------- | :------------------------------------------------------------- |
| `raise_html_comment_terminator_error`    | Function | Raises `ParamError` when comment text would end the comment early. |
| `raise_html_invalid_attribute_error`     | Function | Raises `ParamError` when an attribute name is not valid.       |
| `raise_html_invalid_tag_error`           | Function | Raises `ParamError` when a tag name is not valid.              |
| `raise_html_void_tag_with_content_error` | Function | Raises `ParamError` when a void tag gets content.              |
"""
