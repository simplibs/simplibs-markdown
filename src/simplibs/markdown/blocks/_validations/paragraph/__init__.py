from .raise_paragraph_empty_error import raise_paragraph_empty_error


_DESIGN_NOTES = """
# Paragraph Validations Sub-Package

## Purpose
Diagnostic raisers for the `Paragraph` node.

## Internal Components Registry

| Component                    | Type     | Description                                           |
| :--------------------------- | :------- | :---------------------------------------------------- |
| `raise_paragraph_empty_error`| Function | Raises `ParamError` when a paragraph has no text.     |
"""
