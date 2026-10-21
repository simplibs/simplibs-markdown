_DESIGN_NOTES = """
# Markdown Common Package

## Purpose
Everything that more than one domain (`base_class`, `inline`, `blocks`,
`containers`, `output`) needs: shared helpers, shared enums and shared
diagnostic raisers.

This package groups; it does not export. It has no imports of its own, so
importing it costs nothing and creates no import cycles.

## Placement Rule
Whatever only one element uses stays in that element's private folder
(`_helpers/`, `_validations/`). Once a second domain needs it, it moves here.

## Import Rule — `_common` Never Imports Upward at Import Time
Some helpers have to name nodes from the layers above them (`add_nodes`
builds a `Paragraph`, `flatten_blocks` recognizes a `Document`). They do it
inside the function body, so importing `_common` never loads a node module
and the module-level import graph has no cycle:

    _common  <-  base_class  <-  inline  <-  blocks  <-  containers  <-  output

These lazy imports are marked with the comment `# Lazy (upward)`.

## Internal Components Registry

| Sub-package   | Kind                    | What it holds                                                          |
| :------------ | :---------------------- | :--------------------------------------------------------------------- |
| `enums`       | Shared enums            | `LineBreakStyle`.                                                      |
| `helpers`     | Shared internal helpers | `add_nodes`, `as_inline`, `escape_label`, `escape_link_destination`, `escape_link_title`, `flatten_blocks`, `normalize_label`, `prefix_lines`, `separate_blocks`. |
| `validations` | Diagnostic raisers      | `raise_param_invalid_type_error`, `raise_node_not_markdown_error`, `raise_block_in_inline_error`, `raise_no_blocks_error`. |
"""
