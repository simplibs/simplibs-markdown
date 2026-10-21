import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Quote import Quote
from simplibs.markdown.containers.enums import AlertKind
from simplibs.markdown.presets.alerts import NOTE


def test_note_builds_a_quote_with_this_alert() -> None:
    """Verify the kind of node, the alert and the level."""

    node = NOTE("text")

    assert isinstance(node, Quote)
    assert node.alert is AlertKind.NOTE
    assert node.node_level is NodeLevel.BLOCK


def test_note_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert NOTE("Back up your data first.").to_text() == "> [!NOTE]\n> Back up your data first."


@pytest.mark.parametrize(
    "blocks, expected",
    [
        (("text",), ("> [!NOTE]", "> text")),
        # Several blocks are separated by a quoted blank line
        (("a", "b"), ("> [!NOTE]", "> a", ">", "> b")),
        ((["a", ["b"]],), ("> [!NOTE]", "> a", ">", "> b")),
        # Nodes are content too
        ((Paragraph("a", "b"),), ("> [!NOTE]", "> a", "> b")),
        ((CodeBlock("x"),), ("> [!NOTE]", "> ```", "> x", "> ```")),
        # An alert may have no content
        ((), ("> [!NOTE]",)),
    ],
)
def test_note_lines(blocks, expected) -> None:
    """Verify the marker line, then the quoted content."""

    assert NOTE(*blocks).to_lines() == expected


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_note_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify an invalid block is refused by the quote below."""

    assert_exception_function(
        subtests,
        NOTE,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
