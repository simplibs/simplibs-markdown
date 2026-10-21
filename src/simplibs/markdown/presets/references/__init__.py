from .COLOR_CHIP import COLOR_CHIP
from .COMMIT_REF import COMMIT_REF
from .EMOJI import EMOJI
from .ISSUE_REF import ISSUE_REF
from .MENTION import MENTION


_DESIGN_NOTES = """
# references presets

## Purpose
`Reference` with the kind filled in, and the color chip that GitHub draws from
a code span.

## Internal Components Registry

| Component    | Type     | Description                                          |
| :----------- | :------- | :--------------------------------------------------- |
| `COLOR_CHIP` | Function | A color code that GitHub shows with a color chip.    |
| `COMMIT_REF` | Function | A reference to a commit by its hash.                 |
| `EMOJI`      | Function | An emoji by its name: `:tada:`.                      |
| `ISSUE_REF`  | Function | A reference to an issue or a pull request: `#12`.    |
| `MENTION`    | Function | A mention of a user: `@name`.                        |
"""
