import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Html import Html
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.blocks.enums import HtmlMode
from simplibs.markdown.presets.emphasis import ITALIC
from simplibs.markdown.presets.html import DETAILS
from simplibs.markdown.presets.lists import BULLET_LIST


def test_details_builds_a_block_details_tag() -> None:
    """Verify the kind of node, the tag, the mode and the level."""

    node = DETAILS("Show more", "Hidden text.")

    assert isinstance(node, Html)
    assert node.tag == "details"
    assert node.mode is HtmlMode.BLOCK
    assert node.node_level is NodeLevel.BLOCK


def test_details_is_collapsed_by_default() -> None:
    """Verify no `open` attribute is written unless asked for."""

    assert DETAILS("s", "b").attrs == {}
    assert DETAILS("s", "b", expanded=False).attrs == {}
    assert DETAILS("s", "b", expanded=True).attrs == {"open": True}


def test_details_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert DETAILS("Show more", "Hidden text.").to_lines() == (
        "<details>",
        "",
        "<summary>Show more</summary>",
        "",
        "Hidden text.",
        "",
        "</details>",
    )


def test_details_expanded_example_from_the_docstring() -> None:
    """Verify the same with `expanded=True`."""

    assert DETAILS("Show more", "Hidden text.", expanded=True).to_lines() == (
        "<details open>",
        "",
        "<summary>Show more</summary>",
        "",
        "Hidden text.",
        "",
        "</details>",
    )


@pytest.mark.parametrize(
    "body, expected",
    [
        # No body: the summary only
        ((), ("<details>", "", "<summary>s</summary>", "", "</details>")),
        # Several blocks are separated by a blank line
        (("a", "b"), ("<details>", "", "<summary>s</summary>", "", "a", "", "b", "", "</details>")),
        ((["a", ["b"]],), ("<details>", "", "<summary>s</summary>", "", "a", "", "b", "", "</details>")),
        # Nodes are content too: the Markdown inside is written as Markdown
        ((Paragraph("a", "b"),), ("<details>", "", "<summary>s</summary>", "", "a", "b", "", "</details>")),
        ((BULLET_LIST("x", "y"),), ("<details>", "", "<summary>s</summary>", "", "- x", "- y", "", "</details>")),
    ],
)
def test_details_body(body, expected) -> None:
    """Verify the lines, with a blank line around every block."""

    assert DETAILS("s", *body).to_lines() == expected


@pytest.mark.parametrize(
    "summary, expected",
    [
        ("Title", "<summary>Title</summary>"),
        ("a*b", r"<summary>a\*b</summary>"),     # a string is content: escaped
        (ITALIC("b"), "<summary>*b*</summary>"),  # a node is written as it is
    ],
)
def test_details_summary(summary, expected) -> None:
    """Verify the summary line."""

    assert DETAILS(summary, "body").to_lines()[2] == expected


def test_details_expanded_is_keyword_only() -> None:
    """Verify a value given by position is a block of the body, not the flag."""

    with pytest.raises(ParamError) as caught:
        DETAILS("s", "body", True)

    assert caught.value.error_name == "MARKDOWN_NODE_NOT_MARKDOWN"


@pytest.mark.parametrize("value", [42, 3.14, {"a": 1}])
def test_details_rejects_a_body_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        DETAILS,
        invalid_params=("s", "a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_details_rejects_a_summary_that_is_not_content(subtests, value) -> None:
    """Verify the summary has to be content as well."""

    assert_exception_function(
        subtests,
        DETAILS,
        invalid_params=(value, "body"),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
