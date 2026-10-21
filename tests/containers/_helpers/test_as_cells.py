import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers._helpers import as_cells
from simplibs.markdown.inline.Text import Text


@pytest.mark.parametrize("container", [list, tuple])
def test_as_cells_list_or_tuple_gives_one_cell_each(container) -> None:
    """Verify every item of the row is rendered as a cell."""

    assert as_cells(container(["a", "b", "c"])) == ("a", "b", "c")


def test_as_cells_returns_a_tuple() -> None:
    """Verify the result is a tuple, whatever went in."""

    assert isinstance(as_cells(["a", "b"]), tuple)
    assert isinstance(as_cells("a"), tuple)


@pytest.mark.parametrize(
    "row, expected",
    [
        # A string or a node is a row of one cell
        ("a", ("a",)),
        ("", ("",)),
        (Text("a"), ("a",)),
        # No cells, no result
        ([], ()),
        ((), ()),
    ],
)
def test_as_cells_single_item_and_empty_rows(row, expected) -> None:
    """Verify a lone string or node is one cell and an empty row has none."""

    assert as_cells(row) == expected


def test_as_cells_renders_each_cell_like_cell_text() -> None:
    """Verify strings are escaped, nodes are kept and pipes are escaped."""

    row = ["a|b", "c*d", Text("e|f", escape=False), ["g", Text("h")]]

    assert as_cells(row) == (r"a\|b", r"c\*d", r"e\|f", "gh")


@pytest.mark.parametrize("value", [42, 3.14, None, True, {"a": 1}, {1, 2}])
def test_as_cells_rejects_a_row_of_the_wrong_type(subtests, value) -> None:
    """Verify a row that is no string, node, list or tuple raises the type card."""

    assert_exception_function(
        subtests,
        as_cells,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'row'",
        expected="str, list or tuple",
        value=value,
        verbose=False,
    )


@pytest.mark.parametrize("name", ["head", "rows"])
def test_as_cells_shows_the_given_parameter_name(subtests, name) -> None:
    """Verify the card names the parameter that the caller passed."""

    assert_exception_function(
        subtests,
        as_cells,
        invalid_params=(42, name),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label=f"parameter '{name}'",
        value=42,
        verbose=False,
    )


def test_as_cells_rejects_a_block_as_a_row(subtests) -> None:
    """Verify a block node is a one-cell row, and then fails as a cell."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        as_cells,
        invalid_params=(block,),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


def test_as_cells_rejects_a_wrong_cell(subtests) -> None:
    """Verify one wrong cell raises the not-markdown card for that cell."""

    assert_exception_function(
        subtests,
        as_cells,
        invalid_params=(["a", 42],),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=42,
        verbose=False,
    )


def test_as_cells_rejects_a_cell_with_a_line_break(subtests) -> None:
    """Verify a multiline cell raises the multiline card."""

    assert_exception_function(
        subtests,
        as_cells,
        invalid_params=(["a", "b\nc"],),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_CELL_MULTILINE",
        value="b\nc",
        verbose=False,
    )
