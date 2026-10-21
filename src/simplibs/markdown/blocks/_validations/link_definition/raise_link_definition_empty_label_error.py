from typing import NoReturn
from simplibs.exception import ParamError


def raise_link_definition_empty_label_error() -> NoReturn:
    """Raise ParamError when a link definition has an empty label."""

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LINK_DEFINITION_EMPTY_LABEL",
        label="link definition label",
        problem=(
            "A definition is found by its label.",
            "An empty label cannot be referenced.",
        ),
        expected="A label with at least one visible character.",
        how_to_fix="Pass the label that the reference links use.",
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_link_definition_empty_label_error — A Definition Nobody Can Name

## Purpose
`[]: https://x.y` is not a definition. The label is judged after whitespace
is collapsed, so `"   "` is empty too.

## No `value`
The original label is already normalized when the check runs, so the card
would only print an empty string.
"""
