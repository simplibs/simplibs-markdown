import random
import re

import pytest
from simplibs.markdown._common.helpers import escape_link_destination


@pytest.mark.parametrize(
    "dest",
    [
        "https://example.com/a?b=c&d=e",
        "file.pdf",
        "../docs/readme.md",
        "#anchor",
        # Balanced parentheses are fine
        "https://en.wikipedia.org/wiki/A_(b)",
        "a(b(c))d",
        "()",
        # An angle bracket that does not start the destination is fine
        "a<b",
        "a>b",
    ],
)
def test_escape_link_destination_keeps_a_safe_destination(dest) -> None:
    """Verify an ordinary destination stays readable, without angle brackets."""

    assert escape_link_destination(dest) == dest


@pytest.mark.parametrize(
    "dest, expected",
    [
        # A space or another whitespace ends a plain destination
        ("my file.pdf", "<my file.pdf>"),
        ("a\tb", "<a\tb>"),
        ("a\nb", "<a\nb>"),
        # So does a control character
        ("a\x01b", "<a\x01b>"),
        # Unbalanced parentheses
        ("f(x.html", "<f(x.html>"),
        ("f)x", "<f)x>"),
        (")(", "<)(>"),
        ("((a)", "<((a)>"),
        # Balanced parentheses do not save a destination with a space
        ("a (b) c", "<a (b) c>"),
        # An empty destination is written as an empty pair
        ("", "<>"),
    ],
)
def test_escape_link_destination_wraps_an_unsafe_destination(dest, expected) -> None:
    """Verify a destination that would end early goes between angle brackets."""

    assert escape_link_destination(dest) == expected


@pytest.mark.parametrize(
    "dest, expected",
    [
        # A leading '<' would open an angle destination by itself
        ("<a", r"<\<a>"),
        ("<a>", r"<\<a\>>"),
        # Angle brackets and backslashes inside the wrapped form are escaped
        ("my <file>.pdf", r"<my \<file\>.pdf>"),
        (r"my\file name", r"<my\\file name>"),
    ],
)
def test_escape_link_destination_escapes_inside_the_wrapper(dest, expected) -> None:
    """Verify the wrapped form escapes backslashes and angle brackets."""

    assert escape_link_destination(dest) == expected


# ----------------------------------------------------------------------
# What a parser reads back
# ----------------------------------------------------------------------

_ESCAPABLE = re.compile(r"\\([!-/:-@\[-`{-~])")


def _read_back(written: str) -> str:
    """Read a destination the way CommonMark does: without angle brackets, backslash escapes undone."""

    inner = written[1:-1] if written.startswith("<") and written.endswith(">") else written
    return _ESCAPABLE.sub(r"\1", inner)


DESTINATIONS = [
    "https://example.com/a?b=c&d=e",
    "my file.pdf",
    "a(b",
    "a)b",
    "a(b)c",
    "",
    "<a",
    "a>",
    "<a>",
    # Backslashes: before punctuation a parser reads them as escapes
    r"a\*b",
    r"a\\b",
    r"a\b",
    r"a\(b",
    r"a\)b",
    r"a\<b",
    r"a\>b",
    r"a\ b",
    r"C:\dir\f.txt",
    r"C:\*x",
    r"\\",
    "\\",
    "x\\",
    r"\\server\share",
]


@pytest.mark.parametrize("dest", DESTINATIONS)
def test_escape_link_destination_reads_back_as_the_original(dest) -> None:
    """Verify a parser gets the destination that was given (a backslash must survive)."""

    assert _read_back(escape_link_destination(dest)) == dest


@pytest.mark.parametrize("dest", DESTINATIONS)
def test_escape_link_destination_never_ends_with_a_lone_backslash(dest) -> None:
    """Verify the last backslash cannot escape the closing parenthesis or angle bracket."""

    written = escape_link_destination(dest)
    trailing = len(written) - len(written.rstrip("\\"))

    assert trailing % 2 == 0


def _samples(count: int = 600) -> list[str]:
    """The same pseudo-random destinations on every run."""

    rng = random.Random(20240602)
    alphabet = list("ab ()<>\\*_.#")
    return ["".join(rng.choices(alphabet, k=rng.randint(0, 8))) for _ in range(count)]


@pytest.mark.parametrize("dest", _samples())
def test_escape_link_destination_reads_back_for_generated_destinations(dest) -> None:
    """Verify the round trip on many destinations made of the risky characters."""

    assert _read_back(escape_link_destination(dest)) == dest
