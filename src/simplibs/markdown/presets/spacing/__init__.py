from .EMPTY_LINE import EMPTY_LINE
from .HARD_BREAK import HARD_BREAK
from .RULE import RULE


_DESIGN_NOTES = """
# spacing presets

## Purpose
The nodes that are about space, not content.

## Internal Components Registry

| Component    | Type     | Description                                      |
| :----------- | :------- | :----------------------------------------------- |
| `EMPTY_LINE` | Function | One or more explicit empty lines.                |
| `HARD_BREAK` | Instance | A hard line break in the default style.          |
| `RULE`       | Instance | A horizontal rule of three dashes.               |
"""
