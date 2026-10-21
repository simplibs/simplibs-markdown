import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Reference import Reference
from simplibs.markdown.inline.enums import ReferenceKind
from simplibs.markdown.presets.references import COMMIT_REF


def test_commit_ref_builds_a_commit_reference() -> None:
    """Verify the kind of node, the kind and the level."""

    node = COMMIT_REF("a1b2c3d")

    assert isinstance(node, Reference)
    assert node.kind is ReferenceKind.COMMIT
    assert node.node_level is NodeLevel.INLINE


def test_commit_ref_example_from_the_docstring() -> None:
    """Verify the sentence the docstring promises."""

    result = "Introduced in " + COMMIT_REF("a1b2c3d") + "."

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "Introduced in a1b2c3d."


@pytest.mark.parametrize(
    "value, expected",
    [
        ("a1b2c3d", "a1b2c3d"),
        ("abcdef0", "abcdef0"),
        ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
    ],
)
def test_commit_ref_text(value, expected) -> None:
    """Verify the mark of this kind of reference, and that nothing is escaped."""

    node = COMMIT_REF(value)

    assert node.to_text() == expected
    assert node.to_lines() == (expected,)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "abc",
        "A1B2C3D",
        "ghijklm",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "abc def0",
        42,
    ],
)
def test_commit_ref_rejects_a_value_of_the_wrong_shape(subtests, value) -> None:
    """Verify the shape is checked."""

    assert_exception_function(
        subtests,
        COMMIT_REF,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_REFERENCE_INVALID_VALUE",
        value=value,
        verbose=False,
    )


@pytest.mark.parametrize("value", [None, True, False, 1.5, [], {"a": 1}])
def test_commit_ref_rejects_a_value_that_is_neither_a_string_nor_an_integer(subtests, value) -> None:
    """Verify the type is checked before the shape."""

    assert_exception_function(
        subtests,
        COMMIT_REF,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'value'",
        value=value,
        verbose=False,
    )
