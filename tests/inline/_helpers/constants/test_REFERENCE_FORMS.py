import re
from types import MappingProxyType

import pytest
from simplibs.markdown.inline._helpers import REFERENCE_FORMS
from simplibs.markdown.inline.enums import ReferenceKind

TEMPLATES = {
    ReferenceKind.MENTION: "@{}",
    ReferenceKind.TEAM: "@{}",
    ReferenceKind.ISSUE: "#{}",
    ReferenceKind.REPO_ISSUE: "{}",
    ReferenceKind.COMMIT: "{}",
    ReferenceKind.EMOJI: ":{}:",
}

# kind -> (values the pattern must accept, values it must refuse)
EXAMPLES = {
    ReferenceKind.MENTION: (
        ["octocat", "a", "A1", "user-name", "x" * 39],
        ["", "-user", "user_name", "user name", "x" * 40, "a/b", "@user"],
    ),
    ReferenceKind.TEAM: (
        ["org/team", "my-org/team_name", "o/t"],
        ["org", "org/", "/team", "org/team name", "o_rg/team", "a/b/c", "@org/team"],
    ),
    ReferenceKind.ISSUE: (
        ["12", "0", "007"],
        ["", "-1", "1a", "#12", "1.5", " 1"],
    ),
    ReferenceKind.REPO_ISSUE: (
        ["owner/repo#12", "a.b/c-d_e#1"],
        ["owner/repo", "owner#12", "owner/repo#", "owner/repo#1a", "/repo#1", "a b/c#1"],
    ),
    ReferenceKind.COMMIT: (
        ["abcdef0", "a" * 40, "0123456789abcdef"],
        ["", "abcdef", "a" * 41, "ABCDEF0", "ghijklm", "abc def0"],
    ),
    ReferenceKind.EMOJI: (
        ["tada", "+1", "-1", "white_check_mark", "a2"],
        ["", "Tada", "ta da", ":tada:", "ta:da"],
    ),
}


def test_reference_forms_is_read_only() -> None:
    """Verify the table is a read-only mapping."""

    assert isinstance(REFERENCE_FORMS, MappingProxyType)

    with pytest.raises(TypeError):
        REFERENCE_FORMS[ReferenceKind.ISSUE] = ()


def test_reference_forms_covers_every_kind() -> None:
    """Verify no ReferenceKind is missing (a new kind must get an entry)."""

    assert set(REFERENCE_FORMS) == set(ReferenceKind)


@pytest.mark.parametrize("kind", list(ReferenceKind))
def test_reference_forms_entry_shape(kind) -> None:
    """Verify every entry is (pattern, template, description) of the right types."""

    pattern, template, description = REFERENCE_FORMS[kind]

    assert isinstance(pattern, re.Pattern)
    assert isinstance(template, str)
    assert template.count("{}") == 1
    assert isinstance(description, str)
    assert description.strip() != ""


@pytest.mark.parametrize("kind", list(ReferenceKind))
def test_reference_forms_template(kind) -> None:
    """Verify the exact template each kind is written with."""

    assert REFERENCE_FORMS[kind][1] == TEMPLATES[kind]


@pytest.mark.parametrize(
    "kind, value",
    [(kind, value) for kind, (valid, _) in EXAMPLES.items() for value in valid],
)
def test_reference_forms_pattern_accepts(kind, value) -> None:
    """Verify the pattern accepts a valid value in full."""

    assert REFERENCE_FORMS[kind][0].fullmatch(value) is not None


@pytest.mark.parametrize(
    "kind, value",
    [(kind, value) for kind, (_, invalid) in EXAMPLES.items() for value in invalid],
)
def test_reference_forms_pattern_refuses(kind, value) -> None:
    """Verify the pattern refuses a value of the wrong shape."""

    assert REFERENCE_FORMS[kind][0].fullmatch(value) is None


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
def test_reference_forms_template_writes_the_reference(kind, value, expected) -> None:
    """Verify filling the template gives the text GitHub recognizes."""

    assert REFERENCE_FORMS[kind][1].format(value) == expected
