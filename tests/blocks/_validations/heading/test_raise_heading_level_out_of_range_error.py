import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.heading import (
    raise_heading_level_out_of_range_error,
)


@pytest.mark.parametrize(
    "level, problem, exception",
    [
        # A wrong number is a ValueError
        (0, "Markdown has six heading levels.", ValueError),
        (7, "Markdown has six heading levels.", ValueError),
        (-1, "Markdown has six heading levels.", ValueError),
        # A wrong kind of value is a TypeError (a bool is not a number here)
        ("2", "The level is not an integer.", TypeError),
        (2.5, "The level is not an integer.", TypeError),
        (None, "The level is not an integer.", TypeError),
        (True, "The level is not an integer.", TypeError),
    ],
)
def test_raise_heading_level_out_of_range_error_contract(
    subtests, level, problem, exception
) -> None:
    """Verify raise_heading_level_out_of_range_error chooses the right problem and exception."""

    assert_exception_function(
        subtests,
        raise_heading_level_out_of_range_error,
        invalid_params=(level,),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_LEVEL_OUT_OF_RANGE",
        label="heading level",
        expected="An integer from 1 to 6.",
        value=level,
        problem=problem,
        how_to_fix=(
            "Pass a level from 1 (the biggest) to 6 (the smallest).",
            "Use the presets H1 to H6 to avoid the number.",
        ),
        exception=exception,
        verbose=False,
    )
