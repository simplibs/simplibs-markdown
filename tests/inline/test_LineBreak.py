import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown._common.enums import LineBreakStyle
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.inline.LineBreak import LineBreak
from simplibs.markdown.inline.Text import Text


def test_line_break_is_an_inline_node() -> None:
    """Verify the class."""

    assert isinstance(LineBreak(), InlineMarkdown)


def test_line_break_default_style_is_spaces() -> None:
    """Verify the default."""

    assert LineBreak().style is LineBreakStyle.SPACES
    assert LineBreak().to_inline() == "  \n"


@pytest.mark.parametrize(
    "style, expected",
    [
        (LineBreakStyle.SPACES, "  \n"),
        (LineBreakStyle.BACKSLASH, "\\\n"),
        (LineBreakStyle.HTML, "<br>"),
    ],
)
def test_line_break_writes_each_style(style, expected) -> None:
    """Verify the exact text of every style."""

    node = LineBreak(style)

    assert node.style is style
    assert node.to_inline() == expected
    assert node.to_text() == expected
    assert str(node) == expected


@pytest.mark.parametrize(
    "style, expected",
    [
        (LineBreakStyle.SPACES, ("  ", "")),
        (LineBreakStyle.BACKSLASH, ("\\", "")),
        (LineBreakStyle.HTML, ("<br>",)),
    ],
)
def test_line_break_lines(style, expected) -> None:
    """Verify the two styles that end the line give two lines, the HTML style one."""

    assert LineBreak(style).to_lines() == expected


@pytest.mark.parametrize(
    "style, expected",
    [
        (LineBreakStyle.SPACES, "a  \nb"),
        (LineBreakStyle.BACKSLASH, "a\\\nb"),
        (LineBreakStyle.HTML, "a<br>b"),
    ],
)
def test_line_break_inside_a_line_of_content(style, expected) -> None:
    """Verify the break works between two texts."""

    assert (Text("a") + LineBreak(style) + Text("b")).to_text() == expected


def test_line_break_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(LineBreak(), "__dict__")


@pytest.mark.parametrize("style", ["spaces", "html", None, 1, True, "  \n"])
def test_line_break_rejects_a_style_of_the_wrong_type(subtests, style) -> None:
    """Verify `style` has to be a LineBreakStyle."""

    assert_exception_function(
        subtests,
        LineBreak,
        invalid_params=(style,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'style'",
        expected="LineBreakStyle",
        value=style,
        verbose=False,
    )
