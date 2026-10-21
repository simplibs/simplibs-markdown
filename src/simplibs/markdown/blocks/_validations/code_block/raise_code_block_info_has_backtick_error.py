from typing import NoReturn
from simplibs.exception import ParamError


def raise_code_block_info_has_backtick_error(
    info: str,
) -> NoReturn:
    """Raise ParamError when the info string of a backtick fence contains a backtick.

    Args:
        info: The rejected info string.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_CODE_BLOCK_INFO_HAS_BACKTICK",
        label="code block info",
        value=info,
        problem=(
            "A backtick inside the info string would end the opening fence.",
            "The line would no longer start a code block.",
        ),
        expected="An info string without a backtick, or a tilde fence.",
        how_to_fix=(
            "Remove the backtick from the info string.",
            "Use FenceChar.TILDE for the fence.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_code_block_info_has_backtick_error — An Info String That Closes Itself

## Purpose
CommonMark forbids a backtick in the info string of a backtick fence. Tilde
fences have no such rule, which is why the second fix exists.
"""
