from .raise_link_autolink_with_text_error import raise_link_autolink_with_text_error
from .raise_link_empty_destination_error import raise_link_empty_destination_error
from .raise_link_image_unsupported_kind_error import raise_link_image_unsupported_kind_error
from .raise_link_kind_requires_label_error import raise_link_kind_requires_label_error


_DESIGN_NOTES = """
# Link Validations Sub-Package

## Purpose
Diagnostic raisers for the `Link` node (links and images).

## Internal Components Registry

| Component                                | Type     | Description                                                         |
| :--------------------------------------- | :------- | :------------------------------------------------------------------ |
| `raise_link_autolink_with_text_error`    | Function | Raises `ParamError` when an autolink or a bare URL gets link text.  |
| `raise_link_empty_destination_error`     | Function | Raises `ParamError` when a link has no destination.                 |
| `raise_link_image_unsupported_kind_error`| Function | Raises `ParamError` when an image is an autolink or a bare URL.     |
| `raise_link_kind_requires_label_error`   | Function | Raises `ParamError` when a reference link has no label.             |
"""
