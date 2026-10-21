import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown._common.enums import LineBreakStyle
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers._helpers import cell_text
from simplibs.markdown.inline.LineBreak import LineBreak
from simplibs.markdown.inline.Text import Text


@pytest.mark.parametrize(
    "cell, expected",
    [
        ("text", "text"),
        ("", ""),
        # A string is content: special characters are escaped
        ("a*b", r"a\*b"),
        # A pipe would end the cell
        ("a|b", r"a\|b"),
        # A node is written as it is, then its pipes are escaped
        (Text("x|y", escape=False), r"x\|y"),
        (Text("*x*", escape=False), "*x*"),
        # A list of inline content is one cell
        (["a", Text("b")], "ab"),
        (["a", ["b", "c"]], "abc"),
        # A break written as HTML stays on the line
        (["a", LineBreak(LineBreakStyle.HTML), "b"], "a<br>b"),
    ],
)
def test_cell_text(cell, expected) -> None:
    """Verify a cell becomes one line of inline text with its pipes escaped."""

    assert cell_text(cell) == expected


def test_cell_text_returns_a_string() -> None:
    """Verify the result is a plain string."""

    assert isinstance(cell_text(["a", "b"]), str)


@pytest.mark.parametrize(
    "cell, rendered",
    [
        ("a\nb", "a\nb"),
        ("\nleading", "\nleading"),
        (["a", LineBreak(LineBreakStyle.SPACES), "b"], "a  \nb"),
        (["a", LineBreak(LineBreakStyle.BACKSLASH), "b"], "a\\\nb"),
    ],
)
def test_cell_text_rejects_a_line_break(subtests, cell, rendered) -> None:
    """Verify a cell that renders to more than one line raises the multiline card."""

    assert_exception_function(
        subtests,
        cell_text,
        invalid_params=(cell,),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_CELL_MULTILINE",
        value=rendered,
        verbose=False,
    )


def test_cell_text_rejects_a_block(subtests) -> None:
    """Verify a block node raises the block-in-inline card."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        cell_text,
        invalid_params=(block,),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, None, True, {"a": 1}])
def test_cell_text_rejects_what_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        cell_text,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
