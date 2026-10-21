# Constants
from .constants.ALWAYS_ESCAPED import ALWAYS_ESCAPED
from .constants.EMPHASIS_REPEAT import EMPHASIS_REPEAT
from .constants.LINE_BREAKS import LINE_BREAKS
from .constants.LINE_START_ESCAPED import LINE_START_ESCAPED
from .constants.REFERENCE_FORMS import REFERENCE_FORMS
# Functions
from .choose_code_delimiter import choose_code_delimiter
from .escape_text import escape_text


_DESIGN_NOTES = """
# Markdown Inline Helpers Sub-Package

## Purpose
Private helpers and constants of the inline nodes. What a second domain needs
lives in `_common/helpers`.

## Internal Components Registry

| Component               | Type     | Description                                                   |
| :---------------------- | :------- | :------------------------------------------------------------ |
| `ALWAYS_ESCAPED`        | Constant | Characters escaped everywhere in text.                        |
| `choose_code_delimiter` | Function | Picks the backtick run that fits a piece of code.             |
| `EMPHASIS_REPEAT`       | Constant | How many times each emphasis kind repeats its marker.         |
| `escape_text`           | Function | Escapes everything in a text that Markdown could read as formatting. |
| `LINE_BREAKS`           | Constant | The text of each line break style.                            |
| `LINE_START_ESCAPED`    | Constant | Characters escaped only at the start of a line.               |
| `REFERENCE_FORMS`       | Constant | Pattern, template and description of each reference kind.     |
"""
