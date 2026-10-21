import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.BlankLine import BlankLine


def test_blank_line_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = BlankLine()

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_blank_line_default_is_one_line() -> None:
    """Verify the default count."""

    assert BlankLine().count == 1
    assert BlankLine().to_lines() == ("",)


@pytest.mark.parametrize("count", [1, 2, 3, 10])
def test_blank_line_gives_that_many_empty_lines(count) -> None:
    """Verify one empty string per line."""

    node = BlankLine(count)

    assert node.count == count
    assert node.to_lines() == ("",) * count


@pytest.mark.parametrize("count, text", [(1, ""), (2, "\n"), (3, "\n\n")])
def test_blank_line_to_text(count, text) -> None:
    """Verify the lines joined by line breaks."""

    assert BlankLine(count).to_text() == text
    assert str(BlankLine(count)) == text


def test_blank_line_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(BlankLine(), "__dict__")


@pytest.mark.parametrize("count", [0, -1, -100, "1", 1.5, None, True, False, [1]])
def test_blank_line_rejects_a_count_that_is_not_a_positive_integer(subtests, count) -> None:
    """Verify only a positive integer is a count (a bool is not)."""

    assert_exception_function(
        subtests,
        BlankLine,
        invalid_params=(count,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'count'",
        expected="positive int",
        value=count,
        verbose=False,
    )
