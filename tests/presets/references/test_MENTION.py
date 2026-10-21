import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Reference import Reference
from simplibs.markdown.inline.enums import ReferenceKind
from simplibs.markdown.presets.references import MENTION


def test_mention_builds_a_mention_reference() -> None:
    """Verify the kind of node, the kind and the level."""

    node = MENTION("octocat")

    assert isinstance(node, Reference)
    assert node.kind is ReferenceKind.MENTION
    assert node.node_level is NodeLevel.INLINE


def test_mention_example_from_the_docstring() -> None:
    """Verify the sentence the docstring promises."""

    result = "Thanks, " + MENTION("octocat") + "!"

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "Thanks, @octocat!"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("octocat", "@octocat"),
        ("user-name", "@user-name"),
        ("A1", "@A1"),
        ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "@xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
    ],
)
def test_mention_text(value, expected) -> None:
    """Verify the mark of this kind of reference, and that nothing is escaped."""

    node = MENTION(value)

    assert node.to_text() == expected
    assert node.to_lines() == (expected,)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "bad name",
        "@octocat",
        "-user",
        "user_name",
        "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "org/team",
    ],
)
def test_mention_rejects_a_value_of_the_wrong_shape(subtests, value) -> None:
    """Verify the shape is checked."""

    assert_exception_function(
        subtests,
        MENTION,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_REFERENCE_INVALID_VALUE",
        value=value,
        verbose=False,
    )


@pytest.mark.parametrize("value", [None, True, False, 1.5, [], {"a": 1}])
def test_mention_rejects_a_value_that_is_neither_a_string_nor_an_integer(subtests, value) -> None:
    """Verify the type is checked before the shape."""

    assert_exception_function(
        subtests,
        MENTION,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'value'",
        value=value,
        verbose=False,
    )
