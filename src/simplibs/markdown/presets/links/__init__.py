from .AUTOLINK import AUTOLINK
from .BARE_URL import BARE_URL
from .IMAGE import IMAGE


_DESIGN_NOTES = """
# links presets

## Purpose
`Link` with the kind or the image flag filled in. A plain link needs no preset:
`Link(text, destination)` is already short.

## Internal Components Registry

| Component  | Type     | Description                                  |
| :--------- | :------- | :------------------------------------------- |
| `AUTOLINK` | Function | A destination in angle brackets: `<url>`.    |
| `BARE_URL` | Function | A destination written as it is.              |
| `IMAGE`    | Function | An image: `![alt](source "title")`.          |
"""
