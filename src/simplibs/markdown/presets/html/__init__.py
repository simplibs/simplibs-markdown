from .ANCHOR import ANCHOR
from .COMMENT import COMMENT
from .DETAILS import DETAILS
from .KBD import KBD
from .MARK import MARK
from .SUB import SUB
from .SUP import SUP


_DESIGN_NOTES = """
# html presets

## Purpose
`Html` for the tags that Markdown has no syntax for.

## Internal Components Registry

| Component | Type     | Description                                              |
| :-------- | :------- | :------------------------------------------------------- |
| `ANCHOR`  | Function | An invisible anchor to link to: `<a id="name"></a>`.     |
| `COMMENT` | Function | A comment that is not shown.                             |
| `DETAILS` | Function | A collapsible section with a summary.                    |
| `KBD`     | Function | A keyboard key: `<kbd>`.                                 |
| `MARK`    | Function | Highlighted text: `<mark>`.                              |
| `SUB`     | Function | Subscript: `<sub>`.                                      |
| `SUP`     | Function | Superscript: `<sup>`.                                    |
"""
