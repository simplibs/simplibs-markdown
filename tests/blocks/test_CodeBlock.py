import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.enums import FenceChar

BACKTICK = FenceChar.BACKTICK
TILDE = FenceChar.TILDE


def test_code_block_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = CodeBlock("x")

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_code_block_defaults() -> None:
    """Verify a backtick fence without an info string."""

    node = CodeBlock("x")

    assert node.info is None
    assert node.fence is BACKTICK
    assert node.indented is False
    assert node.code == "x"


@pytest.mark.parametrize(
    "code, expected",
    [
        ("print(1)", ("```", "print(1)", "```")),
        ("a\nb", ("```", "a", "b", "```")),
        ("a\n\nb", ("```", "a", "", "b", "```")),
        # One trailing newline is not a line of code
        ("print(1)\n", ("```", "print(1)", "```")),
        ("a\n\n", ("```", "a", "", "```")),
        # No code, no lines inside
        ("", ("```", "```")),
        ("\n", ("```", "```")),
        # The code is written as it is
        ("# x\n*y*\n<b>", ("```", "# x", "*y*", "<b>", "```")),
    ],
)
def test_code_block_fenced(code, expected) -> None:
    """Verify the fence around the code lines."""

    assert CodeBlock(code).to_lines() == expected


@pytest.mark.parametrize(
    "info, expected_info, first_line",
    [
        ("python", "python", "```python"),
        ("  python  ", "python", "```python"),
        ("python title=x", "python title=x", "```python title=x"),
        ("", None, "```"),
    ],
)
def test_code_block_info_string(info, expected_info, first_line) -> None:
    """Verify the info string is stripped and written after the opening fence."""

    node = CodeBlock("x", info)

    assert node.info == expected_info
    assert node.to_lines() == (first_line, "x", "```")


@pytest.mark.parametrize(
    "code, fence, expected",
    [
        # The fence is longer than any run of its character inside the code
        ("```", BACKTICK, "````"),
        ("a ``` b", BACKTICK, "````"),
        ("````", BACKTICK, "`````"),
        ("~~~", TILDE, "~~~~"),
        # Only its own character counts
        ("~~~", BACKTICK, "```"),
        ("```", TILDE, "~~~"),
        # The default length is three
        ("x", BACKTICK, "```"),
        ("x", TILDE, "~~~"),
    ],
)
def test_code_block_fence_fits_the_code(code, fence, expected) -> None:
    """Verify the code can never close its own fence."""

    lines = CodeBlock(code, fence=fence).to_lines()

    assert lines[0] == expected
    assert lines[-1] == expected


def test_code_block_tilde_fence_may_have_a_backtick_in_the_info() -> None:
    """Verify the backtick rule applies to backtick fences only."""

    assert CodeBlock("x", "a`b", TILDE).to_lines() == ("~~~a`b", "x", "~~~")


@pytest.mark.parametrize(
    "code, expected",
    [
        ("a", ("    a",)),
        ("a\nb", ("    a", "    b")),
        # An empty line stays empty, without trailing spaces
        ("a\n\nb", ("    a", "", "    b")),
        ("a\n", ("    a",)),
        ("  a", ("      a",)),
        ("", ()),
        ("\n", ()),
    ],
)
def test_code_block_indented(code, expected) -> None:
    """Verify four spaces before every non-empty line, and no fence."""

    node = CodeBlock(code, indented=True)

    assert node.indented is True
    assert node.to_lines() == expected


def test_code_block_to_text_and_str() -> None:
    """Verify the rendered text."""

    node = CodeBlock("a\nb", "py")

    assert node.to_text() == "```py\na\nb\n```"
    assert str(node) == "```py\na\nb\n```"


def test_code_block_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(CodeBlock("x"), "__dict__")


@pytest.mark.parametrize("code", [42, None, 3.14, True, ["a"], b"x"])
def test_code_block_rejects_code_that_is_not_a_string(subtests, code) -> None:
    """Verify the code has to be a string."""

    assert_exception_function(
        subtests,
        CodeBlock,
        invalid_params=(code,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'code'",
        expected="str",
        value=code,
        verbose=False,
    )


@pytest.mark.parametrize("fence", ["`", "~", None, 1, True])
def test_code_block_rejects_a_fence_of_the_wrong_type(subtests, fence) -> None:
    """Verify `fence` has to be a FenceChar."""

    assert_exception_function(
        subtests,
        CodeBlock,
        invalid_params=("x", None, fence),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'fence'",
        expected="FenceChar",
        value=fence,
        verbose=False,
    )


@pytest.mark.parametrize("info", [42, 3.14, True, ["py"], b"py"])
def test_code_block_rejects_an_info_that_is_not_a_string(subtests, info) -> None:
    """Verify the info string has to be a string or None."""

    assert_exception_function(
        subtests,
        CodeBlock,
        invalid_params=("x", info),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'info'",
        expected="str",
        value=info,
        verbose=False,
    )


@pytest.mark.parametrize("info", ["python", "js", "a b"])
def test_code_block_rejects_an_info_for_an_indented_block(subtests, info) -> None:
    """Verify an indented block has no fence to carry an info string."""

    assert_exception_function(
        subtests,
        CodeBlock,
        invalid_params=("x", info, BACKTICK, True),
        exception_type=ParamError,
        error_name="MARKDOWN_CODE_BLOCK_INDENTED_WITH_INFO",
        value=info,
        verbose=False,
    )


@pytest.mark.parametrize("info", ["py`thon", "`", "a ` b"])
def test_code_block_rejects_a_backtick_in_the_info_of_a_backtick_fence(subtests, info) -> None:
    """Verify a backtick would end the opening fence."""

    assert_exception_function(
        subtests,
        CodeBlock,
        invalid_params=("x", info),
        exception_type=ParamError,
        error_name="MARKDOWN_CODE_BLOCK_INFO_HAS_BACKTICK",
        value=info,
        verbose=False,
    )


def test_code_block_an_empty_info_is_fine_for_an_indented_block() -> None:
    """Verify an empty info string is no info string."""

    assert CodeBlock("x", "", indented=True).to_lines() == ("    x",)
