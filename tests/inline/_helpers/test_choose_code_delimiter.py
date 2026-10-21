import re

import pytest
from simplibs.markdown.inline._helpers import choose_code_delimiter


@pytest.mark.parametrize(
    "code, expected",
    [
        # No backtick inside: one is enough
        ("code", ("`", "code")),
        ("", ("`", "")),
        ("a b", ("`", "a b")),
        # The delimiter is one longer than the longest run inside
        ("a`b", ("``", "a`b")),
        ("a``b", ("```", "a``b")),
        ("a`b``c", ("```", "a`b``c")),
        # A backtick at an edge would merge with the delimiter: pad
        ("`a", ("``", " `a ")),
        ("a`", ("``", " a` ")),
        ("`", ("``", " ` ")),
        ("``", ("```", " `` ")),
        # Spaces on both sides would be stripped by the parser: pad to keep them
        (" a ", ("`", "  a  ")),
        # One side only, or spaces only: nothing to protect
        (" a", ("`", " a")),
        ("a ", ("`", "a ")),
        ("   ", ("`", "   ")),
        (" ", ("`", " ")),
    ],
)
def test_choose_code_delimiter(code, expected) -> None:
    """Verify the delimiter and the padding for each shape of code."""

    assert choose_code_delimiter(code) == expected


def _read_back(delimiter: str, body: str) -> str:
    """Read an inline code span the way CommonMark does (one space stripped from each side)."""

    if body.startswith(" ") and body.endswith(" ") and body.strip(" ") != "":
        return body[1:-1]
    return body


@pytest.mark.parametrize(
    "code",
    [
        "code", "", "a`b", "a``b", "`a", "a`", "`", "``", "```x```",
        " a ", " a", "a ", "   ", " ", "` a `", "a` `b", "`` ` ``",
    ],
)
def test_choose_code_delimiter_round_trip(code) -> None:
    """Verify the span reads back as the original code."""

    delimiter, body = choose_code_delimiter(code)

    assert _read_back(delimiter, body) == code


@pytest.mark.parametrize("code", ["a`b", "a``b", "`a", "a`", "`", "``", "`` ` ``", "a`b``c"])
def test_choose_code_delimiter_is_safe(code) -> None:
    """Verify the delimiter is a run of backticks that no run inside the body can match."""

    delimiter, body = choose_code_delimiter(code)

    assert set(delimiter) == {"`"}
    assert all(len(run) != len(delimiter) for run in re.findall(r"`+", body))
    assert not body.startswith("`")
    assert not body.endswith("`")
