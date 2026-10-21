import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Link import Link
from simplibs.markdown.inline.enums import LinkKind
from simplibs.markdown.presets.links import BARE_URL


def test_bare_url_builds_a_link_of_this_kind() -> None:
    """Verify the kind of node, the kind, that it is no image, and the level."""

    node = BARE_URL("https://example.com")

    assert isinstance(node, Link)
    assert node.kind is LinkKind.BARE
    assert node.image is False
    assert node.text is None
    assert node.dest == "https://example.com"
    assert node.node_level is NodeLevel.INLINE


def test_bare_url_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert BARE_URL("https://example.com").to_text() == "https://example.com"


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://example.com", "https://example.com"),
        ("https://example.com/a?b=c&d=e", "https://example.com/a?b=c&d=e"),
        ("mailto:me@example.com", "mailto:me@example.com"),
    ],
)
def test_bare_url_url(url, expected) -> None:
    """Verify the address is written as it is."""

    assert BARE_URL(url).to_text() == expected


def test_bare_url_stands_inside_a_line() -> None:
    """Verify it can be added to text, like any inline node."""

    result = "See " + BARE_URL("https://example.com") + "."

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "See https://example.com."


@pytest.mark.parametrize("url", ["", None])
def test_bare_url_rejects_an_empty_url(subtests, url) -> None:
    """Verify there has to be an address."""

    assert_exception_function(
        subtests,
        BARE_URL,
        invalid_params=(url,),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_EMPTY_DESTINATION",
        value=url,
        verbose=False,
    )


@pytest.mark.parametrize("url", [42, 3.14, True, ["u"], b"u"])
def test_bare_url_rejects_a_url_that_is_not_a_string(subtests, url) -> None:
    """Verify the address has to be a string."""

    assert_exception_function(
        subtests,
        BARE_URL,
        invalid_params=(url,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'dest'",
        expected="str",
        value=url,
        verbose=False,
    )
