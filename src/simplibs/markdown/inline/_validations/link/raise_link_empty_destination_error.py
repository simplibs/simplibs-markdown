from typing import Any, NoReturn, TYPE_CHECKING
from simplibs.exception import ParamError
# Annotations
if TYPE_CHECKING:
    from ...enums import LinkKind


def raise_link_empty_destination_error(
    kind: "LinkKind",
    dest: Any,
) -> NoReturn:
    """Raise ParamError when a link has no destination.

    Args:
        kind: The kind of the link being built.
        dest: The rejected destination (`None` or an empty string).
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LINK_EMPTY_DESTINATION",
        label="link destination",
        value=dest,
        problem=f"A link of kind {kind.name} needs a destination.",
        expected="A non-empty URL or path.",
        how_to_fix=(
            "Pass the target as `dest`.",
            "Leave the link out when there is nowhere to point.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_link_empty_destination_error — A Link That Goes Nowhere

## Purpose
`[text]()` is valid Markdown and a dead link. Inline links, autolinks and
bare URLs all need a destination, so one card with the `kind` serves them.
Reference links keep the destination in a `LinkDefinition`, not here.
"""
