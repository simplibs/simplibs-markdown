from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_entity_name_xor_codepoint_error(
    name: Any,
    codepoint: Any,
) -> NoReturn:
    """Raise ParamError unless exactly one of `name` and `codepoint` is given.

    Args:
        name: The `name` argument as it was passed.
        codepoint: The `codepoint` argument as it was passed.
    """

    # 1. Say which of the two mistakes it was
    both_given = name is not None and codepoint is not None
    mistake = "Both were given." if both_given else "Neither was given."

    # 2. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_ENTITY_NAME_XOR_CODEPOINT",
        label="entity",
        value={"name": name, "codepoint": codepoint},
        problem=(
            "Exactly one of `name` and `codepoint` is required.",
            mistake,
        ),
        expected="`name` (e.g. 'copy') or `codepoint` (e.g. 169), not both.",
        how_to_fix="Pass only one of them.",
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_entity_name_xor_codepoint_error — Two Ways to Name One Character

## Purpose
`&copy;` and `&#169;` are the same character. Accepting both at once would
force the node to decide which one wins; refusing is simpler and honest.

## `value`
A small dict with both arguments, so the card shows exactly what was passed.
"""
