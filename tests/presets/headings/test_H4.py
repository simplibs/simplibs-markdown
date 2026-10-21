import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Heading import Heading
from simplibs.markdown.blocks.enums import HeadingStyle
from simplibs.markdown.presets.emphasis import ITALIC
from simplibs.markdown.presets.headings import H4

HASHES = "#" * 4


def test_h4_builds_a_heading_of_level_4() -> None:
    """Verify the kind of node, the level, the default style and the node level."""

    node = H4("Title")

    assert isinstance(node, Heading)
    assert node.level == 4
    assert node.style is HeadingStyle.ATX
    assert node.node_level is NodeLevel.BLOCK


def test_h4_writes_as_many_hashes_as_its_level() -> None:
    """Verify the default form."""

    assert H4("Title").to_lines() == (f"{HASHES} Title",)


def test_h4_closed_style() -> None:
    """Verify the hashes are repeated at the end."""

    assert H4("Title", HeadingStyle.ATX_CLOSED).to_lines() == (f"{HASHES} Title {HASHES}",)


def test_h4_style_may_be_given_by_name() -> None:
    """Verify the second parameter can be a keyword."""

    assert H4("Title", style=HeadingStyle.ATX_CLOSED).to_lines() == (f"{HASHES} Title {HASHES}",)


def test_h4_rejects_the_setext_style(subtests) -> None:
    """Verify setext has two levels only."""

    assert_exception_function(
        subtests,
        H4,
        invalid_params=("Title", HeadingStyle.SETEXT),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_SETEXT_LEVEL",
        value=4,
        verbose=False,
    )


@pytest.mark.parametrize(
    "inner, expected",
    [
        ("a *b*", HASHES + r" a \*b\*"),       # a string is content: escaped
        (ITALIC("b"), HASHES + " *b*"),         # a node is written as it is
        (["a ", ITALIC("b")], HASHES + " a *b*"),
        ("  Title  ", HASHES + " Title"),       # edge whitespace is dropped
    ],
)
def test_h4_text(inner, expected) -> None:
    """Verify how the content of the heading is written."""

    assert H4(inner).to_lines() == (expected,)


def test_h4_level_is_fixed_by_the_preset() -> None:
    """Verify the level cannot be given."""

    with pytest.raises(TypeError):
        H4("Title", level=2)


@pytest.mark.parametrize("text", ["first\nsecond", "a\r\nb"])
def test_h4_rejects_text_on_more_lines(subtests, text) -> None:
    """Verify a heading stays on one line."""

    assert_exception_function(
        subtests,
        H4,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_MULTILINE",
        value=text,
        verbose=False,
    )


@pytest.mark.parametrize("style", ["atx", None, 1, True])
def test_h4_rejects_a_style_of_the_wrong_type(subtests, style) -> None:
    """Verify the style has to be a HeadingStyle."""

    assert_exception_function(
        subtests,
        H4,
        invalid_params=("Title", style),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'style'",
        expected="HeadingStyle",
        value=style,
        verbose=False,
    )
