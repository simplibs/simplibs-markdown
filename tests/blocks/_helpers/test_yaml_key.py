import pytest
from simplibs.exception import ConversionError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.blocks._helpers import yaml_key


@pytest.mark.parametrize(
    "key",
    ["title", "last-updated", "_id", "a1", "A", "x_y", "Title", "once", "nope", "none", "k9"],
)
def test_yaml_key_plain_word_is_written_bare(key) -> None:
    """Verify a plain word stays readable."""

    assert yaml_key(key) == key


@pytest.mark.parametrize(
    "key",
    ["true", "false", "null", "yes", "no", "on", "off", "y", "n",
     "True", "NO", "Yes", "NULL", "On", "OFF", "Y", "N"],
)
def test_yaml_key_reserved_word_is_quoted_in_any_case(key) -> None:
    """Verify a key that YAML 1.1 would read as a value is quoted, whatever its case."""

    assert yaml_key(key) == f'"{key}"'


@pytest.mark.parametrize(
    "key, expected",
    [
        ("my key", '"my key"'),
        ("1st", '"1st"'),
        ("-a", '"-a"'),
        ("a:b", '"a:b"'),
        ("a.b", '"a.b"'),
        ("a#b", '"a#b"'),
        ("", '""'),
        ('say "x"', r'"say \"x\""'),
        ("a\\b", r'"a\\b"'),
        ("line\nbreak", r'"line\nbreak"'),
        # Non-ASCII stays readable in quotes
        ("název x", '"název x"'),
        ("日本 語", '"日本 語"'),
    ],
)
def test_yaml_key_other_key_is_quoted(key, expected) -> None:
    """Verify every key that is no plain word is a double-quoted string."""

    assert yaml_key(key) == expected


@pytest.mark.parametrize("key", [1, 1.5, None, True, ("a",), b"a", object])
def test_yaml_key_rejects_a_key_that_is_not_a_string(subtests, key) -> None:
    """Verify only strings are keys."""

    assert_exception_function(
        subtests,
        yaml_key,
        invalid_params=(key,),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        value=key,
        verbose=False,
    )


@pytest.mark.parametrize(
    "key, expected",
    [
        ("název", '"název"'),
        ("živnost", '"živnost"'),
        ("a-č", '"a-č"'),
        ("日本", '"日本"'),
        ("a_é", '"a_é"'),
    ],
)
def test_yaml_key_a_key_with_a_non_ascii_letter_is_always_quoted(key, expected) -> None:
    """Verify the rule does not depend on where the letter stands in the key."""

    assert yaml_key(key) == expected
