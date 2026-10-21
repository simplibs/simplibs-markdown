import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Link import Link
from simplibs.markdown.inline.enums import LinkKind
from simplibs.markdown.presets.emphasis import ITALIC
from simplibs.markdown.presets.links import IMAGE


def test_image_builds_an_inline_link_that_is_an_image() -> None:
    """Verify the kind of node, the kind, the image flag, the parts and the level."""

    node = IMAGE("Logo", "img/logo.png", "Our logo")

    assert isinstance(node, Link)
    assert node.kind is LinkKind.INLINE
    assert node.image is True
    assert node.dest == "img/logo.png"
    assert node.title == "Our logo"
    assert node.node_level is NodeLevel.INLINE


def test_image_title_is_optional() -> None:
    """Verify the default."""

    assert IMAGE("Logo", "img/logo.png").title is None


@pytest.mark.parametrize(
    "arguments, expected",
    [
        # The examples from the docstring
        (("Logo", "img/logo.png"), "![Logo](img/logo.png)"),
        (("Logo", "img/logo.png", "Our logo"), '![Logo](img/logo.png "Our logo")'),
        # An empty alt text is allowed
        (("", "img/logo.png"), "![](img/logo.png)"),
        # An address with a space goes into angle brackets
        (("Logo", "my logo.png"), "![Logo](<my logo.png>)"),
        # An empty title is no title
        (("Logo", "u", ""), "![Logo](u)"),
        # The alt text is content: escaped
        (("a*b", "u"), r"![a\*b](u)"),
        # A node is written as it is
        ((ITALIC("b"), "u"), "![*b*](u)"),
        ((["a ", ITALIC("b")], "u"), "![a *b*](u)"),
    ],
)
def test_image_text(arguments, expected) -> None:
    """Verify how the image is written."""

    assert IMAGE(*arguments).to_text() == expected


def test_image_stands_inside_a_line() -> None:
    """Verify it can be added to text, like any inline node."""

    result = "Our " + IMAGE("logo", "l.png") + " here"

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "Our ![logo](l.png) here"


@pytest.mark.parametrize("src", ["", None])
def test_image_rejects_an_empty_source(subtests, src) -> None:
    """Verify there has to be an address."""

    assert_exception_function(
        subtests,
        IMAGE,
        invalid_params=("Logo", src),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_EMPTY_DESTINATION",
        value=src,
        verbose=False,
    )


def test_image_rejects_a_missing_alt_text(subtests) -> None:
    """Verify the alt text is required (an empty string is fine, `None` is not)."""

    assert_exception_function(
        subtests,
        IMAGE,
        invalid_params=(None, "u"),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'text'",
        expected="str | Markdown",
        value=None,
        verbose=False,
    )


def test_image_rejects_a_block_as_alt_text(subtests) -> None:
    """Verify the alt text is inline content."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        IMAGE,
        invalid_params=(block, "u"),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("name, value", [("src", 42), ("title", 42)])
def test_image_rejects_a_text_parameter_of_the_wrong_type(subtests, name, value) -> None:
    """Verify the address and the title have to be strings."""

    arguments = ("alt", value) if name == "src" else ("alt", "u", value)
    label = "dest" if name == "src" else "title"

    assert_exception_function(
        subtests,
        IMAGE,
        invalid_params=arguments,
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label=f"parameter '{label}'",
        expected="str",
        value=value,
        verbose=False,
    )
