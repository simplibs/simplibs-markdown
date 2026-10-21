import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.footnote import (
    raise_footnote_label_has_whitespace_error,
)


@pytest.mark.parametrize(
    "label, problem, exception",
    [
        # A wrong string is a ValueError
        ("", "A footnote label cannot be empty or contain whitespace.", ValueError),
        ("two words", "A footnote label cannot be empty or contain whitespace.", ValueError),
        ("tab\tlabel", "A footnote label cannot be empty or contain whitespace.", ValueError),
        # A wrong kind of value is a TypeError
        (1, "The label is not a string.", TypeError),
        (None, "The label is not a string.", TypeError),
        (["note"], "The label is not a string.", TypeError),
    ],
)
def test_raise_footnote_label_has_whitespace_error_contract(
    subtests, label, problem, exception
) -> None:
    """Verify raise_footnote_label_has_whitespace_error chooses the right problem and exception."""

    assert_exception_function(
        subtests,
        raise_footnote_label_has_whitespace_error,
        invalid_params=(label,),
        exception_type=ParamError,
        error_name="MARKDOWN_FOOTNOTE_LABEL_INVALID",
        label="footnote label",
        expected="A non-empty string without spaces or tabs (e.g. '1', 'note').",
        value=label,
        problem=problem,
        how_to_fix=(
            "Use a short label such as '1' or 'source'.",
            "Replace spaces with '-' or '_'.",
        ),
        exception=exception,
        verbose=False,
    )
