import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.inline._helpers import REFERENCE_FORMS
from simplibs.markdown.inline.Reference import Reference
from simplibs.markdown.inline.enums import ReferenceKind


def test_reference_is_an_inline_node() -> None:
    """Verify the class."""

    assert isinstance(Reference(ReferenceKind.ISSUE, 1), InlineMarkdown)


@pytest.mark.parametrize(
    "kind, value, expected",
    [
        (ReferenceKind.MENTION, "octocat", "@octocat"),
        (ReferenceKind.TEAM, "org/team", "@org/team"),
        (ReferenceKind.ISSUE, "12", "#12"),
        (ReferenceKind.REPO_ISSUE, "owner/repo#12", "owner/repo#12"),
        (ReferenceKind.COMMIT, "abcdef0", "abcdef0"),
        (ReferenceKind.EMOJI, "tada", ":tada:"),
    ],
)
def test_reference_is_written_with_the_mark_of_its_kind(kind, value, expected) -> None:
    """Verify the leading mark of each kind, and that nothing is escaped (`#12` must stay `#12`)."""

    node = Reference(kind, value)

    assert node.to_inline() == expected
    assert node.to_text() == expected
    assert str(node) == expected
    assert node.to_lines() == (expected,)


def test_reference_stores_its_parameters_as_given_and_as_text() -> None:
    """Verify the kind is kept and the value is kept as a string."""

    node = Reference(ReferenceKind.MENTION, "octocat")

    assert node.kind is ReferenceKind.MENTION
    assert node.value == "octocat"


@pytest.mark.parametrize("value", [12, 0, 7])
def test_reference_accepts_a_number_for_an_issue(value) -> None:
    """Verify an issue number may be an integer; it is stored as text."""

    node = Reference(ReferenceKind.ISSUE, value)

    assert node.value == str(value)
    assert node.to_inline() == f"#{value}"


@pytest.mark.parametrize("kind", list(ReferenceKind))
def test_reference_has_a_form_for_every_kind(kind) -> None:
    """Verify a valid example of every kind can be created (a new kind needs an entry)."""

    examples = {
        ReferenceKind.MENTION: "octocat",
        ReferenceKind.TEAM: "org/team",
        ReferenceKind.ISSUE: "1",
        ReferenceKind.REPO_ISSUE: "o/r#1",
        ReferenceKind.COMMIT: "abcdef0",
        ReferenceKind.EMOJI: "tada",
    }

    assert Reference(kind, examples[kind]).value == examples[kind]


def test_reference_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Reference(ReferenceKind.ISSUE, 1), "__dict__")


@pytest.mark.parametrize("kind", ["mention", "issue", None, 1, True])
def test_reference_rejects_a_kind_of_the_wrong_type(subtests, kind) -> None:
    """Verify `kind` has to be a ReferenceKind."""

    assert_exception_function(
        subtests,
        Reference,
        invalid_params=(kind, "x"),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'kind'",
        expected="ReferenceKind",
        value=kind,
        verbose=False,
    )


@pytest.mark.parametrize(
    "kind, value",
    [
        (ReferenceKind.MENTION, "bad name"),
        (ReferenceKind.MENTION, ""),
        (ReferenceKind.MENTION, "@octocat"),
        (ReferenceKind.TEAM, "org"),
        (ReferenceKind.ISSUE, "x"),
        (ReferenceKind.ISSUE, -1),
        (ReferenceKind.ISSUE, "#12"),
        (ReferenceKind.REPO_ISSUE, "owner/repo"),
        (ReferenceKind.COMMIT, "XYZ"),
        (ReferenceKind.COMMIT, "abc"),
        (ReferenceKind.EMOJI, "Tada"),
        (ReferenceKind.EMOJI, ":tada:"),
    ],
)
def test_reference_rejects_a_value_that_does_not_fit_the_kind(subtests, kind, value) -> None:
    """Verify the card carries the description of the valid form, taken from the one table."""

    assert_exception_function(
        subtests,
        Reference,
        invalid_params=(kind, value),
        exception_type=ParamError,
        error_name="MARKDOWN_REFERENCE_INVALID_VALUE",
        expected=REFERENCE_FORMS[kind][2],
        value=value,
        verbose=False,
    )


@pytest.mark.parametrize("kind", list(ReferenceKind))
@pytest.mark.parametrize("value", [None, True, False, 1.5, [], ["a"], {"a": 1}, b"x", object])
def test_reference_rejects_a_value_that_is_neither_a_string_nor_an_integer(subtests, kind, value) -> None:
    """Verify the type is checked before the shape: `None` and `True` must not become `@None` and `@True`."""

    assert_exception_function(
        subtests,
        Reference,
        invalid_params=(kind, value),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'value'",
        value=value,
        verbose=False,
    )
