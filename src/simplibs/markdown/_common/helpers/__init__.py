from .add_nodes import add_nodes
from .as_inline import as_inline
from .flatten_blocks import flatten_blocks
from .prefix_lines import prefix_lines
from .separate_blocks import separate_blocks
from .escape_link_title import escape_link_title
from .escape_link_destination import escape_link_destination
from .escape_label import escape_label
from .normalize_label import normalize_label


_DESIGN_NOTES = """
# Markdown Common Helpers Sub-Package

## Purpose
Internal helpers used by more than one domain. None of them imports a node
module at import time — see the import rule in `_common`.

## Internal Components Registry

| Component                 | Type     | Description                                                          |
| :------------------------ | :------- | :------------------------------------------------------------------- |
| `add_nodes`               | Function | Composes two operands of `+` into an inline join or a document.      |
| `as_inline`               | Function | Turns a string, an inline node or a list of them into one inline node. |
| `flatten_blocks`          | Function | Turns anything fit for a block slot into a flat tuple of blocks.     |
| `prefix_lines`            | Function | Puts a prefix before every line (first line and the rest may differ). |
| `separate_blocks`         | Function | Renders blocks as lines with blank lines between them.               |
| `escape_link_title`       | Function | Writes a link title with the quotes that fit it.                     |
| `escape_link_destination` | Function | Writes a link destination so that it survives parsing.               |
| `escape_label`            | Function | Writes a link label so that its brackets and backslashes do not end it. |
| `normalize_label`         | Function | Collapses whitespace in a link or footnote label.                    |
"""
