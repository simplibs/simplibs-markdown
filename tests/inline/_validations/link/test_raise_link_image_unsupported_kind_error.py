import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline.enums import LinkKind
from simplibs.markdown.inline._validations.link import (
    raise_link_image_unsupported_kind_error,
)


@pytest.mark.parametrize("kind", [LinkKind.AUTOLINK, LinkKind.BARE])
def test_raise_link_image_unsupported_kind_error_contract(subtests, kind) -> None:
    """Verify raise_link_image_unsupported_kind_error names the link kind and reports image=True."""

    assert_exception_function(
        subtests,
        raise_link_image_unsupported_kind_error,
        invalid_params=(kind,),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_IMAGE_UNSUPPORTED_KIND",
        label="image flag",
        expected="`image=False`, or a kind that supports images.",
        value=True,
        problem=(
            f"An image cannot use the link kind {kind.name}.",
            "Markdown has no image form for it.",
        ),
        how_to_fix=(
            "Use INLINE, REFERENCE, COLLAPSED or SHORTCUT for an image.",
            "Set `image=False` to keep this kind.",
        ),
        exception=ValueError,
        verbose=False,
    )
