import re

import pytest
from simplibs.markdown.blocks._helpers import choose_fence


@pytest.mark.parametrize(
    "code, char, expected",
    [
        # No run inside: the shortest fence of three
        ("code", "`", "```"),
        ("", "`", "```"),
        ("a`b", "`", "```"),
        ("a``b", "`", "```"),
        # A run of three needs a fence of four
        ("```", "`", "````"),
        ("a ``` b", "`", "````"),
        ("````", "`", "`````"),
        # The longest run counts
        ("``` and ````", "`", "`````"),
        ("```\n````\n``", "`", "`````"),
        # Tildes
        ("code", "~", "~~~"),
        ("~~~ x", "~", "~~~~"),
        ("~~~~~", "~", "~~~~~~"),
        # Only the chosen character counts
        ("```", "~", "~~~"),
        ("~~~~~~", "`", "```"),
    ],
)
def test_choose_fence(code, char, expected) -> None:
    """Verify the fence is longer than any run of its character inside the code."""

    assert choose_fence(code, char) == expected


def test_choose_fence_default_character_is_a_backtick() -> None:
    """Verify the fence is made of backticks when no character is given."""

    assert choose_fence("code") == "```"
    assert choose_fence("```") == "````"


@pytest.mark.parametrize("char", ["`", "~"])
@pytest.mark.parametrize(
    "code",
    ["", "x", "`", "``", "```", "````", "~", "~~~", "~~~~", "a```b````c", "```\n~~~\n```", "`~`~```~~~~"],
)
def test_choose_fence_cannot_be_closed_by_the_code(code, char) -> None:
    """Verify the fence is at least three characters and no run inside the code can close it."""

    fence = choose_fence(code, char)

    assert len(fence) >= 3
    assert set(fence) == {char}
    assert all(len(run) < len(fence) for run in re.findall(re.escape(char) + "+", code))
