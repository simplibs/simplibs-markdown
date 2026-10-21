import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.presets.references import COLOR_CHIP


def test_color_chip_builds_an_inline_code() -> None:
    """Verify the kind of node and the level."""

    node = COLOR_CHIP("#0969DA")

    assert isinstance(node, InlineCode)
    assert node.text == "#0969DA"
    assert node.node_level is NodeLevel.INLINE


def test_color_chip_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert COLOR_CHIP("#0969DA").to_text() == "`#0969DA`"


@pytest.mark.parametrize(
    "color, expected",
    [
        ("#0969DA", "`#0969DA`"),
        ("#fff", "`#fff`"),
        ("rgb(9, 105, 218)", "`rgb(9, 105, 218)`"),
        ("hsl(212, 92%, 45%)", "`hsl(212, 92%, 45%)`"),
        # The color is not checked
        ("not a color", "`not a color`"),
    ],
)
def test_color_chip_text(color, expected) -> None:
    """Verify the color is written between backticks, as it is."""

    assert COLOR_CHIP(color).to_text() == expected


def test_color_chip_stands_inside_a_line() -> None:
    """Verify it can be added to text, like any inline node."""

    result = "Blue is " + COLOR_CHIP("#0969DA") + "."

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "Blue is `#0969DA`."


@pytest.mark.parametrize("color", ["", "   ", "\t"])
def test_color_chip_rejects_an_empty_color(subtests, color) -> None:
    """Verify there has to be something to show."""

    assert_exception_function(
        subtests,
        COLOR_CHIP,
        invalid_params=(color,),
        exception_type=ParamError,
        error_name="MARKDOWN_INLINE_CODE_EMPTY",
        value=color,
        verbose=False,
    )


@pytest.mark.parametrize("color", [42, 3.14, None, True, ["#fff"]])
def test_color_chip_rejects_a_color_that_is_not_a_string(subtests, color) -> None:
    """Verify the color has to be a string."""

    assert_exception_function(
        subtests,
        COLOR_CHIP,
        invalid_params=(color,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        value=color,
        verbose=False,
    )
