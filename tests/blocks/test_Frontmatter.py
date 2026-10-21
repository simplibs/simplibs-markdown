import pytest
from simplibs.exception import ConversionError, ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Frontmatter import Frontmatter


def test_frontmatter_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = Frontmatter({"a": 1})

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


@pytest.mark.parametrize(
    "data, body",
    [
        ({"title": "Hello"}, ['title: "Hello"']),
        ({"a": 1, "b": 2.5, "c": True, "d": None}, ["a: 1", "b: 2.5", "c: true", "d: null"]),
        ({"tags": ["a", "b"]}, ["tags:", '  - "a"', '  - "b"']),
        ({"author": {"name": "X"}}, ["author:", '  name: "X"']),
        ({"my key": 1, "no": 2}, ['"my key": 1', '"no": 2']),
        ({"empty_list": [], "empty_dict": {}}, ["empty_list: []", "empty_dict: {}"]),
    ],
)
def test_frontmatter_lines(data, body) -> None:
    """Verify the YAML between two marker lines."""

    node = Frontmatter(data)

    assert node.to_lines() == ("---", *body, "---")
    assert node.lines == ("---", *body, "---")


def test_frontmatter_to_text_and_str() -> None:
    """Verify the rendered text."""

    node = Frontmatter({"title": "X", "count": 1})

    assert node.to_text() == '---\ntitle: "X"\ncount: 1\n---'
    assert str(node) == '---\ntitle: "X"\ncount: 1\n---'


def test_frontmatter_quotes_a_key_that_yaml_reads_as_a_value() -> None:
    """Verify a key such as `n` or `no` is quoted, so a parser does not turn it into a boolean."""

    assert Frontmatter({"n": 1}).to_lines() == ("---", '"n": 1', "---")


def test_frontmatter_keeps_the_order_of_the_keys() -> None:
    """Verify the output follows the dictionary."""

    assert Frontmatter({"b": 1, "a": 2}).to_lines() == ("---", "b: 1", "a: 2", "---")


def test_frontmatter_is_written_at_construction() -> None:
    """Verify a change to the dictionary afterwards is not reflected."""

    data = {"a": 1}
    node = Frontmatter(data)

    data["a"] = 2
    data["b"] = 3

    assert node.to_lines() == ("---", "a: 1", "---")


def test_frontmatter_stores_the_data() -> None:
    """Verify the attribute."""

    data = {"a": 1}

    assert Frontmatter(data).data == data


def test_frontmatter_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Frontmatter({"a": 1}), "__dict__")


@pytest.mark.parametrize("data", [None, [], ["a"], "a", 42, ("a", 1), {"a"}, 3.14, True])
def test_frontmatter_rejects_data_that_is_not_a_dictionary(subtests, data) -> None:
    """Verify only a dictionary is a header."""

    assert_exception_function(
        subtests,
        Frontmatter,
        invalid_params=(data,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'data'",
        expected="dict",
        value=data,
        verbose=False,
    )


@pytest.mark.parametrize(
    "data, bad",
    [
        ({"a": {1, 2}}, {1, 2}),
        ({"a": b"x"}, b"x"),
        ({"a": [1j]}, 1j),
        ({"a": {"b": object}}, object),
        ({1: "a"}, 1),
        ({"a": {2: "b"}}, 2),
        ({"a": float("inf")}, float("inf")),
    ],
)
def test_frontmatter_rejects_what_yaml_cannot_hold_at_construction(subtests, data, bad) -> None:
    """Verify an unsupported value or key fails where the data is passed."""

    assert_exception_function(
        subtests,
        Frontmatter,
        invalid_params=(data,),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        value=bad,
        verbose=False,
    )


def test_frontmatter_an_empty_dictionary_is_an_empty_header() -> None:
    """Verify no keys give two marker lines, without a `{}` between them."""

    node = Frontmatter({})

    assert node.to_lines() == ("---", "---")
    assert node.to_text() == "---\n---"


def test_frontmatter_nested_empty_values_are_still_written() -> None:
    """Verify only the whole header is special: an empty value inside it stays on its key's line."""

    assert Frontmatter({"a": {}, "b": []}).to_lines() == ("---", "a: {}", "b: []", "---")
