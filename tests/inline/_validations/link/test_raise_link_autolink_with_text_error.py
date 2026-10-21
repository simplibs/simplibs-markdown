import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline.enums import LinkKind
from simplibs.markdown.inline._validations.link import (
    raise_link_autolink_with_text_error,
)


@pytest.mark.parametrize("kind", [LinkKind.AUTOLINK, LinkKind.BARE])
def test_raise_link_autolink_with_text_error_contract(subtests, kind) -> None:
    """Verify raise_link_autolink_with_text_error names the link kind."""

    assert_exception_function(
        subtests,
        raise_link_autolink_with_text_error,
        invalid_params=(kind,),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_AUTOLINK_WITH_TEXT",
        label="link text",
        expected="`text` left as None.",
        problem=(
            f"A link of kind {kind.name} shows its destination as the text.",
            "It cannot carry a separate text.",
        ),
        how_to_fix=(
            "Remove `text`.",
            "Use LinkKind.INLINE when the link needs its own text.",
        ),
        exception=ValueError,
        verbose=False,
    )
