import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.inline.Entity import Entity


def _make(arguments: dict) -> Entity:
    """Create an Entity from keyword arguments."""

    return Entity(**arguments)


def test_entity_is_an_inline_node() -> None:
    """Verify the class."""

    assert isinstance(Entity("copy"), InlineMarkdown)


@pytest.mark.parametrize(
    "name, expected",
    [
        ("copy", "&copy;"),
        ("nbsp", "&nbsp;"),
        ("amp", "&amp;"),
        ("lt", "&lt;"),
        ("gt", "&gt;"),
        ("quot", "&quot;"),
        ("hellip", "&hellip;"),
        # The name is accepted with or without the '&' and the ';'
        ("&copy;", "&copy;"),
        ("&copy", "&copy;"),
        ("copy;", "&copy;"),
    ],
)
def test_entity_by_name(name, expected) -> None:
    """Verify a name is written between '&' and ';'."""

    assert Entity(name).to_inline() == expected


@pytest.mark.parametrize(
    "codepoint, expected",
    [
        (169, "&#169;"),
        (0, "&#0;"),
        (8203, "&#8203;"),
        (0x10FFFF, "&#1114111;"),
    ],
)
def test_entity_by_codepoint(codepoint, expected) -> None:
    """Verify a code point is written after '&#', in decimal."""

    assert Entity(codepoint=codepoint).to_inline() == expected


def test_entity_stores_only_what_was_given() -> None:
    """Verify the name is stripped and the other attribute is None."""

    by_name = Entity("&copy;")
    by_code = Entity(codepoint=169)

    assert by_name.name == "copy"
    assert by_name.codepoint is None
    assert by_code.name is None
    assert by_code.codepoint == 169


def test_entity_is_not_escaped() -> None:
    """Verify the ampersand stays, so the entity is rendered and not shown as text."""

    assert Entity("amp").to_text().startswith("&")
    assert "\\" not in Entity("amp").to_text()


def test_entity_to_text_and_str() -> None:
    """Verify the inline text is the text."""

    node = Entity("copy")

    assert node.to_text() == "&copy;"
    assert str(node) == "&copy;"
    assert node.to_lines() == ("&copy;",)


def test_entity_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Entity("copy"), "__dict__")


@pytest.mark.parametrize(
    "arguments, name, codepoint",
    [
        ({}, None, None),
        ({"name": "copy", "codepoint": 169}, "copy", 169),
        ({"name": "amp", "codepoint": 0}, "amp", 0),
    ],
)
def test_entity_rejects_both_or_neither(subtests, arguments, name, codepoint) -> None:
    """Verify exactly one of `name` and `codepoint` is required."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(arguments,),
        exception_type=ParamError,
        error_name="MARKDOWN_ENTITY_NAME_XOR_CODEPOINT",
        value={"name": name, "codepoint": codepoint},
        verbose=False,
    )


@pytest.mark.parametrize("name", [42, 3.14, True, ["copy"], b"copy"])
def test_entity_rejects_a_name_that_is_not_a_string(subtests, name) -> None:
    """Verify the name has to be a string."""

    assert_exception_function(
        subtests,
        Entity,
        invalid_params=(name,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'name'",
        expected="str",
        value=name,
        verbose=False,
    )


@pytest.mark.parametrize(
    "name, shown",
    [
        ("copyy", "copyy"),
        ("notanentity", "notanentity"),
        ("&copyy;", "copyy"),     # the card shows the stripped name
        ("", ""),
        ("&;", ""),
    ],
)
def test_entity_rejects_an_unknown_name(subtests, name, shown) -> None:
    """Verify a typo is an error and not a literal `&copyy;` in the document."""

    assert_exception_function(
        subtests,
        Entity,
        invalid_params=(name,),
        exception_type=ParamError,
        error_name="MARKDOWN_ENTITY_UNKNOWN_NAME",
        value=shown,
        verbose=False,
    )


@pytest.mark.parametrize("codepoint", [-1, 0x110000, 10 ** 10, "169", 169.0, True, False, [169]])
def test_entity_rejects_a_codepoint_that_is_not_valid(subtests, codepoint) -> None:
    """Verify the code point must be an integer in the Unicode range (a bool is not an integer here)."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"codepoint": codepoint},),
        exception_type=ParamError,
        error_name="MARKDOWN_ENTITY_CODEPOINT_OUT_OF_RANGE",
        value=codepoint,
        verbose=False,
    )
