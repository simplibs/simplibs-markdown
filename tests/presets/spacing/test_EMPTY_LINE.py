import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.presets.headings import H1
from simplibs.markdown.presets.spacing import EMPTY_LINE


def test_empty_line_builds_a_blank_line() -> None:
    """Verify the kind of node, the default count and the level."""

    node = EMPTY_LINE()

    assert isinstance(node, BlankLine)
    assert node.count == 1
    assert node.node_level is NodeLevel.BLOCK


@pytest.mark.parametrize("count", [1, 2, 3, 10])
def test_empty_line_gives_that_many_empty_lines(count) -> None:
    """Verify one empty line per count."""

    assert EMPTY_LINE(count).to_lines() == ("",) * count


@pytest.mark.parametrize(
    "count, expected",
    [
        # The separator between two blocks is not added to it
        (1, ("# A", "", "text")),
        (2, ("# A", "", "", "text")),
        (3, ("# A", "", "", "", "text")),   # the example from the docstring
    ],
)
def test_empty_line_counts_the_separator_between_blocks(count, expected) -> None:
    """Verify `EMPTY_LINE(1)` changes nothing and a larger count is the total."""

    result = H1("A") + EMPTY_LINE(count) + "text"

    assert isinstance(result, Document)
    assert result.to_lines() == expected


@pytest.mark.parametrize("count", [0, -1, "1", 1.5, None, True, False])
def test_empty_line_rejects_a_count_that_is_not_a_positive_integer(subtests, count) -> None:
    """Verify the count is an integer of at least one (a bool is not)."""

    assert_exception_function(
        subtests,
        EMPTY_LINE,
        invalid_params=(count,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'count'",
        expected="positive int",
        value=count,
        verbose=False,
    )
