import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown._common.enums import LineBreakStyle
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.inline.Emphasis import Emphasis
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Text import Text

SPACES = LineBreakStyle.SPACES
BACKSLASH = LineBreakStyle.BACKSLASH
HTML = LineBreakStyle.HTML


def _make(lines, options: dict) -> Paragraph:
    """Create a Paragraph from lines and keyword options."""

    return Paragraph(*lines, **options)


def test_paragraph_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = Paragraph("a")

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_paragraph_stores_one_inline_node_per_line() -> None:
    """Verify the arguments become inline nodes, a node is kept as it is."""

    node_given = Text("b")

    node = Paragraph("a", node_given)

    assert len(node.lines) == 2
    assert isinstance(node.lines[0], Text)
    assert node.lines[1] is node_given
    assert node.break_style is None


@pytest.mark.parametrize(
    "lines, expected",
    [
        (("a",), ("a",)),
        (("a", "b"), ("a", "b")),
        (("a", "b", "c"), ("a", "b", "c")),
        # Empty lines are dropped, they would end the paragraph
        (("a", "", "b"), ("a", "b")),
        (("", "a", ""), ("a",)),
        (("a", "   ", "b"), ("a", "b")),
        # Indentation would make a code block
        (("   a",), ("a",)),
        (("a", "    b"), ("a", "b")),
        # A line with a line break inside is more lines
        (("a\nb",), ("a", "b")),
        (("a\n\nb",), ("a", "b")),
    ],
)
def test_paragraph_lines(lines, expected) -> None:
    """Verify the lines, without indentation and without empty lines."""

    assert Paragraph(*lines).to_lines() == expected


def test_paragraph_text_is_escaped() -> None:
    """Verify a string is content: nothing in it is read as formatting."""

    assert Paragraph("a*b").to_lines() == (r"a\*b",)
    assert Paragraph("2024. was a year").to_lines() == (r"2024\. was a year",)
    assert Paragraph("# not a heading").to_lines() == (r"\# not a heading",)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("# heading", r"\# heading"),
        ("> quote", r"\> quote"),
        ("- item", r"\- item"),
        ("1. item", r"1\. item"),
        ("```", r"\```"),
        ("---", r"\---"),
        ("<!-- x", r"\<!-- x"),
    ],
)
def test_paragraph_escapes_a_raw_line_that_would_start_a_block(raw, expected) -> None:
    """Verify the second line of defence: raw text cannot turn a paragraph into something else."""

    assert Paragraph(Text(raw, escape=False)).to_lines() == (expected,)


def test_paragraph_keeps_raw_text_that_starts_no_block() -> None:
    """Verify raw Markdown that is safe is left alone."""

    assert Paragraph(Text("some *emphasis*", escape=False)).to_lines() == ("some *emphasis*",)


def test_paragraph_a_line_may_be_built_with_plus() -> None:
    """Verify inline nodes joined with `+` are one line."""

    assert Paragraph("See " + Emphasis("this") + ".").to_lines() == ("See *this*.",)


def test_paragraph_a_list_is_one_line() -> None:
    """Verify a list of inline items is one line."""

    assert Paragraph(["a ", Emphasis("b")]).to_lines() == ("a *b*",)


@pytest.mark.parametrize(
    "style, lines, expected",
    [
        (SPACES, ("a", "b"), ("a  ", "b")),
        (BACKSLASH, ("a", "b"), ("a\\", "b")),
        (HTML, ("a", "b"), ("a<br>", "b")),
        # Every line but the last
        (SPACES, ("a", "b", "c"), ("a  ", "b  ", "c")),
        (HTML, ("a", "b", "c"), ("a<br>", "b<br>", "c")),
        # One line, nothing to break
        (SPACES, ("a",), ("a",)),
        (BACKSLASH, ("a",), ("a",)),
        # A line with a line break inside counts as lines
        (SPACES, ("a\nb",), ("a  ", "b")),
        # Dropped empty lines do not get a break
        (BACKSLASH, ("a", "", "b"), ("a\\", "b")),
    ],
)
def test_paragraph_break_style(style, lines, expected) -> None:
    """Verify a hard break at the end of every line but the last."""

    node = Paragraph(*lines, break_style=style)

    assert node.break_style is style
    assert node.to_lines() == expected


def test_paragraph_to_text_and_str() -> None:
    """Verify the rendered text."""

    node = Paragraph("a", "b")

    assert node.to_text() == "a\nb"
    assert str(node) == "a\nb"
    assert repr(Paragraph("a")) == "Paragraph('a')"


def test_paragraph_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Paragraph("a"), "__dict__")


@pytest.mark.parametrize("lines", [(), ("",), ("  ", "\t"), ("", Text("")), ("\n",), ([],)])
def test_paragraph_rejects_no_visible_text(subtests, lines) -> None:
    """Verify a paragraph needs at least one line with text."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(lines, {}),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAGRAPH_EMPTY",
        verbose=False,
    )


@pytest.mark.parametrize("style", ["spaces", "html", 1, True, "  "])
def test_paragraph_rejects_a_break_style_of_the_wrong_type(subtests, style) -> None:
    """Verify `break_style` has to be a LineBreakStyle."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(("a", "b"), {"break_style": style}),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'break_style'",
        expected="LineBreakStyle",
        value=style,
        verbose=False,
    )


@pytest.mark.parametrize("block", [BlankLine(), Paragraph("x")])
def test_paragraph_rejects_a_block_as_a_line(subtests, block) -> None:
    """Verify a block node cannot be a line of a paragraph."""

    assert_exception_function(
        subtests,
        Paragraph,
        invalid_params=("a", block),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, None, 3.14, {"a": 1}])
def test_paragraph_rejects_a_line_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        Paragraph,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )


@pytest.mark.parametrize(
    "code, expected",
    [
        # Two backticks inside make the delimiter three backticks, which looks like a fence
        ("a``b", "```a``b```"),
        ("``x", "``` ``x ```"),
        ("x``", "``` x`` ```"),
        ("``", "``` `` ```"),
    ],
)
def test_paragraph_a_code_span_with_three_backticks_at_the_line_start_is_not_escaped(code, expected) -> None:
    """Verify a code span is not broken by the fence rule (a fence has no backtick in its info)."""

    assert Paragraph(InlineCode(code)).to_lines() == (expected,)


def test_paragraph_a_code_span_with_three_backticks_on_a_later_line() -> None:
    """Verify the same for the second line of a paragraph."""

    assert Paragraph("a", InlineCode("a``b")).to_lines() == ("a", "```a``b```")


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("```py", r"\```py"),
        ("```py title=x", r"\```py title=x"),
        ("~~~a`b", r"\~~~a`b"),
    ],
)
def test_paragraph_a_raw_fence_at_the_line_start_is_still_escaped(raw, expected) -> None:
    """Verify the narrower rule does not let a real fence through."""

    assert Paragraph(Text(raw, escape=False)).to_lines() == (expected,)
