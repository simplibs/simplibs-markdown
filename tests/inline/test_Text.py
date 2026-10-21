import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.Text import Text


def test_text_is_an_inline_node() -> None:
    """Verify the class and the level."""

    node = Text("a")

    assert isinstance(node, InlineMarkdown)
    assert node.node_level is NodeLevel.INLINE


def test_text_stores_its_parameters() -> None:
    """Verify the attributes and the default of `escape`."""

    node = Text("a*b")

    assert node.value == "a*b"
    assert node.escape is True
    assert Text("a", escape=False).escape is False
    assert Text("a", False).escape is False


@pytest.mark.parametrize(
    "value, expected",
    [
        ("", ""),
        ("plain", "plain"),
        ("a*b", r"a\*b"),
        ("snake_case", r"snake\_case"),
        ("# not a heading", r"\# not a heading"),
        ("2024. was a year", r"2024\. was a year"),
        ("a\n# b", "a\n" + r"\# b"),
    ],
)
def test_text_escapes_by_default(value, expected) -> None:
    """Verify a string is content, so what Markdown could read is escaped."""

    assert Text(value).to_inline() == expected


@pytest.mark.parametrize("value", ["", "plain", "*bold*", "# heading", "- item", "a\nb", "[link](url)"])
def test_text_without_escape_is_written_as_it_is(value) -> None:
    """Verify `escape=False` lets raw Markdown through."""

    assert Text(value, escape=False).to_inline() == value


@pytest.mark.parametrize("escape", [True, False])
def test_text_to_text_is_to_inline(escape) -> None:
    """Verify an inline node is one string."""

    node = Text("a*b\n# c", escape=escape)

    assert node.to_text() == node.to_inline()
    assert str(node) == node.to_inline()


def test_text_to_lines_splits_at_line_breaks() -> None:
    """Verify a text with a line break has several lines, each escaped on its own."""

    assert Text("a\n# b").to_lines() == ("a", r"\# b")
    assert Text("one line").to_lines() == ("one line",)
    assert Text("").to_lines() == ("",)


def test_text_repr() -> None:
    """Verify the representation shows the written text."""

    assert repr(Text("x")) == "Text('x')"
    assert repr(Text("a*b")) == f"Text({Text('a*b').to_text()!r})"


def test_text_has_no_instance_dict() -> None:
    """Verify slots are in force, so a stray attribute is refused."""

    node = Text("a")

    assert not hasattr(node, "__dict__")
    with pytest.raises(AttributeError):
        node.extra = 1


@pytest.mark.parametrize("value", [42, 3.14, None, True, ["a"], b"bytes", {"a": 1}])
def test_text_rejects_a_value_that_is_not_a_string(subtests, value) -> None:
    """Verify only a string is text."""

    assert_exception_function(
        subtests,
        Text,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'value'",
        expected="str",
        value=value,
        verbose=False,
    )
