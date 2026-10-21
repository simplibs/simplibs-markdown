from .EmphasisKind import EmphasisKind
from .EmphasisMarker import EmphasisMarker
from .LinkKind import LinkKind
from .ReferenceKind import ReferenceKind


_DESIGN_NOTES = """
# inline enums — Choices of the Inline Nodes

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component        | Type | Description                                                  |
| :--------------- | :--- | :----------------------------------------------------------- |
| `EmphasisKind`   | Enum | Emphasis, strong, both, or strike-through.                   |
| `EmphasisMarker` | Enum | The character that wraps the emphasized text.                |
| `LinkKind`       | Enum | The syntax form of a link.                                   |
| `ReferenceKind`  | Enum | The kind of automatic reference (mention, issue, commit...). |

`LineBreakStyle` is shared with `blocks`, so it lives in `_common/enums`.
"""
