import pytest
from simplibs.markdown._common.helpers import prefix_lines


@pytest.mark.parametrize(
    "lines, first, rest, expected",
    [
        # No lines, no result
        ((), "> ", None, ()),
        # `rest` defaults to `first`
        (("a", "b"), "> ", None, ("> a", "> b")),
        (("a",), "> ", None, ("> a",)),
        # The first line carries the marker, the others are indented
        (("a", "b", "c"), "- ", "  ", ("- a", "  b", "  c")),
        # A footnote: marker first, four spaces after
        (("a", "b"), "[^1]: ", "    ", ("[^1]: a", "    b")),
        # An empty line keeps the prefix but loses the spaces behind it
        (("a", "", "b"), "> ", None, ("> a", ">", "> b")),
        # A prefix of spaces only becomes a truly empty line
        (("a", "", "b"), "- ", "  ", ("- a", "", "  b")),
        # An empty FIRST line uses the stripped first prefix
        (("", "x"), "- ", "  ", ("-", "  x")),
        # An explicit empty `rest` is not the same as None
        (("a", "b"), "> ", "", ("> a", "b")),
        # Leading spaces of a line are kept
        (("  a",), "> ", None, (">   a",)),
    ],
)
def test_prefix_lines(lines, first, rest, expected) -> None:
    """Verify the first line gets `first`, the others `rest`, and empty lines are not padded."""

    assert prefix_lines(lines, first, rest) == expected


def test_prefix_lines_returns_a_tuple() -> None:
    """Verify the result is a tuple, whatever iterable went in."""

    assert isinstance(prefix_lines(["a", "b"], "> "), tuple)


def test_prefix_lines_accepts_a_generator() -> None:
    """Verify any iterable of lines works, a generator included."""

    assert prefix_lines((line for line in ("a", "b")), "- ", "  ") == ("- a", "  b")


def test_prefix_lines_does_not_change_its_input() -> None:
    """Verify the given list is left as it was."""

    lines = ["a", "", "b"]
    prefix_lines(lines, "> ")
    assert lines == ["a", "", "b"]


def test_prefix_lines_nests_from_the_inside_out() -> None:
    """Verify applying it twice gives the nesting of Markdown (a quote inside a list item)."""

    inner = prefix_lines(("a", "b"), "> ")
    outer = prefix_lines(inner, "- ", "  ")
    assert outer == ("- > a", "  > b")
