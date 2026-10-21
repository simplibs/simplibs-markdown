import pytest
from simplibs.markdown.containers._helpers import separator_cell
from simplibs.markdown.containers.enums import TableAlign


@pytest.mark.parametrize(
    "width, align, expected",
    [
        (3, TableAlign.NONE, "---"),
        (5, TableAlign.NONE, "-----"),
        (3, TableAlign.LEFT, ":--"),
        (5, TableAlign.LEFT, ":----"),
        (3, TableAlign.RIGHT, "--:"),
        (5, TableAlign.RIGHT, "----:"),
        (3, TableAlign.CENTER, ":-:"),
        (5, TableAlign.CENTER, ":---:"),
    ],
)
def test_separator_cell(width, align, expected) -> None:
    """Verify the dashes and the colons that carry the alignment."""

    assert separator_cell(width, align) == expected


@pytest.mark.parametrize("align", list(TableAlign))
@pytest.mark.parametrize("width", [3, 4, 5, 10, 40])
def test_separator_cell_has_the_column_width(width, align) -> None:
    """Verify the separator is as wide as the column, so the source lines up."""

    assert len(separator_cell(width, align)) == width


@pytest.mark.parametrize("align", list(TableAlign))
def test_separator_cell_has_only_dashes_and_colons(align) -> None:
    """Verify nothing else can get into the separator row."""

    assert set(separator_cell(6, align)) <= {"-", ":"}


@pytest.mark.parametrize(
    "align, left_colon, right_colon",
    [
        (TableAlign.NONE, False, False),
        (TableAlign.LEFT, True, False),
        (TableAlign.RIGHT, False, True),
        (TableAlign.CENTER, True, True),
    ],
)
def test_separator_cell_colons_say_the_alignment(align, left_colon, right_colon) -> None:
    """Verify a colon on the left means left, on the right means right, on both means center."""

    result = separator_cell(6, align)

    assert result.startswith(":") is left_colon
    assert result.endswith(":") is right_colon
