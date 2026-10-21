import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown._common.enums import LineBreakStyle
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Table import Table
from simplibs.markdown.containers.enums import TableAlign
from simplibs.markdown.inline.Emphasis import Emphasis
from simplibs.markdown.inline.LineBreak import LineBreak
from simplibs.markdown.inline.Text import Text

NONE = TableAlign.NONE
LEFT = TableAlign.LEFT
CENTER = TableAlign.CENTER
RIGHT = TableAlign.RIGHT


def test_table_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = Table(["a"])

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_table_stores_cells_as_text() -> None:
    """Verify the head and the rows are tuples of rendered cells, and the alignment a tuple."""

    node = Table(["a", "b"], [["1", "2"], ["3", "4"]], [LEFT, RIGHT])

    assert node.head == ("a", "b")
    assert node.rows == (("1", "2"), ("3", "4"))
    assert node.align == (LEFT, RIGHT)


def test_table_default_alignment_is_none_for_every_column() -> None:
    """Verify no alignment is the default."""

    assert Table(["a", "b", "c"]).align == (NONE, NONE, NONE)


# ----------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------

def test_table_pads_every_column_to_its_longest_cell() -> None:
    """Verify the source lines up."""

    node = Table(["Name", "Age"], [["Alice", "30"], ["Bob", "4"]])

    assert node.to_lines() == (
        "| Name  | Age |",
        "| ----- | --- |",
        "| Alice | 30  |",
        "| Bob   | 4   |",
    )


def test_table_columns_are_at_least_three_wide() -> None:
    """Verify the separator always has room for its dashes."""

    assert Table(["a", "b"], [["1", "2"]]).to_lines() == (
        "| a   | b   |",
        "| --- | --- |",
        "| 1   | 2   |",
    )


def test_table_without_rows_is_the_header_and_the_separator() -> None:
    """Verify a table with no rows."""

    assert Table(["a", "b"]).to_lines() == ("| a   | b   |", "| --- | --- |")


def test_table_alignment() -> None:
    """Verify the cells and the colons of the separator follow the alignment."""

    node = Table(["a", "b", "c", "d"], [["1", "2", "3", "4"]], [NONE, LEFT, CENTER, RIGHT])

    assert node.to_lines() == (
        "| a   | b   |  c  |   d |",
        "| --- | :-- | :-: | --: |",
        "| 1   | 2   |  3  |   4 |",
    )


@pytest.mark.parametrize("container", [list, tuple])
def test_table_alignment_may_be_a_list_or_a_tuple(container) -> None:
    """Verify both are accepted and stored as a tuple."""

    node = Table(["a", "b"], align=container([LEFT, RIGHT]))

    assert node.align == (LEFT, RIGHT)


@pytest.mark.parametrize(
    "head, rows",
    [
        (["a", "bb", "ccc"], [["1", "22", "333"], ["4444", "5", "6"]]),
        (["Name"], [["x"], ["a longer cell"]]),
        (["x", "y"], [["a|b", "c*d"]]),
    ],
)
@pytest.mark.parametrize("align", [None, "mixed"])
def test_table_all_lines_are_equally_long(head, rows, align) -> None:
    """Verify the table is a clean rectangle in the source."""

    columns = len(head)
    aligns = None if align is None else [[LEFT, CENTER, RIGHT][index % 3] for index in range(columns)]

    lines = Table(head, rows, aligns).to_lines()

    assert len({len(line) for line in lines}) == 1


def test_table_to_text_and_str() -> None:
    """Verify the rendered text."""

    node = Table(["a"], [["1"]])

    assert node.to_text() == "| a   |\n| --- |\n| 1   |"
    assert str(node) == "| a   |\n| --- |\n| 1   |"


# ----------------------------------------------------------------------
# Cells
# ----------------------------------------------------------------------

def test_table_a_string_head_is_a_one_column_table() -> None:
    """Verify a lone string is a row of one cell, for the head and for the rows."""

    node = Table("Name", ["a", "b"])

    assert node.head == ("Name",)
    assert node.rows == (("a",), ("b",))
    assert node.to_lines() == ("| Name |", "| ---- |", "| a    |", "| b    |")


def test_table_cells_are_escaped_and_pipes_are_protected() -> None:
    """Verify a string is content, and a pipe cannot end the cell."""

    node = Table(["a|b"], [["c*d"]])

    assert node.head == (r"a\|b",)
    assert node.rows == ((r"c\*d",),)


