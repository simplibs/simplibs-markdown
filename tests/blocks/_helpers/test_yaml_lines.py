import pytest
from simplibs.exception import ConversionError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.blocks._helpers import yaml_lines


@pytest.mark.parametrize(
    "value, expected",
    [
        ("a", ['"a"']),
        (5, ["5"]),
        (None, ["null"]),
        (True, ["true"]),
        ({}, ["{}"]),
        ([], ["[]"]),
        ((), ["[]"]),
    ],
)
def test_yaml_lines_scalar_or_empty_collection_is_one_line(value, expected) -> None:
    """Verify a value that fits on a line gives exactly that line."""

    assert yaml_lines(value) == expected


def test_yaml_lines_returns_a_list() -> None:
    """Verify the result is a list of strings."""

    result = yaml_lines({"a": 1})

    assert isinstance(result, list)
    assert all(isinstance(line, str) for line in result)


@pytest.mark.parametrize("depth, pad", [(0, ""), (1, "  "), (2, "    "), (3, "      ")])
def test_yaml_lines_indents_two_spaces_per_level(depth, pad) -> None:
    """Verify `depth` sets the indentation of every line."""

    assert yaml_lines({"a": 1, "b": 2}, depth) == [f"{pad}a: 1", f"{pad}b: 2"]
    assert yaml_lines([1, 2], depth) == [f"{pad}- 1", f"{pad}- 2"]
    assert yaml_lines("a", depth) == [f'{pad}"a"']


@pytest.mark.parametrize(
    "value, expected",
    [
        # A dictionary: one line per key, in the given order
        ({"a": 1, "b": "x"}, ["a: 1", 'b: "x"']),
        ({"b": 1, "a": 2}, ["b: 1", "a: 2"]),
        # A key that needs quotes
        ({"my key": 1, "no": 2}, ['"my key": 1', '"no": 2']),
        # An empty collection stays on the line of its key
        ({"a": {}, "b": []}, ["a: {}", "b: []"]),
        # A nested dictionary goes one level deeper
        ({"a": {"b": 1}}, ["a:", "  b: 1"]),
        ({"a": {"b": {"c": 1}}}, ["a:", "  b:", "    c: 1"]),
        # A list in a dictionary
        ({"tags": ["a", "b"]}, ["tags:", '  - "a"', '  - "b"']),
        ({"tags": ("a",)}, ["tags:", '  - "a"']),
    ],
)
def test_yaml_lines_dictionary(value, expected) -> None:
    """Verify the lines of a dictionary and of what it holds."""

    assert yaml_lines(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        # A list: one dash per item
        ([1, "x", None], ["- 1", '- "x"', "- null"]),
        ((1, 2), ["- 1", "- 2"]),
        # An empty collection stays on the line of its dash
        ([[]], ["- []"]),
        ([{}], ["- {}"]),
        # A nested list: the dash stands alone, the content is one level deeper
        ([[1, 2], [3]], ["-", "  - 1", "  - 2", "-", "  - 3"]),
        # A dictionary in a list
        ([{"a": 1, "b": 2}, {"a": 3}], ["-", "  a: 1", "  b: 2", "-", "  a: 3"]),
        # Mixed
        (["x", {"a": 1}, [True]], ['- "x"', "-", "  a: 1", "-", "  - true"]),
    ],
)
def test_yaml_lines_list(value, expected) -> None:
    """Verify the lines of a list and of what it holds."""

    assert yaml_lines(value) == expected


def test_yaml_lines_a_typical_front_matter() -> None:
    """Verify a realistic front matter, with every kind of value in it."""

    value = {
        "title": "Hello, world",
        "draft": False,
        "weight": 3,
        "tags": ["a", "b"],
        "author": {"name": "X", "links": []},
        "empty": None,
    }

    assert yaml_lines(value) == [
        'title: "Hello, world"',
        "draft: false",
        "weight: 3",
        "tags:",
        '  - "a"',
        '  - "b"',
        "author:",
        '  name: "X"',
        "  links: []",
        "empty: null",
    ]


def test_yaml_lines_rejects_a_key_that_is_not_a_string(subtests) -> None:
    """Verify a dictionary key must be a string."""

    assert_exception_function(
        subtests,
        yaml_lines,
        invalid_params=({1: "a"},),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        value=1,
        verbose=False,
    )


def test_yaml_lines_rejects_a_key_deep_inside(subtests) -> None:
    """Verify the check reaches the nested levels."""

    assert_exception_function(
        subtests,
        yaml_lines,
        invalid_params=({"a": [{"b": {2: 1}}]},),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        value=2,
        verbose=False,
    )


@pytest.mark.parametrize(
    "value, bad",
    [
        ({"a": {1, 2}}, {1, 2}),
        ({"a": b"x"}, b"x"),
        ([1, object], object),
        ({"a": [float("inf")]}, float("inf")),
        ({"a": {"b": [1j]}}, 1j),
    ],
)
def test_yaml_lines_rejects_a_value_it_cannot_write(subtests, value, bad) -> None:
    """Verify an unsupported value, however deep, is an error and not a guess."""

    assert_exception_function(
        subtests,
        yaml_lines,
        invalid_params=(value,),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        value=bad,
        verbose=False,
    )
