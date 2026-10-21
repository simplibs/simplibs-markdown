from .CAUTION import CAUTION
from .IMPORTANT import IMPORTANT
from .NOTE import NOTE
from .TIP import TIP
from .WARNING import WARNING


_DESIGN_NOTES = """
# alerts presets

## Purpose
`Quote` with the alert kind filled in.

## Internal Components Registry

| Component   | Type     | Description                                          |
| :---------- | :------- | :--------------------------------------------------- |
| `CAUTION`   | Function | An alert about a negative outcome.                   |
| `IMPORTANT` | Function | An alert about information that is key to success.   |
| `NOTE`      | Function | An alert about information worth noticing.           |
| `TIP`       | Function | An alert with advice.                                |
| `WARNING`   | Function | An alert about something that needs attention.       |
"""
