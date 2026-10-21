_DESIGN_NOTES = """
# Markdown Blocks Validations Sub-Package

## Purpose
Diagnostic raisers owned by single block elements. Each element keeps its
own folder, so a node and its failure cards are found side by side.

This package groups; it does not export. It has no imports of its own, so
importing it costs nothing and creates no import cycles.

Validations shared with other domains (`raise_param_invalid_type_error`,
`raise_no_blocks_error`...) live in `_common/validations`.

## Internal Components Registry

| Sub-package       | Kind               | What it holds                                                   |
| :---------------- | :----------------- | :-------------------------------------------------------------- |
| `code_block`      | Diagnostic raisers | Info string with a backtick, info on an indented block.         |
| `footnote`        | Diagnostic raisers | A label that is not usable, a reference that holds blocks.      |
| `frontmatter`     | Diagnostic raisers | A value that cannot be written as YAML.                         |
| `heading`         | Diagnostic raisers | Level out of range, setext limits, multiline or empty text.     |
| `html`            | Diagnostic raisers | Invalid tag or attribute, void tag with content, bad comment.   |
| `link_definition` | Diagnostic raisers | Empty label or destination.                                     |
| `paragraph`       | Diagnostic raisers | A paragraph without any text.                                   |
| `thematic_break`  | Diagnostic raisers | A character that is not allowed, a break that is too short.     |
"""
