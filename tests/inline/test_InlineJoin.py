import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Text import Text


def test_inline_join_is_an_inline_node() -> None:
    """Verify the class."""

    assert isinstance(InlineJoin("a"), InlineMarkdown)


def test_inline_join_without_parts_is_empty() -> None:
    """Verify no parts give no parts and no text."""

    node = InlineJoin()

    assert node.parts == ()
    assert node.to_inline() == ""
    assert node.to_lines() == ("",)


def test_inline_join_parts_is_a_tuple() -> None:
    """Verify the parts are kept as a tuple."""

    assert isinstance(InlineJoin("a", "b").parts, tuple)


def test_inline_join_strings_become_escaped_text() -> None:
    """Verify every string is turned into a Text."""

    node = InlineJoin("a*", "b")

    assert [type(part) for part in node.parts] == [Text, Text]
    assert node.to_inline() == r"a\*b"


def test_inline_join_keeps_node_parts_as_they_are() -> None:
    """Verify a node given as a part is not copied."""

    first, second = Text("a"), InlineCode("b")

    node = InlineJoin(first, second)

    assert node.parts[0] is first
    assert node.parts[1] is second


def test_inline_join_writes_the_parts_without_a_separator() -> None:
    """Verify the parts follow each other directly."""

    assert InlineJoin("a", Text("b"), InlineCode("c"), "d").to_inline() == "ab`c`d"
    assert InlineJoin("a ", "b").to_inline() == "a b"


def test_inline_join_keeps_raw_text() -> None:
    """Verify a part written without escaping stays raw."""

    assert InlineJoin("a", Text("*b*", escape=False)).to_inline() == r"a*b*"


def test_inline_join_a_nested_join_is_unpacked() -> None:
    """Verify the parts of a join in a join are flat."""

    inner = InlineJoin("a", "b")

    node = InlineJoin(inner, "c")

    assert len(node.parts) == 3
    assert node.parts[0] is inner.parts[0]
    assert node.parts[1] is inner.parts[1]
    assert node.to_inline() == "abc"


def test_inline_join_a_list_part_is_unpacked() -> None:
    """Verify a list of parts gives its content, at any depth."""

    node = InlineJoin(["a", ["b", ("c",)]], "d")

    assert len(node.parts) == 4
    assert node.to_inline() == "abcd"


def test_inline_join_empty_list_part_adds_nothing() -> None:
    """Verify an empty list is a part with no content."""

    assert InlineJoin("a", [], "b").to_inline() == "ab"
    assert len(InlineJoin("a", [], "b").parts) == 2


def test_inline_join_grouping_does_not_matter() -> None:
    """Verify `(a + b) + c` and `a + (b + c)` give the same flat parts."""

    a, b, c = Text("a"), Text("b"), Text("c")

    left = (a + b) + c
    right = a + (b + c)

    assert len(left.parts) == len(right.parts) == 3
    assert left.to_text() == right.to_text() == "abc"


def test_inline_join_lines_follow_the_line_breaks_in_the_text() -> None:
    """Verify a break inside a part gives several lines."""

    node = InlineJoin("a", Text("b\nc", escape=False))

    assert node.to_lines() == ("ab", "c")


def test_inline_join_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(InlineJoin("a"), "__dict__")


@pytest.mark.parametrize("block", [Paragraph("text"), BlankLine()])
def test_inline_join_rejects_a_block_part(subtests, block) -> None:
    """Verify a block node cannot be a part of a line."""

    assert_exception_function(
        subtests,
        InlineJoin,
        invalid_params=("a", block),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, None, True, {"a": 1}])
def test_inline_join_rejects_a_part_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        InlineJoin,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
