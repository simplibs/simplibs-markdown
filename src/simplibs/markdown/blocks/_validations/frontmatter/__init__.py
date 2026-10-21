from .raise_frontmatter_not_serializable_error import raise_frontmatter_not_serializable_error


_DESIGN_NOTES = """
# Frontmatter Validations Sub-Package

## Purpose
Diagnostic raisers for the `Frontmatter` node.

## Internal Components Registry

| Component                                | Type     | Description                                                  |
| :--------------------------------------- | :------- | :----------------------------------------------------------- |
| `raise_frontmatter_not_serializable_error`| Function | Raises `ConversionError` when a value cannot be written as YAML. |
"""
