import pytest
from simplibs.exception import ConversionError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.blocks._helpers import yaml_inline


@pytest.mark.parametrize(
    "value, expected",
    [
        # The words YAML knows
        (None, "null"),
        (True, "true"),
        (False, "false"),
        # Integers (a bool is tested before them)
        (0, "0"),
        (42, "42"),
        (-7, "-7"),
        (10 ** 20, "100000000000000000000"),
        # Floats stay floats
        (1.5, "1.5"),
        (-0.5, "-0.5"),
        (0.1, "0.1"),
        (2.0, "2.0"),
        (1e20, "1e+20"),
        # Empty collections
        ({}, "{}"),
        ([], "[]"),
        ((), "[]"),
    ],
)
def test_yaml_inline_scalars_and_empty_collections(value, expected) -> None:
    """Verify the YAML text of a value that fits on one line."""

    assert yaml_inline(value) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("text", '"text"'),
        ("", '""'),
        # Words that would otherwise become something else
        ("yes", '"yes"'),
        ("null", '"null"'),
        ("1.0", '"1.0"'),
        ("2024-01-01", '"2024-01-01"'),
        # Escapes
        ('say "hi"', r'"say \"hi\""'),
        ("line\nbreak", r'"line\nbreak"'),
        ("tab\there", r'"tab\there"'),
        ("a\\b", r'"a\\b"'),
        # Non-ASCII stays readable
        ("název", '"název"'),
        ("日本語", '"日本語"'),
    ],
)
def test_yaml_inline_strings_are_always_quoted(text, expected) -> None:
    """Verify a string is a double-quoted token, so it can never be read as another type."""

    assert yaml_inline(text) == expected


def test_yaml_inline_true_is_not_the_number_one() -> None:
    """Verify a bool is not written as an integer."""

    assert yaml_inline(True) == "true"
    assert yaml_inline(1) == "1"
    assert yaml_inline(False) == "false"
    assert yaml_inline(0) == "0"


@pytest.mark.parametrize("value", [float("inf"), float("-inf")])
def test_yaml_inline_rejects_infinity(subtests, value) -> None:
    """Verify infinity has no YAML form here."""

    assert_exception_function(
        subtests,
        yaml_inline,
        invalid_params=(value,),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        value=value,
        verbose=False,
    )


def test_yaml_inline_rejects_nan(subtests) -> None:
    """Verify NaN has no YAML form here (its value is not compared: nan != nan)."""

    assert_exception_function(
        subtests,
        yaml_inline,
        invalid_params=(float("nan"),),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        verbose=False,
    )


@pytest.mark.parametrize(
    "value",
    [{1, 2}, b"bytes", 1 + 2j, object, {"a": 1}, [1], (1,), [[]], [{}]],
)
def test_yaml_inline_rejects_everything_else(subtests, value) -> None:
    """Verify a non-empty collection or an unsupported type is an error, not a guess."""

    assert_exception_function(
        subtests,
        yaml_inline,
        invalid_params=(value,),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        value=value,
        verbose=False,
    )
