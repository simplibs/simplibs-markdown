import random
import re

import pytest
from simplibs.markdown.inline._helpers import ALWAYS_ESCAPED, LINE_START_ESCAPED, escape_text


@pytest.mark.parametrize("text", ["", "hello world", "plain text, with: punctuation! (and) more?", "   ", "a\n\nb"])
def test_escape_text_keeps_plain_text(text) -> None:
    """Verify text without special characters comes back unchanged."""

    assert escape_text(text) == text


@pytest.mark.parametrize("char", sorted(ALWAYS_ESCAPED))
def test_escape_text_escapes_always_escaped_characters_anywhere(char) -> None:
    """Verify each of these characters gets a backslash at any position."""

    assert escape_text(f"a{char}b") == f"a\\{char}b"
    assert escape_text(f"{char}ab") == f"\\{char}ab"
    assert escape_text(f"ab{char}") == f"ab\\{char}"


@pytest.mark.parametrize(
    "text, expected",
    [
        (r"\\", r"\\\\"),
        (r"a\*", r"a\\\*"),
        ("**bold**", r"\*\*bold\*\*"),
        ("snake_case", r"snake\_case"),
        ("a & b", r"a \& b"),
        ("[link](url)", r"\[link\](url)"),
        ("<b>x</b>", r"\<b\>x\</b\>"),
        ("$x$", r"\$x\$"),
    ],
)
def test_escape_text_mixed_characters(text, expected) -> None:
    """Verify some typical texts, including the cautious extra backslashes."""

    assert escape_text(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("# heading", r"\# heading"),
        ("+ item", r"\+ item"),
        ("- item", r"\- item"),
        ("= underline", r"\= underline"),
        ("---", r"\---"),
        ("#hashtag", r"\#hashtag"),
        # Only the first character of the line is escaped
        ("## two", r"\## two"),
    ],
)
def test_escape_text_escapes_a_line_start_mark(text, expected) -> None:
    """Verify a heading, list or underline mark at the line start is escaped."""

    assert escape_text(text) == expected


@pytest.mark.parametrize("text", ["a # b", "a + b", "a - b", "a = b", "well-known", "C#", "1+1=2"])
def test_escape_text_keeps_a_line_start_mark_in_the_middle(text) -> None:
    """Verify the same characters inside a line stay as they are."""

    assert escape_text(text) == text


@pytest.mark.parametrize(
    "text, expected",
    [
        ("  # x", r"  \# x"),
        ("    - x", r"    \- x"),
        ("  3. x", r"  3\. x"),
    ],
)
def test_escape_text_judges_the_line_start_after_the_indentation(text, expected) -> None:
    """Verify the indentation is kept and the mark behind it is escaped."""

    assert escape_text(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("1. x", r"1\. x"),
        ("2) x", r"2\) x"),
        ("123456789. x", r"123456789\. x"),
        # Ten digits are not a list marker in CommonMark
        ("1234567890. x", "1234567890. x"),
        # No dot or parenthesis after the number
        ("2024 was a year", "2024 was a year"),
        # Not at the line start
        ("see 1. x", "see 1. x"),
    ],
)
def test_escape_text_escapes_an_ordered_list_marker(text, expected) -> None:
    """Verify a number followed by '.' or ')' at the line start cannot start a list."""

    assert escape_text(text) == expected


def test_escape_text_works_line_by_line() -> None:
    """Verify every line is judged on its own."""

    assert escape_text("a\n# b\n1. c\n- d") == "a\n" + r"\# b" + "\n" + r"1\. c" + "\n" + r"\- d"


def test_escape_text_keeps_blank_lines_and_line_count() -> None:
    """Verify the number of lines never changes."""

    text = "a\n\n# b\n   \nc"

    assert escape_text(text).count("\n") == text.count("\n")


# ----------------------------------------------------------------------
# Properties, checked on many generated texts
# ----------------------------------------------------------------------

_ALPHABET = list("ab1 .)#+-=*_`[]<>&~$\\\n")
_ESCAPABLE = re.compile(r"\\([!-/:-@\[-`{-~])")


def _samples(count: int = 600) -> list[str]:
    """The same pseudo-random texts on every run."""

    rng = random.Random(20240601)
    return ["".join(rng.choices(_ALPHABET, k=rng.randint(0, 12))) for _ in range(count)]


@pytest.mark.parametrize("text", _samples())
def test_escape_text_reads_back_as_the_original(text) -> None:
    """Verify removing the backslash escapes gives the original text again."""

    assert _ESCAPABLE.sub(r"\1", escape_text(text)) == text


@pytest.mark.parametrize("text", _samples(200))
def test_escape_text_leaves_nothing_unescaped(text) -> None:
    """Verify no special character and no line-start mark is left bare."""

    escaped = escape_text(text)

    without_pairs = re.sub(r"\\.", "", escaped, flags=re.DOTALL)
    assert not (set(without_pairs) & ALWAYS_ESCAPED)

    for line in escaped.split("\n"):
        body = line.lstrip(" ")
        assert not body or body[0] not in LINE_START_ESCAPED
        assert re.match(r"\d{1,9}[.)]", body) is None
