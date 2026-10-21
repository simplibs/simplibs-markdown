import re

import pytest
from simplibs.markdown.blocks._helpers import YAML_PLAIN_KEY


def test_yaml_plain_key_is_a_compiled_pattern() -> None:
    """Verify the constant is a compiled regular expression."""

    assert isinstance(YAML_PLAIN_KEY, re.Pattern)


@pytest.mark.parametrize(
    "key",
    ["title", "last-updated", "_id", "a1", "A", "x_y", "Title", "a-b-c", "_", "k9"],
)
def test_yaml_plain_key_accepts(key) -> None:
    """Verify words that need no quotes."""

    assert YAML_PLAIN_KEY.fullmatch(key) is not None


@pytest.mark.parametrize(
    "key",
    [
        "",
        "1st",         # may not start with a digit
        "-a",          # nor with a hyphen
        "my key",      # no space
        "a:b",         # no colon
        "a.b",         # no dot
        "a#b",
        '"a"',
        "a,b",
        "a b c",
        # Only ASCII letters, digits, `_` and `-` are written bare
        "název",
        "živnost",
        "ábc",
        "a-č",
        "日本",
        "a_é",
    ],
)
def test_yaml_plain_key_refuses(key) -> None:
    """Verify keys that must be quoted."""

    assert YAML_PLAIN_KEY.fullmatch(key) is None
