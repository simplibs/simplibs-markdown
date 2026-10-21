from .Emphasis import Emphasis
from .Entity import Entity
from .InlineCode import InlineCode
from .InlineJoin import InlineJoin
from .LineBreak import LineBreak
from .Link import Link
from .Math import Math
from .Reference import Reference
from .Text import Text


_DESIGN_NOTES = """
# inline — Nodes Inside a Line

## Purpose
Everything that can stand inside a line of text. Inline nodes are joined with
`+` into an `InlineJoin`, and can be the content of a heading, a paragraph, a
table cell or a list item.

Plain imports, no `__all__` — the package root decides what is public.

## Internal Components Registry

| Component      | Type        | Description                                                   |
| :------------- | :---------- | :------------------------------------------------------------ |
| `Emphasis`     | Node        | Emphasis, strong, both, or strike-through around content.     |
| `Entity`       | Node        | An HTML entity by name or by code point.                      |
| `InlineCode`   | Node        | A code span with a delimiter that fits its content.           |
| `InlineJoin`   | Node        | Several inline nodes written one after another.               |
| `LineBreak`    | Node        | A hard line break in one of three styles.                     |
| `Link`         | Node        | A link or an image in any of six forms.                       |
| `Math`         | Node        | An inline or display math expression.                         |
| `Reference`    | Node        | A mention, an issue, a commit or an emoji.                    |
| `Text`         | Node        | Plain text, escaped by default.                               |
| `_helpers`     | Sub-package | Private helpers and constants of the nodes.                   |
| `_validations` | Sub-package | Diagnostic raisers of single nodes.                           |
| `enums`        | Sub-package | `EmphasisKind`, `EmphasisMarker`, `LinkKind`, `ReferenceKind`. |
"""
