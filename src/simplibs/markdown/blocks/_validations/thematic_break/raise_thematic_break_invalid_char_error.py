from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_thematic_break_invalid_char_error(
    char: Any,
) -> NoReturn:
    """Raise ParamError when the character of a thematic break is not a `BreakChar`.

    Args:
        char: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="MARKDOWN_THEMATIC_BREAK_INVALID_CHAR",
        label="thematic break character",
        value=char,
        problem="Only a dash, an asterisk or an underscore can draw a thematic break.",
        expected="BreakChar.DASH, BreakChar.ASTERISK or BreakChar.UNDERSCORE.",
        how_to_fix=(
            "Pass one of the `BreakChar` members.",
            "Leave `char` out to get the dash.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_thematic_break_invalid_char_error — A Rule Drawn With the Wrong Pen

## Purpose
`===` is a setext underline and `___` is a rule only because the character
is on the short list. A free-form string would let `+++` through.
"""
