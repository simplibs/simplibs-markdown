# Outers
from ...blocks import BlankLine


def EMPTY_LINE(count: int = 1) -> BlankLine:
    """Build one or more explicit empty lines.

    Init Params:
        count (int): The number of blank lines at this place, 1 or more.

    Markdown:
        `count` empty lines between two blocks.

    Example:
        H1("A") + EMPTY_LINE(3) + "text"
        # Writes:
        # # A
        #
        #
        #
        # text

    Note:
        Blocks are separated by one blank line already, and that separator is not added to
        this one: `EMPTY_LINE(1)` changes nothing, `EMPTY_LINE(3)` gives three blank lines
        in total.
    """
    return BlankLine(count)
