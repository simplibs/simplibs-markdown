import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Html import Html
from simplibs.markdown.blocks.enums import HtmlMode
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.presets.html import COMMENT


def test_comment_builds_an_html_comment() -> None:
    """Verify the kind of node, the mode, that there is no tag, and the level."""

    node = COMMENT("note")

    assert isinstance(node, Html)
    assert node.mode is HtmlMode.COMMENT
    assert node.tag is None
    assert node.node_level is NodeLevel.BLOCK


def test_comment_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert COMMENT("TODO: add an example").to_text() == "<!-- TODO: add an example -->"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("note", ("<!-- note -->",)),
        ("", ("<!-- -->",)),
        # Nothing in a comment is escaped
        ("*x* # y", ("<!-- *x* # y -->",)),
        # More lines: between two marker lines
        ("a\nb", ("<!--", "a", "b", "-->")),
    ],
)
def test_comment_lines(text, expected) -> None:
    """Verify a comment on one line or on several."""

    assert COMMENT(text).to_lines() == expected


def test_comment_is_a_block_between_other_blocks() -> None:
    """Verify it is written as a block of its own (the use for keeping two lists apart)."""

    result = "a" + COMMENT("x") + "b"

    assert isinstance(result, Document)
    assert result.to_lines() == ("a", "", "<!-- x -->", "", "b")


def test_comment_without_a_text_is_an_empty_comment() -> None:
    """Verify `None` means no content, as it does for the node below."""

    assert COMMENT(None).to_lines() == ("<!-- -->",)


@pytest.mark.parametrize("text", [42, ["a"], True, 3.14])
def test_comment_rejects_a_text_that_is_not_a_string(subtests, text) -> None:
    """Verify the text has to be a string."""

    assert_exception_function(
        subtests,
        COMMENT,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'content'",
        expected="str",
        value=text,
        verbose=False,
    )


@pytest.mark.parametrize("text", ["a --> b", ">x", "->x"])
def test_comment_rejects_a_text_that_would_end_the_comment(subtests, text) -> None:
    """Verify the text cannot close the comment early."""

    assert_exception_function(
        subtests,
        COMMENT,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_COMMENT_TERMINATOR",
        value=text,
        verbose=False,
    )
