import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Quote import Quote
from simplibs.markdown.containers.enums import AlertKind
from simplibs.markdown.presets.alerts import TIP


def test_tip_builds_a_quote_with_this_alert() -> None:
    """Verify the kind of node, the alert and the level."""

    node = TIP("text")

    assert isinstance(node, Quote)
    assert node.alert is AlertKind.TIP
    assert node.node_level is NodeLevel.BLOCK


def test_tip_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert TIP("Run the tests before you commit.").to_text() == "> [!TIP]\n> Run the tests before you commit."


@pytest.mark.parametrize(
    "blocks, expected",
    [
        (("text",), ("> [!TIP]", "> text")),
        # Several blocks are separated by a quoted blank line
        (("a", "b"), ("> [!TIP]", "> a", ">", "> b")),
        ((["a", ["b"]],), ("> [!TIP]", "> a", ">", "> b")),
        # Nodes are content too
        ((Paragraph("a", "b"),), ("> [!TIP]", "> a", "> b")),
        ((CodeBlock("x"),), ("> [!TIP]", "> ```", "> x", "> ```")),
        # An alert may have no content
        ((), ("> [!TIP]",)),
    ],
)
def test_tip_lines(blocks, expected) -> None:
    """Verify the marker line, then the quoted content."""

    assert TIP(*blocks).to_lines() == expected


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_tip_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify an invalid block is refused by the quote below."""

    assert_exception_function(
        subtests,
        TIP,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
