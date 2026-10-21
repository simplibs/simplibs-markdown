from .InlineMarkdown import InlineMarkdown
from .Markdown import Markdown


_DESIGN_NOTES = """
# base_class — The Two Bases of Every Node

## Purpose
The abstract roots of the node tree. `Markdown` is the contract every node
fulfils (`to_lines`, `to_text`, `+`). `InlineMarkdown` is the shortcut for
nodes that live inside a line and render as one string.

Plain imports, no `__all__` — the package root decides what is public.

## Layering
`base_class` knows no concrete node. The one place where `+` has to name
`Text`, `Paragraph` or `Document` is `add_nodes` in `_common/helpers`, which
imports them lazily.

## Internal Components Registry

| Component        | Type           | Description                                                    |
| :--------------- | :------------- | :------------------------------------------------------------ |
| `InlineMarkdown` | Abstract class | Base of nodes inside a line; renders through `to_inline()`.    |
| `Markdown`       | Abstract class | Base of every node: `to_lines()`, `to_text()` and `+`.         |
| `enums`          | Sub-package    | `NodeLevel`.                                                   |
"""
