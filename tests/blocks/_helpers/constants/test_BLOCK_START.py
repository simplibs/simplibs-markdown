import re

import pytest
from simplibs.markdown.blocks._helpers import BLOCK_START


def test_block_start_is_a_compiled_pattern() -> None:
    """Verify the constant is a compiled regular expression."""

    assert isinstance(BLOCK_START, re.Pattern)


@pytest.mark.parametrize(
    "line",
    [
        # Headings: one to six marks, then a space or the end
        "# x", "#", "###### x", "## ",
        # A quote
        "> x", ">x", ">",
        # Bullet items
        "- x", "+ x", "* x", "-", "+", "*",
        # Ordered items
        "1. x", "2) x", "123456789. x", "1.", "7)",
        # Fences
        "```", "```python", "````", "~~~", "~~~~ x",
        # Thematic breaks
        "---", "***", "___", "- - -", "* * *", "_ _ _", "-- -", "----------",
        # Setext underlines
        "===", "=", "== ",
        # A comment
        "<!-- x",
        # Up to three spaces of indentation
        " # x", "  - x", "   1. x",
    ],
)
def test_block_start_matches(line) -> None:
    """Verify a line that Markdown reads as the start of a block is found."""

    assert BLOCK_START.match(line) is not None


@pytest.mark.parametrize(
    "line",
    [
        "", "text", "a # b", "a > b", "a - b",
        # The mark needs a space after it
        "#hashtag", "-a", "+a", "*a", "1.5", "2024", "1.x",
        # Seven marks are no heading
        "####### x",
        # Ten digits are no list marker
        "1234567890. x",
        # Two characters are no thematic break or fence
        "--", "``", "~~",
        # A line that is only a part of an equal sign
        "=a", "==x",
        # Other HTML
        "<div>", "<!- x",
        # Four spaces are an indented code block, which is no concern of this pattern
        "    # x",
        # An escaped line
        r"\# x", r"\> x", r"1\. x", r"\- x",
    ],
)
def test_block_start_does_not_match(line) -> None:
    """Verify an ordinary line, or one that is escaped already, is left alone."""

    assert BLOCK_START.match(line) is None


@pytest.mark.parametrize(
    "line",
    [
        # A backtick fence has no backtick in its info string, so these are code spans, not fences
        "```a``b```",
        "``` ``x ```",
        "```a`",
        "```py`thon",
        "```` a```",
    ],
)
def test_block_start_a_backtick_run_followed_by_more_backticks_is_no_fence(line) -> None:
    """Verify the line stays text (an inline code span that happens to start the line)."""

    assert BLOCK_START.match(line) is None


@pytest.mark.parametrize(
    "line",
    [
        # A real backtick fence, with or without an info string
        "```py title=x",
        "``` ",
        "```   ",
        "`````",
        "```a b",
        # A tilde fence may have a backtick in its info string
        "~~~a`b",
        "~~~ `x`",
        "~~~~ a``b```",
    ],
)
def test_block_start_real_fences_are_still_found(line) -> None:
    """Verify the narrower rule for backticks does not hide a real fence."""

    assert BLOCK_START.match(line) is not None
