import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.LinkDefinition import LinkDefinition


def test_link_definition_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = LinkDefinition("docs", "https://x.com")

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_link_definition_stores_its_parameters() -> None:
    """Verify the attributes."""

    node = LinkDefinition("docs", "https://x.com", "Title")

    assert node.label == "docs"
    assert node.dest == "https://x.com"
    assert node.title == "Title"
    assert LinkDefinition("docs", "u").title is None


@pytest.mark.parametrize(
    "arguments, expected",
    [
        (("docs", "https://x.com"), "[docs]: https://x.com"),
        (("docs", "u", "Title"), '[docs]: u "Title"'),
        # An empty title is no title
        (("docs", "u", ""), "[docs]: u"),
        # A destination with a space goes into angle brackets
        (("docs", "my file.pdf"), "[docs]: <my file.pdf>"),
        # A title with a double quote moves to single quotes
        (("docs", "u", 'say "hi"'), "[docs]: u 'say \"hi\"'"),
        # Brackets and backslashes in the label would end it early
        (("a[b]c", "u"), r"[a\[b\]c]: u"),
        (("a\\b", "u"), r"[a\\b]: u"),
    ],
)
def test_link_definition_line(arguments, expected) -> None:
    """Verify the one line of the definition."""

    node = LinkDefinition(*arguments)

    assert node.to_lines() == (expected,)
    assert node.to_text() == expected
    assert str(node) == expected


@pytest.mark.parametrize(
    "label, stored",
    [
        ("Foo   Bar", "Foo Bar"),
        ("  Foo Bar  ", "Foo Bar"),
        ("Foo\tBar", "Foo Bar"),
        ("Foo\nBar", "Foo Bar"),
        ("FOO", "FOO"),
    ],
)
def test_link_definition_label_is_normalized(label, stored) -> None:
    """Verify the label is stored and written with its whitespace collapsed."""

    node = LinkDefinition(label, "u")

    assert node.label == stored
    assert node.to_lines() == (f"[{stored}]: u",)


def test_link_definition_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(LinkDefinition("a", "u"), "__dict__")


@pytest.mark.parametrize("label", [42, None, 3.14, True, ["a"]])
def test_link_definition_rejects_a_label_that_is_not_a_string(subtests, label) -> None:
    """Verify the label has to be a string."""

    assert_exception_function(
        subtests,
        LinkDefinition,
        invalid_params=(label, "u"),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'label'",
        expected="str",
        value=label,
        verbose=False,
    )


@pytest.mark.parametrize("dest", [42, 3.14, True, ["u"], b"u"])
def test_link_definition_rejects_a_destination_that_is_not_a_string(subtests, dest) -> None:
    """Verify the destination has to be a string (None is an empty destination, below)."""

    assert_exception_function(
        subtests,
        LinkDefinition,
        invalid_params=("a", dest),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'dest'",
        expected="str",
        value=dest,
        verbose=False,
    )


@pytest.mark.parametrize("title", [42, 3.14, True, ["t"], b"t"])
def test_link_definition_rejects_a_title_that_is_not_a_string(subtests, title) -> None:
    """Verify the title has to be a string or None."""

    assert_exception_function(
        subtests,
        LinkDefinition,
        invalid_params=("a", "u", title),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'title'",
        expected="str",
        value=title,
        verbose=False,
    )


@pytest.mark.parametrize("label", ["", " ", "   ", "\t", "\n", " \n\t "])
def test_link_definition_rejects_an_empty_label(subtests, label) -> None:
    """Verify the label is judged after its whitespace is collapsed."""

    assert_exception_function(
        subtests,
        LinkDefinition,
        invalid_params=(label, "u"),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_DEFINITION_EMPTY_LABEL",
        verbose=False,
    )


@pytest.mark.parametrize("dest", [None, ""])
def test_link_definition_rejects_an_empty_destination(subtests, dest) -> None:
    """Verify a definition points somewhere."""

    assert_exception_function(
        subtests,
        LinkDefinition,
        invalid_params=("a", dest),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_DEFINITION_EMPTY_DESTINATION",
        value=dest,
        verbose=False,
    )
