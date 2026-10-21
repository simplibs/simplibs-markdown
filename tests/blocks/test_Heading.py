import re

import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Heading import Heading
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.blocks.enums import HeadingStyle
from simplibs.markdown.inline.Emphasis import Emphasis
from simplibs.markdown.inline.Text import Text

ATX = HeadingStyle.ATX
CLOSED = HeadingStyle.ATX_CLOSED
SETEXT = HeadingStyle.SETEXT


def test_heading_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = Heading("x")

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_heading_defaults() -> None:
    """Verify level 1 and the ATX style."""

    node = Heading("x")

    assert node.level == 1
    assert node.style is ATX
    assert isinstance(node.inner, Text)
    assert node.to_lines() == ("# x",)


def test_heading_keeps_an_inline_node_as_inner() -> None:
    """Verify a node given as text is not copied."""

    inner = Emphasis("x")

    assert Heading(inner).inner is inner


@pytest.mark.parametrize("level", [1, 2, 3, 4, 5, 6])
def test_heading_atx_uses_as_many_hashes_as_the_level(level) -> None:
    """Verify one hash per level."""

    assert Heading("Title", level).to_lines() == ("#" * level + " Title",)


@pytest.mark.parametrize("level", [1, 2, 3, 6])
def test_heading_atx_closed_repeats_the_hashes(level) -> None:
    """Verify the closed form."""

    hashes = "#" * level

    assert Heading("Title", level, CLOSED).to_lines() == (f"{hashes} Title {hashes}",)


@pytest.mark.parametrize(
    "text, level, expected",
    [
        ("Title", 1, ("Title", "=====")),
        ("Title", 2, ("Title", "-----")),
        # The underline is at least three characters
        ("ab", 1, ("ab", "===")),
        ("a", 2, ("a", "---")),
        ("abc", 1, ("abc", "===")),
        # ... and as long as the text
        ("a longer heading", 1, ("a longer heading", "=" * 16)),
        ("a longer heading", 2, ("a longer heading", "-" * 16)),
    ],
)
def test_heading_setext(text, level, expected) -> None:
    """Verify the text and an underline at least as long as the text."""

    assert Heading(text, level, SETEXT).to_lines() == expected


@pytest.mark.parametrize(
    "inner, expected",
    [
        ("  Title  ", "# Title"),            # edge whitespace is dropped
        ("\nTitle\n", "# Title"),
        ("a *b*", r"# a \*b\*"),             # a string is content: escaped
        (Emphasis("b"), "# *b*"),            # a node is written as it is
        (["a ", Emphasis("b")], "# a *b*"),  # a list is one inline run
        ("# x", r"# \# x"),                  # a leading '#' stays text
    ],
)
def test_heading_text(inner, expected) -> None:
    """Verify how the content of a heading is written."""

    assert Heading(inner).to_lines() == (expected,)


@pytest.mark.parametrize(
    "inner, expected",
    [
        # A closing mark needs a space before it, so a '#' that follows a letter stays as it is
        ("C#", "# C#"),
        ("C##", "# C##"),
        ("x#y", "# x#y"),
        # After a space (or alone) a run of '#' would close the heading: its last '#' is escaped
        ("a #", r"# a \#"),
        ("#", r"# \#"),
        # Only one is escaped per heading
        ("a ##", r"# a #\#"),
        ("a #  #", r"# a #  \#"),
    ],
)
def test_heading_escapes_a_trailing_hash_only_when_it_could_close_the_heading(inner, expected) -> None:
    """Verify only a '#' after a space, or a text of '#' alone, is escaped."""

    assert Heading(inner).to_lines() == (expected,)


def test_heading_trailing_escaped_hash_is_left_alone() -> None:
    """Verify a '#' that is escaped already is not escaped again."""

    node = Heading(Text(r"a \#", escape=False))

    assert node.to_lines() == (r"# a \#",)


def test_heading_closed_form_escapes_a_trailing_hash_too() -> None:
    """Verify the closing marks never merge with the text, and `C#` needs no escape here either."""

    assert Heading("a #", 2, CLOSED).to_lines() == (r"## a \# ##",)
    assert Heading("C#", 2, CLOSED).to_lines() == ("## C# ##",)


