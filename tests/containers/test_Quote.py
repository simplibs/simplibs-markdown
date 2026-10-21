import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.containers.List import List
from simplibs.markdown.containers.Quote import Quote
from simplibs.markdown.containers.enums import AlertKind


def _make(blocks, options: dict) -> Quote:
    """Create a Quote from blocks and keyword options."""

    return Quote(*blocks, **options)


def test_quote_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = Quote("a")

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_quote_stores_its_parameters() -> None:
    """Verify the attributes and the default of `alert`."""

    node = Quote("a", "b")

    assert isinstance(node.blocks, tuple)
    assert len(node.blocks) == 2
    assert node.alert is None
    assert Quote("a", alert=AlertKind.NOTE).alert is AlertKind.NOTE


@pytest.mark.parametrize(
    "blocks, expected",
    [
        (("a",), ("> a",)),
        # Several blocks: a bare '>' between them, without trailing space
        (("a", "b"), ("> a", ">", "> b")),
        (("a", "b", "c"), ("> a", ">", "> b", ">", "> c")),
        # A block with several lines
        ((Paragraph("a", "b"),), ("> a", "> b")),
        # A document is unpacked
        ((Document("a", "b"),), ("> a", ">", "> b")),
        # Code, with an empty line inside
        ((CodeBlock("x"),), ("> ```", "> x", "> ```")),
        ((CodeBlock("a\n\nb"),), ("> ```", "> a", ">", "> b", "> ```")),
        # A list
        ((List("a", "b"),), ("> - a", "> - b")),
    ],
)
def test_quote_lines(blocks, expected) -> None:
    """Verify every line gets the quote mark."""

    node = Quote(*blocks)

    assert node.to_lines() == expected
    assert node.to_text() == "\n".join(expected)
    assert str(node) == "\n".join(expected)


def test_quote_nested_quotes() -> None:
    """Verify a quote in a quote just gets one more mark."""

    assert Quote(Quote("a")).to_lines() == ("> > a",)
    assert Quote("a", Quote("b")).to_lines() == ("> a", ">", "> > b")


@pytest.mark.parametrize("alert", list(AlertKind))
def test_quote_alert_starts_with_its_marker_line(alert) -> None:
    """Verify the marker line, then the content on the lines right after it."""

    node = Quote("text", alert=alert)

    assert node.to_lines() == (f"> [!{alert.value}]", "> text")


def test_quote_alert_content_has_no_blank_line_after_the_marker() -> None:
    """Verify GitHub gets the content straight after `[!NOTE]`."""

    node = Quote("a", "b", alert=AlertKind.WARNING)

    assert node.to_lines() == ("> [!WARNING]", "> a", ">", "> b")


@pytest.mark.parametrize("blocks", [(), (None,), ([],)])
def test_quote_alert_may_be_empty(blocks) -> None:
    """Verify an alert without content is only its marker line."""

    node = Quote(*blocks, alert=AlertKind.TIP)

    assert node.to_lines() == ("> [!TIP]",)
    assert node.blocks == ()


def test_quote_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Quote("a"), "__dict__")


@pytest.mark.parametrize("blocks", [(), (None,), ([],), ((), [None])])
def test_quote_rejects_a_plain_quote_without_content(subtests, blocks) -> None:
    """Verify only an alert may be empty."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(blocks, {}),
        exception_type=ParamError,
        error_name="MARKDOWN_NO_BLOCKS",
        verbose=False,
    )


@pytest.mark.parametrize("alert", ["NOTE", "note", "tip", 1, True, AlertKind.NOTE.value])
def test_quote_rejects_an_alert_of_the_wrong_type(subtests, alert) -> None:
    """Verify `alert` has to be an AlertKind."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(("a",), {"alert": alert}),
        exception_type=ParamError,
        error_name="MARKDOWN_QUOTE_UNKNOWN_ALERT",
        value=alert,
        verbose=False,
    )


def test_quote_checks_the_alert_before_the_content(subtests) -> None:
    """Verify a wrong alert is reported even when there is no content."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=((), {"alert": "NOTE"}),
        exception_type=ParamError,
        error_name="MARKDOWN_QUOTE_UNKNOWN_ALERT",
        value="NOTE",
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_quote_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        Quote,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
