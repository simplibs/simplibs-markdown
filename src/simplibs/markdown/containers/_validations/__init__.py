_DESIGN_NOTES = """
# Markdown Containers Validations Sub-Package

## Purpose
Diagnostic raisers owned by single container elements. Each element keeps its
own folder, so a node and its failure cards are found side by side.

This package groups; it does not export. It has no imports of its own, so
importing it costs nothing and creates no import cycles.

Validations shared with other domains (`raise_param_invalid_type_error`,
`raise_no_blocks_error`...) live in `_common/validations`.

## Internal Components Registry

| Sub-package | Kind               | What it holds                                                      |
| :---------- | :----------------- | :----------------------------------------------------------------- |
| `list`      | Diagnostic raisers | Start number, marker mismatch, unusable or missing items.          |
| `list_item` | Diagnostic raisers | A task item without a paragraph.                                   |
| `quote`     | Diagnostic raisers | An unknown alert kind.                                             |
| `table`     | Diagnostic raisers | Missing columns, rows and alignments of the wrong width, multiline cells. |
"""
