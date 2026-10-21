import pytest
from simplibs.markdown.blocks._helpers import BLOCK_START, escape_block_start

# line -> the same line escaped
ESCAPED = [
    # Headings
    ("# x", r"\# x"),
    ("###### x", r"\###### x"),
    ("#", r"\#"),
    # Quotes
    ("> x", r"\> x"),
    (">x", r"\>x"),
    # Bullet items
    ("- x", r"\- x"),
    ("+ x", r"\+ x"),
    ("* x", r"\* x"),
    ("-", r"\-"),
    # Ordered items: the backslash goes before the delimiter, not before the digit
    ("1. x", r"1\. x"),
    ("2) x", r"2\) x"),
    ("123456789. x", r"123456789\. x"),
    ("1.", r"1\."),
    # Fences
    ("```", r"\```"),
    ("```python", r"\```python"),
    ("~~~", r"\~~~"),
    ("```py title=x", r"\```py title=x"),
    ("~~~a`b", r"\~~~a`b"),
    ("~~~ `x`", r"\~~~ `x`"),
    # Thematic breaks
    ("---", r"\---"),
    ("***", r"\***"),
    ("___", r"\___"),
    # Setext underlines
    ("===", r"\==="),
    ("=", r"\="),
    # A comment
    ("<!-- x", r"\<!-- x"),
]

UNCHANGED = [
    "", "text", "a # b", "a > b", "a - b",
    "#hashtag", "-a", "1.5", "2024 was a year", "1234567890. x",
    "<div>", "=a",
    # Escaped already: not escaped twice
    r"\# x", r"\> x", r"\- x", r"1\. x", r"\---",
    # A backtick fence has no backtick in its info string: these are code spans
    "```a``b```", "``` ``x ```", "```a`", "```` a```",
]


@pytest.mark.parametrize("line, expected", ESCAPED)
def test_escape_block_start_escapes_a_block_start(line, expected) -> None:
    """Verify a line that would start a block is escaped so that it stays text."""

    assert escape_block_start(line) == expected


@pytest.mark.parametrize("line", UNCHANGED)
def test_escape_block_start_keeps_other_lines(line) -> None:
    """Verify a line that starts no block, or is escaped already, comes back as it was."""

    assert escape_block_start(line) == line


@pytest.mark.parametrize("line", [line for line, _ in ESCAPED])
def test_escape_block_start_result_starts_no_block(line) -> None:
    """Verify the escaped line is no longer read as the start of a block."""

    assert BLOCK_START.match(escape_block_start(line)) is None


@pytest.mark.parametrize("line", [line for line, _ in ESCAPED] + UNCHANGED)
def test_escape_block_start_is_idempotent(line) -> None:
    """Verify escaping twice gives the same result as escaping once."""

    once = escape_block_start(line)

    assert escape_block_start(once) == once
