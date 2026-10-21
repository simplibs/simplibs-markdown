from .MarkdownText import MarkdownText
from .to_file import to_file


_DESIGN_NOTES = """
# output — From a Node to Text and to a File

## Purpose
The last layer. A node becomes a `MarkdownText` (text, lines, a file), or goes
straight into a file.

Plain imports, no `__all__` — the package root decides what is public.

## Dependency
The only place of the library that uses another `simplibs` library:
`simplibs-file` (`write_text`).

## Internal Components Registry

| Component      | Type     | Description                                                       |
| :------------- | :------- | :---------------------------------------------------------------- |
| `MarkdownText` | Class    | The finished text of a node: `str`, lines, `len`, `to_file()`.    |
| `to_file`      | Function | Writes a string, a node or a `MarkdownText` to a file.            |
"""
