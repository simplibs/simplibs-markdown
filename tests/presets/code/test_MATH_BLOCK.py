import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.enums import FenceChar
from simplibs.markdown.presets.code import MATH_BLOCK


def test_math_block_builds_a_fenced_code_block_with_this_info() -> None:
    """Verify the kind of node, the info string and the level."""

    node = MATH_BLOCK("x")

    assert isinstance(node, CodeBlock)
    assert node.info == "math"
    assert node.fence is FenceChar.BACKTICK
    assert node.indented is False
    assert node.node_level is NodeLevel.BLOCK


def test_math_block_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert MATH_BLOCK("E = mc^2").to_lines() == ("```math", "E = mc^2", "```")


@pytest.mark.parametrize(
    "code, expected",
    [
        ("x", ("```math", "x", "```")),
        ("a\nb", ("```math", "a", "b", "```")),
        ("a\n\nb", ("```math", "a", "", "b", "```")),
        # One trailing newline is not a line of code
        ("a\n", ("```math", "a", "```")),
        # Nothing inside is escaped
        ("# x *y* <b>", ("```math", "# x *y* <b>", "```")),
        # No code, no lines inside
        ("", ("```math", "```")),
        # The fence grows when the code holds a fence
        ("a\n```\nb", ("````math", "a", "```", "b", "````")),
    ],
)
def test_math_block_lines(code, expected) -> None:
    """Verify the fence, the info string and the code lines."""

    assert MATH_BLOCK(code).to_lines() == expected


def test_math_block_has_no_parameter_for_the_info_string() -> None:
    """Verify the info string is fixed by the preset."""

    with pytest.raises(TypeError):
        MATH_BLOCK("x", "other")


@pytest.mark.parametrize("code", [42, 3.14, None, True, ["a"], b"bytes"])
def test_math_block_rejects_code_that_is_not_a_string(subtests, code) -> None:
    """Verify the code block below refuses it."""

    assert_exception_function(
        subtests,
        MATH_BLOCK,
        invalid_params=(code,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        value=code,
        verbose=False,
    )
