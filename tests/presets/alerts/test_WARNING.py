import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Quote import Quote
from simplibs.markdown.containers.enums import AlertKind
from simplibs.markdown.presets.alerts import WARNING


def test_warning_builds_a_quote_with_this_alert() -> None:
    """Verify the kind of node, the alert and the level."""

    node = WARNING("text")

    assert isinstance(node, Quote)
    assert node.alert is AlertKind.WARNING
    assert node.node_level is NodeLevel.BLOCK


def test_warning_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert WARNING("This deletes all existing files.").to_text() == "> [!WARNING]\n> This deletes all existing files."


@pytest.mark.parametrize(
    "blocks, expected",
    [
        (("text",), ("> [!WARNING]", "> text")),
        # Several blocks are separated by a quoted blank line
        (("a", "b"), ("> [!WARNING]", "> a", ">", "> b")),
        ((["a", ["b"]],), ("> [!WARNING]", "> a", ">", "> b")),
        # Nodes are content too
        ((Paragraph("a", "b"),), ("> [!WARNING]", "> a", "> b")),
        ((CodeBlock("x"),), ("> [!WARNING]", "> ```", "> x", "> ```")),
        # An alert may have no content
        ((), ("> [!WARNING]",)),
    ],
)
def test_warning_lines(blocks, expected) -> None:
    """Verify the marker line, then the quoted content."""

    assert WARNING(*blocks).to_lines() == expected


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_warning_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify an invalid block is refused by the quote below."""

    assert_exception_function(
        subtests,
        WARNING,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
