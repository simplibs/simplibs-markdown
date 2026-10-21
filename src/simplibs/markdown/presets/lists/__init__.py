from .BULLET_LIST import BULLET_LIST
from .DONE_ITEM import DONE_ITEM
from .NUMBERED_LIST import NUMBERED_LIST
from .TASK_ITEM import TASK_ITEM


_DESIGN_NOTES = """
# lists presets

## Purpose
`List` and `ListItem` with the kind and the checkbox filled in.

## Internal Components Registry

| Component       | Type     | Description                                     |
| :-------------- | :------- | :---------------------------------------------- |
| `BULLET_LIST`   | Function | A bullet list.                                  |
| `DONE_ITEM`     | Function | A list item with a checked checkbox.            |
| `NUMBERED_LIST` | Function | A numbered list.                                |
| `TASK_ITEM`     | Function | A list item with an empty checkbox.             |
"""
