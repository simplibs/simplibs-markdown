from html import escape as html_escape
from typing import Any


def build_html_open_tag(tag: str, attrs: dict[str, Any]) -> str:
    """Write the opening tag of an HTML element.

    Args:
        tag: The tag name.
        attrs: The attributes. `True` writes a bare attribute (`open`);
            `None` and `False` leave the attribute out.

    Returns:
        The opening tag, e.g. `<a id="top">`.
    """

    # 1. The tag name comes first
    parts = [tag]

    # 2. Then the attributes in the given order
    for name, value in attrs.items():

        # 2.1 A flag is written without a value
        if value is True:
            parts.append(name)

        # 2.2 Nothing to write
        elif value is None or value is False:
            continue

        # 2.3 A value is escaped and quoted
        else:
            parts.append(f'{name}="{html_escape(str(value), quote=True)}"')

    return "<" + " ".join(parts) + ">"


_DESIGN_NOTES = """
# build_html_open_tag — Attributes That Cannot Break the Tag

## Purpose
`Html("a", attrs={"title": 'say "hi"'})` has to stay one valid tag. The value
is escaped with `html.escape(..., quote=True)`.

## `True`, `False` and `None`
HTML flags (`open`, `hidden`) are written as bare names, so `True` does that.
`False` and `None` mean "not set" and leave the attribute out, which lets a
caller pass a condition directly.
"""
