import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.enums import FenceChar
from simplibs.markdown.presets.code import MERMAID


def test_mermaid_builds_a_fenced_code_block_with_this_info() -> None:
    """Verify the kind of node, the info string and the level."""

    node = MERMAID("x")

    assert isinstance(node, CodeBlock)
    assert node.info == "mermaid"
    assert node.fence is FenceChar.BACKTICK
    assert node.indented is False
    assert node.node_level is NodeLevel.BLOCK


def test_mermaid_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert MERMAID("graph TD; A-->B").to_lines() == ("```mermaid", "graph TD; A-->B", "```")


@pytest.mark.parametrize(
    "code, expected",
    [
        ("x", ("```mermaid", "x", "```")),
        ("a\nb", ("```mermaid", "a", "b", "```")),
        ("a\n\nb", ("```mermaid", "a", "", "b", "```")),
        # One trailing newline is not a line of code
        ("a\n", ("```mermaid", "a", "```")),
        # Nothing inside is escaped
        ("# x *y* <b>", ("```mermaid", "# x *y* <b>", "```")),
        # No code, no lines inside
        ("", ("```mermaid", "```")),
        # The fence grows when the code holds a fence
        ("a\n```\nb", ("````mermaid", "a", "```", "b", "````")),
    ],
)
def test_mermaid_lines(code, expected) -> None:
    """Verify the fence, the info string and the code lines."""

    assert MERMAID(code).to_lines() == expected


def test_mermaid_has_no_parameter_for_the_info_string() -> None:
    """Verify the info string is fixed by the preset."""

    with pytest.raises(TypeError):
        MERMAID("x", "other")


@pytest.mark.parametrize("code", [42, 3.14, None, True, ["a"], b"bytes"])
def test_mermaid_rejects_code_that_is_not_a_string(subtests, code) -> None:
    """Verify the code block below refuses it."""

    assert_exception_function(
        subtests,
        MERMAID,
        invalid_params=(code,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        value=code,
        verbose=False,
    )
