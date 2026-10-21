import re

import pytest
from simplibs.markdown.blocks._helpers import TAG_NAME


def test_tag_name_is_a_compiled_pattern() -> None:
    """Verify the constant is a compiled regular expression."""

    assert isinstance(TAG_NAME, re.Pattern)


@pytest.mark.parametrize(
    "tag",
    ["a", "div", "h1", "my-tag", "A", "custom-element-2", "details", "x1-y2"],
)
def test_tag_name_accepts(tag) -> None:
    """Verify standard tags and custom elements are accepted."""

    assert TAG_NAME.fullmatch(tag) is not None


@pytest.mark.parametrize(
    "tag",
    [
        "",
        "1a",          # must start with a letter
        "-a",
        "a b",         # no space
        "<a>",         # no brackets
        "a_b",         # no underscore
        "a.b",
        "a:b",
        "a/",
        "a>",
        "é",           # ASCII only
    ],
)
def test_tag_name_refuses(tag) -> None:
    """Verify names that could break out of the tag are refused."""

    assert TAG_NAME.fullmatch(tag) is None
