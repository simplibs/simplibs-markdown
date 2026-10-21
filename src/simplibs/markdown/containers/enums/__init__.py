from .AlertKind import AlertKind
from .ListMarker import ListMarker
from .TableAlign import TableAlign


_DESIGN_NOTES = """
# containers enums — Choices of the Container Nodes

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component    | Type | Description                                        |
| :----------- | :--- | :------------------------------------------------- |
| `AlertKind`  | Enum | The five GitHub alert kinds of a quote.            |
| `ListMarker` | Enum | The marker of a bullet or an ordered list.         |
| `TableAlign` | Enum | The alignment of a table column.                   |
"""