def test_table_column_width_counts_the_escaped_text() -> None:
    """Verify the width is that of the text as written, so the lines stay straight."""

    assert Table(["a|b"], [["c|d"]]).to_lines() == (
        r"| a\|b |",
        "| ---- |",
        r"| c\|d |",
    )


def test_table_cells_may_be_nodes_and_lists() -> None:
    """Verify inline nodes are written as they are."""

    node = Table(["h"], [[Emphasis("x")], [["a", Text("b")]], [Text("*c*", escape=False)]])

    assert node.rows == (("*x*",), ("ab",), ("*c*",))


def test_table_a_break_written_as_html_stays_in_the_cell() -> None:
    """Verify the HTML break keeps the cell on one line."""

    node = Table(["h"], [[["a", LineBreak(LineBreakStyle.HTML), "b"]]])

    assert node.rows == (("a<br>b",),)


def test_table_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Table(["a"]), "__dict__")


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

@pytest.mark.parametrize("head", [42, 3.14, None, True, {"a": 1}])
def test_table_rejects_a_head_of_the_wrong_type(subtests, head) -> None:
    """Verify the head is a string, a node, a list or a tuple."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(head,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'head'",
        expected="str, list or tuple",
        value=head,
        verbose=False,
    )


@pytest.mark.parametrize("head", [[], ()])
def test_table_rejects_a_head_without_columns(subtests, head) -> None:
    """Verify a table has at least one column."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(head,),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_NO_COLUMNS",
        verbose=False,
    )


@pytest.mark.parametrize("rows", ["ab", "", 42, 3.14, None, True])
def test_table_rejects_rows_that_are_not_a_collection_of_rows(subtests, rows) -> None:
    """Verify `rows` is an iterable of rows, and a string is not one."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(["a"], rows),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'rows'",
        expected="a list of rows",
        value=rows,
        verbose=False,
    )


@pytest.mark.parametrize("row", [42, 3.14, None, True, {"a": 1}])
def test_table_rejects_a_row_of_the_wrong_type(subtests, row) -> None:
    """Verify one row of the wrong type is named as a `rows` parameter."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(["a"], [row]),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'rows'",
        expected="str, list or tuple",
        value=row,
        verbose=False,
    )


@pytest.mark.parametrize(
    "row, cells",
    [
        ([], ()),
        (["1"], ("1",)),
        (["1", "2", "3"], ("1", "2", "3")),
    ],
)
def test_table_rejects_a_row_of_another_width_than_the_header(subtests, row, cells) -> None:
    """Verify every row has as many cells as the header."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(["a", "b"], [["x", "y"], row]),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_ROW_WIDTH_MISMATCH",
        value=cells,
        verbose=False,
    )


@pytest.mark.parametrize("align", ["left", LEFT, 42, True, {"a": 1}])
def test_table_rejects_an_alignment_that_is_not_a_list(subtests, align) -> None:
    """Verify `align` is a list or a tuple (a single TableAlign is not enough)."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(["a"], (), align),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'align'",
        expected="a list of TableAlign",
        value=align,
        verbose=False,
    )


@pytest.mark.parametrize("bad", ["left", "none", None, 1, True])
def test_table_rejects_an_alignment_that_is_not_a_table_align(subtests, bad) -> None:
    """Verify every member of `align` has to be a TableAlign."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(["a", "b"], (), [LEFT, bad]),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'align'",
        expected="TableAlign",
        value=bad,
        verbose=False,
    )


@pytest.mark.parametrize(
    "align",
    [
        (),
        (LEFT,),
        (LEFT, RIGHT, CENTER),
    ],
)
def test_table_rejects_an_alignment_of_another_width_than_the_header(subtests, align) -> None:
    """Verify there is exactly one alignment per column."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(["a", "b"], (), align),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_ALIGN_WIDTH_MISMATCH",
        value=align,
        verbose=False,
    )


@pytest.mark.parametrize(
    "head, rows, rendered",
    [
        (["a\nb"], (), "a\nb"),
        (["a"], [["x\ny"]], "x\ny"),
        (["a"], [[["x", LineBreak(LineBreakStyle.SPACES), "y"]]], "x  \ny"),
    ],
)
def test_table_rejects_a_cell_with_a_line_break(subtests, head, rows, rendered) -> None:
    """Verify a cell stays on one line, in the header and in the rows."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(head, rows),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_CELL_MULTILINE",
        value=rendered,
        verbose=False,
    )


def test_table_rejects_a_block_as_a_cell(subtests) -> None:
    """Verify a block node cannot be a cell."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(["h"], [[block]]),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, None, {"a": 1}])
def test_table_rejects_a_cell_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        Table,
        invalid_params=(["h"], [[value]]),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
