import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.inline.Math import Math


def test_math_is_an_inline_node() -> None:
    """Verify the class."""

    assert isinstance(Math("x"), InlineMarkdown)


def test_math_stores_its_parameters() -> None:
    """Verify the attributes and the default of `display`."""

    node = Math("x^2")

    assert node.expr == "x^2"
    assert node.display is False
    assert Math("x", display=True).display is True
    assert Math("x", True).display is True


@pytest.mark.parametrize(
    "expr, display, expected",
    [
        ("x^2", False, "$x^2$"),
        ("x^2", True, "$$x^2$$"),
        ("E = mc^2", False, "$E = mc^2$"),
        (r"\frac{a}{b}", False, r"$\frac{a}{b}$"),
        # Nothing is escaped: `Text` would escape the underscore and the backslash
        ("a_b", False, "$a_b$"),
        ("a_b", True, "$$a_b$$"),
    ],
)
def test_math_writes_the_dollars(expr, display, expected) -> None:
    """Verify one dollar for inline math, two for display math."""

    assert Math(expr, display).to_inline() == expected


@pytest.mark.parametrize(
    "expr, stored",
    [
        ("  x  ", "x"),
        ("\tx", "x"),
        ("x\n", "x"),
        (" a b ", "a b"),
    ],
)
def test_math_strips_the_expression(expr, stored) -> None:
    """Verify the edge whitespace is dropped, so it cannot spoil the dollars."""

    node = Math(expr)

    assert node.expr == stored
    assert node.to_inline() == f"${stored}$"


def test_math_to_text_and_str() -> None:
    """Verify the inline text is the text."""

    node = Math("x")

    assert node.to_text() == "$x$"
    assert str(node) == "$x$"
    assert node.to_lines() == ("$x$",)


def test_math_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Math("x"), "__dict__")


@pytest.mark.parametrize("expr", [42, 3.14, None, True, ["x"], b"x"])
def test_math_rejects_an_expression_that_is_not_a_string(subtests, expr) -> None:
    """Verify only a string can be an expression."""

    assert_exception_function(
        subtests,
        Math,
        invalid_params=(expr,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'expr'",
        expected="str",
        value=expr,
        verbose=False,
    )


@pytest.mark.parametrize("expr", ["", " ", "   ", "\t", "\n", " \n\t "])
def test_math_rejects_an_expression_with_nothing_visible(subtests, expr) -> None:
    """Verify empty or blank text raises the empty card, with the text as it was given."""

    assert_exception_function(
        subtests,
        Math,
        invalid_params=(expr,),
        exception_type=ParamError,
        error_name="MARKDOWN_MATH_EMPTY_EXPRESSION",
        value=expr,
        verbose=False,
    )
