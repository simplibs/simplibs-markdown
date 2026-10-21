import re

import pytest
from simplibs.markdown.blocks._helpers import ATTR_NAME


def test_attr_name_is_a_compiled_pattern() -> None:
    """Verify the constant is a compiled regular expression."""

    assert isinstance(ATTR_NAME, re.Pattern)


@pytest.mark.parametrize(
    "name",
    ["id", "class", "data-x", "_a", ":a", "a.b", "xlink:href", "A1", "a_b-c.d", "x"],
)
def test_attr_name_accepts(name) -> None:
    """Verify names that the HTML specification allows."""

    assert ATTR_NAME.fullmatch(name) is not None


@pytest.mark.parametrize(
    "name",
    [
        "",
        "1a",          # may not start with a digit
        "-a",          # nor with a hyphen
        ".a",          # nor with a dot
        "a b",         # no space: it would end the attribute
        'a"b',         # no quote: it would end the value
        "a'b",
        "a=b",         # no '=': it would start the value
        "a>b",         # no '>': it would end the tag
        "a/b",
        "é",           # ASCII only
    ],
)
def test_attr_name_refuses(name) -> None:
    """Verify names that could break the tag are refused."""

    assert ATTR_NAME.fullmatch(name) is None
