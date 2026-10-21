import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Quote import Quote
from simplibs.markdown.containers.enums import AlertKind
from simplibs.markdown.presets.alerts import CAUTION


def test_caution_builds_a_quote_with_this_alert() -> None:
    """Verify the kind of node, the alert and the level."""

    node = CAUTION("text")

    assert isinstance(node, Quote)
    assert node.alert is AlertKind.CAUTION
    assert node.node_level is NodeLevel.BLOCK


def test_caution_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert CAUTION("This cannot be undone.").to_text() == "> [!CAUTION]\n> This cannot be undone."


@pytest.mark.parametrize(
    "blocks, expected",
    [
        (("text",), ("> [!CAUTION]", "> text")),
        # Several blocks are separated by a quoted blank line
        (("a", "b"), ("> [!CAUTION]", "> a", ">", "> b")),
        ((["a", ["b"]],), ("> [!CAUTION]", "> a", ">", "> b")),
        # Nodes are content too
        ((Paragraph("a", "b"),), ("> [!CAUTION]", "> a", "> b")),
        ((CodeBlock("x"),), ("> [!CAUTION]", "> ```", "> x", "> ```")),
        # An alert may have no content
        ((), ("> [!CAUTION]",)),
    ],
)
def test_caution_lines(blocks, expected) -> None:
    """Verify the marker line, then the quoted content."""

    assert CAUTION(*blocks).to_lines() == expected


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_caution_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify an invalid block is refused by the quote below."""

    assert_exception_function(
        subtests,
        CAUTION,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