@pytest.mark.parametrize("inner", ["", "   ", "\t", Text("")])
def test_heading_empty_atx_is_the_hashes_only(inner) -> None:
    """Verify an ATX heading without text is just its marks."""

    assert Heading(inner, 2).to_lines() == ("##",)
    assert Heading(inner, 2, CLOSED).to_lines() == ("##",)


def test_heading_to_text_and_str() -> None:
    """Verify the rendered text."""

    node = Heading("Title", 2, SETEXT)

    assert node.to_text() == "Title\n-----"
    assert str(node) == "Title\n-----"
    assert repr(Heading("x")) == "Heading('# x')"


def test_heading_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Heading("x"), "__dict__")


@pytest.mark.parametrize("level", [0, 7, -1, 100, "1", 1.5, None, True, False])
def test_heading_rejects_a_level_out_of_range(subtests, level) -> None:
    """Verify the level is an integer from 1 to 6 (a bool is not)."""

    assert_exception_function(
        subtests,
        Heading,
        invalid_params=("x", level),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_LEVEL_OUT_OF_RANGE",
        value=level,
        verbose=False,
    )


@pytest.mark.parametrize("style", ["atx", None, 1, True])
def test_heading_rejects_a_style_of_the_wrong_type(subtests, style) -> None:
    """Verify `style` has to be a HeadingStyle."""

    assert_exception_function(
        subtests,
        Heading,
        invalid_params=("x", 1, style),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'style'",
        expected="HeadingStyle",
        value=style,
        verbose=False,
    )


@pytest.mark.parametrize("level", [3, 4, 5, 6])
def test_heading_rejects_a_setext_level_above_two(subtests, level) -> None:
    """Verify setext has two levels only."""

    assert_exception_function(
        subtests,
        Heading,
        invalid_params=("x", level, SETEXT),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_SETEXT_LEVEL",
        value=level,
        verbose=False,
    )


@pytest.mark.parametrize("text", ["first\nsecond", "a\r\nb", "a\n\nb", "a\n b"])
def test_heading_rejects_text_on_more_lines(subtests, text) -> None:
    """Verify a heading is one line (line breaks at the edges are only whitespace)."""

    assert_exception_function(
        subtests,
        Heading,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_MULTILINE",
        value=text,
        verbose=False,
    )


@pytest.mark.parametrize("inner", ["", "   ", "\n", Text("")])
def test_heading_rejects_a_setext_heading_without_text(subtests, inner) -> None:
    """Verify an underline alone is no heading."""

    assert_exception_function(
        subtests,
        Heading,
        invalid_params=(inner, 1, SETEXT),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_EMPTY_SETEXT",
        verbose=False,
    )


def test_heading_rejects_a_block_as_text(subtests) -> None:
    """Verify a block node cannot be the text of a heading."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        Heading,
        invalid_params=(block,),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, None, 3.14, {"a": 1}])
def test_heading_rejects_text_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        Heading,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )


# ----------------------------------------------------------------------
# What a parser reads back
# ----------------------------------------------------------------------

_ESCAPABLE = re.compile(r"\\([!-/:-@\[-`{-~])")


def _atx_text(line: str) -> str:
    """The text of an ATX heading line, read the way CommonMark does."""

    match = re.match(r"^#{1,6}(?:[ \t]+(.*?))?[ \t]*$", line)
    content = match.group(1) or ""
    # A closing sequence of '#' needs a space before it (or is all there is)
    content = re.sub(r"(?:^|[ \t]+)#+[ \t]*$", "", content)
    return _ESCAPABLE.sub(r"\1", content)


@pytest.mark.parametrize(
    "text",
    ["C#", "C##", "a #", "#", "##", "a ##", "a #  #", "x#y", "# a", "#a#", "a\\", "a\\#", "a \\#", "F# and C#", "a # b #"],
)
@pytest.mark.parametrize("style", [ATX, CLOSED])
def test_heading_text_reads_back_as_the_original(text, style) -> None:
    """Verify a parser gets the text that was given, so nothing is under-escaped."""

    line = Heading(text, 2, style).to_lines()[0]

    assert _atx_text(line) == text.strip()
