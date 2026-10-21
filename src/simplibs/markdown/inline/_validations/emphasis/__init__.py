from .raise_emphasis_empty_inner_error import raise_emphasis_empty_inner_error
from .raise_emphasis_marker_kind_mismatch_error import raise_emphasis_marker_kind_mismatch_error


_DESIGN_NOTES = """
# Emphasis Validations Sub-Package

## Purpose
Diagnostic raisers for the `Emphasis` node.

## Internal Components Registry

| Component                                  | Type     | Description                                                        |
| :----------------------------------------- | :------- | :----------------------------------------------------------------- |
| `raise_emphasis_empty_inner_error`         | Function | Raises `ParamError` when the emphasized content is empty.          |
| `raise_emphasis_marker_kind_mismatch_error`| Function | Raises `ParamError` when the marker cannot express the kind.       |
"""
