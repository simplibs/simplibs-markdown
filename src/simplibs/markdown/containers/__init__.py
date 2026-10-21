from .Document import Document
from .List import List
from .ListItem import ListItem
from .Quote import Quote
from .Table import Table


_DESIGN_NOTES = """
# containers — Nodes That Hold Other Blocks

## Purpose
Quotes, lists, tables and the document itself. A container accepts strings,
inline nodes and block nodes in its slots and turns them into blocks with
`flatten_blocks`; it writes them with `separate_blocks` and `prefix_lines`.

Plain imports, no `__all__` — the package root decides what is public.

## Internal Components Registry

| Component      | Type        | Description                                                   |
| :------------- | :---------- | :------------------------------------------------------------ |
| `Document`     | Node        | A whole document: blocks separated by blank lines.            |
| `List`         | Node        | A bullet or an ordered list of items.                         |
| `ListItem`     | Node        | One item of a list, with any blocks and an optional checkbox. |
| `Quote`        | Node        | A block quote, optionally a GitHub alert.                     |
| `Table`        | Node        | A table with a header, rows and column alignment.             |
| `_helpers`     | Sub-package | Private helpers of the table.                                 |
| `_validations` | Sub-package | Diagnostic raisers of single nodes.                           |
| `enums`        | Sub-package | `AlertKind`, `ListMarker`, `TableAlign`.                      |
"""
