import pytest
from simplibs.markdown.containers._helpers import escape_pipes


@pytest.mark.parametrize(
    "text, expected",
    [
        # No pipe, nothing to do
        ("", ""),
        ("no pipes", "no pipes"),
        (r"a\b", r"a\b"),
        # A bare pipe is escaped, wherever it stands
        ("a|b", r"a\|b"),
        ("|a", r"\|a"),
        ("a|", r"a\|"),
        ("|", r"\|"),
        ("a||b", r"a\|\|b"),
        # One backslash before the pipe: it is escaped already
        (r"a\|b", r"a\|b"),
        # Two backslashes are an escaped backslash, so the pipe is bare
        (r"a\\|b", r"a\\\|b"),
        # Three: the last one escapes the pipe
        (r"a\\\|b", r"a\\\|b"),
        # Four: an escaped backslash twice, the pipe is bare
        (r"a\\\\|b", r"a\\\\\|b"),
        # A mix
        (r"a|b\|c|d", r"a\|b\|c\|d"),
    ],
)
def test_escape_pipes(text, expected) -> None:
    """Verify a pipe is escaped exactly when an even number of backslashes stands before it."""

    assert escape_pipes(text) == expected


@pytest.mark.parametrize(
    "text",
    ["a|b", r"a\|b", r"a\\|b", r"a\\\|b", "||", r"|\|\\|", ""],
)
def test_escape_pipes_is_idempotent(text) -> None:
    """Verify escaping twice gives the same result as escaping once."""

    once = escape_pipes(text)

    assert escape_pipes(once) == once


@pytest.mark.parametrize(
    "text",
    ["a|b", r"a\|b", r"a\\|b", r"a\\\|b", r"a\\\\|b", "||", r"|\|\\|", "x"],
)
def test_escape_pipes_leaves_no_bare_pipe(text) -> None:
    """Verify every pipe in the result has an odd number of backslashes before it."""

    result = escape_pipes(text)

    backslashes = 0
    for char in result:
        if char == "|":
            assert backslashes % 2 == 1
        backslashes = backslashes + 1 if char == "\\" else 0
