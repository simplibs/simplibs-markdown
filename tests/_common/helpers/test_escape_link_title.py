import pytest
from simplibs.markdown._common.helpers import escape_link_title

DQ = '"'
SQ = "'"
BS = "\\"


@pytest.mark.parametrize(
    "title, expected",
    [
        # Double quotes first
        ("Title", f"{DQ}Title{DQ}"),
        ("", f"{DQ}{DQ}"),
        ("two words", f"{DQ}two words{DQ}"),
        # A single quote does not disturb double quotes
        (f"it{SQ}s", f"{DQ}it{SQ}s{DQ}"),
        # A double quote inside moves the title to single quotes
        (f"say {DQ}hi{DQ}", f"{SQ}say {DQ}hi{DQ}{SQ}"),
        # Both kinds: double quotes stay, the inner double quotes are escaped
        (f"it{SQ}s {DQ}x{DQ}", f"{DQ}it{SQ}s {BS}{DQ}x{BS}{DQ}{DQ}"),
        # Backslashes are doubled in every form
        (f"a{BS}b", f"{DQ}a{BS}{BS}b{DQ}"),
        (f"a{BS}{DQ}b", f"{SQ}a{BS}{BS}{DQ}b{SQ}"),
        (f"{BS}{SQ}{DQ}", f"{DQ}{BS}{BS}{SQ}{BS}{DQ}{DQ}"),
    ],
)
def test_escape_link_title(title, expected) -> None:
    """Verify the title gets the quotes that fit it, with escapes only when needed."""

    assert escape_link_title(title) == expected


@pytest.mark.parametrize("title", ["Title", f"it{SQ}s", f"say {DQ}hi{DQ}", f"a{BS}b"])
def test_escape_link_title_never_uses_parentheses(title) -> None:
    """Verify the parenthesis form is never written."""

    result = escape_link_title(title)
    assert result[0] in (DQ, SQ)
    assert result[-1] == result[0]
