_DESIGN_NOTES = """
# Markdown Inline Validations Sub-Package

## Purpose
Diagnostic raisers owned by single inline elements. Each element keeps its
own folder, so a node and its failure cards are found side by side.

This package groups; it does not export. It has no imports of its own, so
importing it costs nothing and creates no import cycles.

Validations shared with other domains (`raise_param_invalid_type_error`,
`raise_block_in_inline_error`...) live in `_common/validations`.

## Internal Components Registry

| Sub-package   | Kind                | What it holds                                                      |
| :------------ | :------------------ | :----------------------------------------------------------------- |
| `emphasis`    | Diagnostic raisers  | Empty content and a marker that does not fit the kind.             |
| `entity`      | Diagnostic raisers  | Unknown name, bad code point, name and code point together.        |
| `inline_code` | Diagnostic raisers  | Empty code.                                                        |
| `link`        | Diagnostic raisers  | Missing destination or label, text on an autolink, unsupported image. |
| `math`        | Diagnostic raisers  | Empty expression.                                                  |
| `reference`   | Diagnostic raisers  | A value that does not fit the kind of reference.                   |
"""
