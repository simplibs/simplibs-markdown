from .BlankLine import BlankLine
from .CodeBlock import CodeBlock
from .Footnote import Footnote
from .Frontmatter import Frontmatter
from .Heading import Heading
from .Html import Html
from .LinkDefinition import LinkDefinition
from .Paragraph import Paragraph
from .ThematicBreak import ThematicBreak


_DESIGN_NOTES = """
# blocks — Nodes That Are Lines of Their Own

## Purpose
Headings, paragraphs, code, rules, definitions and the other leaf blocks.
A block is separated from its neighbours by a blank line, which the
containers add.

Plain imports, no `__all__` — the package root decides what is public.

## Internal Components Registry

| Component        | Type        | Description                                                    |
| :--------------- | :---------- | :------------------------------------------------------------- |
| `BlankLine`      | Node        | One or more explicit empty lines.                              |
| `CodeBlock`      | Node        | A fenced or indented block of code.                            |
| `Footnote`       | Node        | A footnote marker (inline) or a footnote definition (block).   |
| `Frontmatter`    | Node        | A YAML header between two `---` lines.                         |
| `Heading`        | Node        | A heading of level 1 to 6 in one of three styles.              |
| `Html`           | Node        | A raw HTML block, an inline tag or a comment.                  |
| `LinkDefinition` | Node        | The target of reference links: `[label]: destination`.         |
| `Paragraph`      | Node        | One or more lines of inline content.                           |
| `ThematicBreak`  | Node        | A horizontal rule.                                             |
| `_helpers`       | Sub-package | Private helpers and constants of the nodes.                    |
| `_validations`   | Sub-package | Diagnostic raisers of single nodes.                            |
| `enums`          | Sub-package | `BreakChar`, `FenceChar`, `FootnoteRole`, `HeadingStyle`, `HtmlMode`. |
"""
