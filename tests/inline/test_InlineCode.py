import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.inline.InlineCode import InlineCode


def test_inline_code_is_an_inline_node() -> None:
    """Verify the class."""

    assert isinstance(InlineCode("x"), InlineMarkdown)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("code", "`code`"),
        ("a b", "`a b`"),
        # Nothing inside is escaped
        ("*x*", "`*x*`"),
        ("# x", "`# x`"),
        ("<b>&</b>", "`<b>&</b>`"),
        ("\\", "`\\`"),
        # Backticks inside get a longer delimiter
        ("a`b", "``a`b``"),
        ("a``b", "```a``b```"),
        # A backtick at the edge is padded
        ("`a", "`` `a ``"),
        ("a`", "`` a` ``"),
        # Spaces on both sides are kept by padding
        (" a ", "`  a  `"),
        (" a", "` a`"),
    ],
)
def test_inline_code_writes_the_fitting_delimiter(text, expected) -> None:
    """Verify any content can be code, and nothing needs escaping inside it."""

    assert InlineCode(text).to_inline() == expected


@pytest.mark.parametrize(
    "text, stored",
    [
        ("a\nb", "a b"),
        ("a\n\nb", "a  b"),
        ("\na", " a"),
        ("a\n", "a "),
    ],
)
def test_inline_code_turns_line_breaks_into_spaces(text, stored) -> None:
    """Verify a code span stays on one line."""

    node = InlineCode(text)

    assert node.text == stored
    assert "\n" not in node.to_inline()


def test_inline_code_stores_its_text() -> None:
    """Verify the attribute."""

    assert InlineCode("x").text == "x"


def test_inline_code_to_text_and_str() -> None:
    """Verify the inline text is the text."""

    node = InlineCode("x")

    assert node.to_text() == "`x`"
    assert str(node) == "`x`"
    assert node.to_lines() == ("`x`",)


def test_inline_code_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(InlineCode("x"), "__dict__")


@pytest.mark.parametrize("text", [42, 3.14, None, True, ["a"], b"bytes"])
def test_inline_code_rejects_a_text_that_is_not_a_string(subtests, text) -> None:
    """Verify only a string can be code."""

    assert_exception_function(
        subtests,
        InlineCode,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'text'",
        expected="str",
        value=text,
        verbose=False,
    )


@pytest.mark.parametrize("text", ["", " ", "   ", "\t", "\n", " \n\t "])
def test_inline_code_rejects_a_text_with_nothing_visible(subtests, text) -> None:
    """Verify empty or blank text raises the empty card, with the text as it was given."""

    assert_exception_function(
        subtests,
        InlineCode,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_INLINE_CODE_EMPTY",
        value=text,
        verbose=False,
    )
