from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_link_definition_empty_destination_error(
    dest: Any,
) -> NoReturn:
    """Raise ParamError when a link definition has no destination.

    Args:
        dest: The rejected destination (`None` or an empty string).
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LINK_DEFINITION_EMPTY_DESTINATION",
        label="link definition destination",
        value=dest,
        problem="A definition exists to say where a label points.",
        expected="A non-empty URL or path.",
        how_to_fix=(
            "Pass the target as `dest`.",
            "Leave the definition out when there is no target.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_link_definition_empty_destination_error — A Label That Points Nowhere

## Purpose
`[ex]:` with nothing after it is not a definition, so every reference to
`ex` would stay plain text.
"""
