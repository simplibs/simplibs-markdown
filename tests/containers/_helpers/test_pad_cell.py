import pytest
from simplibs.markdown.containers._helpers import pad_cell
from simplibs.markdown.containers.enums import TableAlign


@pytest.mark.parametrize("align", [TableAlign.NONE, TableAlign.LEFT])
def test_pad_cell_pads_on_the_right_for_left_and_no_alignment(align) -> None:
    """Verify the text stays at the left edge."""

    assert pad_cell("ab", 5, align) == "ab   "


def test_pad_cell_pads_on_the_left_for_right_alignment() -> None:
    """Verify the text moves to the right edge."""

    assert pad_cell("ab", 5, TableAlign.RIGHT) == "   ab"


def test_pad_cell_centers_with_an_even_amount_of_padding() -> None:
    """Verify equal padding on both sides."""

    assert pad_cell("ab", 6, TableAlign.CENTER) == "  ab  "


@pytest.mark.parametrize("text, width", [("ab", 5), ("a", 4), ("abc", 8), ("", 3)])
def test_pad_cell_centers_with_an_odd_amount_of_padding(text, width) -> None:
    """Verify the two sides differ by at most one space."""

    result = pad_cell(text, width, TableAlign.CENTER)
    left = len(result) - len(result.lstrip(" "))
    right = len(result) - len(result.rstrip(" "))

    assert len(result) == width
    assert result.strip(" ") == text
    if text:
        assert abs(left - right) <= 1


@pytest.mark.parametrize("align", list(TableAlign))
def test_pad_cell_result_has_the_column_width(align) -> None:
    """Verify the result is exactly as wide as the column."""

    assert len(pad_cell("abc", 10, align)) == 10


@pytest.mark.parametrize("align", list(TableAlign))
def test_pad_cell_does_not_cut_a_longer_text(align) -> None:
    """Verify text wider than the column is returned whole."""

    assert pad_cell("abcdef", 3, align) == "abcdef"


@pytest.mark.parametrize("align", list(TableAlign))
def test_pad_cell_text_of_the_exact_width_is_unchanged(align) -> None:
    """Verify nothing is added when the text already fills the column."""

    assert pad_cell("abc", 3, align) == "abc"


@pytest.mark.parametrize("align", list(TableAlign))
def test_pad_cell_empty_text_becomes_spaces(align) -> None:
    """Verify an empty cell is filled with spaces."""

    assert pad_cell("", 4, align) == "    "
