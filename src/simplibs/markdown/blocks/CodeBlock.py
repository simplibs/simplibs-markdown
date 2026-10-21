# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import choose_fence
from ._validations.code_block import (
    raise_code_block_indented_with_info_error,
    raise_code_block_info_has_backtick_error,
)
from .enums import FenceChar


class CodeBlock(Markdown):
    """A block of code, fenced or indented.

    Args:
        code: The code. One trailing newline is ignored.
        info: The info string after the opening fence, usually the language.
        fence: The fence character.
        indented: `True` writes an indented block instead of a fenced one.

    Raises:
        ParamError: If a parameter has the wrong type, an indented block gets
            an info string, or a backtick fence has a backtick in its info.
    """

    __slots__ = ("code", "info", "fence", "indented")

    node_level = NodeLevel.BLOCK

    def __init__(
        self,
        code: str,
        info: str | None = None,
        fence: FenceChar = FenceChar.BACKTICK,
        indented: bool = False,
    ) -> None:

        # 1. Validation
        # 1.1 Types
        if not isinstance(code, str):
            raise_param_invalid_type_error("code", code, str)
        if not isinstance(fence, FenceChar):
            raise_param_invalid_type_error("fence", fence, FenceChar)
        if info is not None and not isinstance(info, str):
            raise_param_invalid_type_error("info", info, str)

        # 1.2 The info string needs a fence, and a backtick fence cannot have a backtick in it
        if indented and info:
            raise_code_block_indented_with_info_error(info)
        if info and fence is FenceChar.BACKTICK and "`" in info:
            raise_code_block_info_has_backtick_error(info)

        # 2. Assignment
        self.code = code
        self.info = info.strip() if info else None
        self.fence = fence
        self.indented = indented

    def to_lines(self) -> tuple[str, ...]:

        # 1. One trailing newline is not a line of code
        body = self.code[:-1] if self.code.endswith("\n") else self.code
        rows = body.split("\n") if body else []

        # 2. An indented block: four spaces before every non-empty line
        if self.indented:
            return tuple("    " + row if row else "" for row in rows)

        # 3. A fenced block: the fence is longer than any run inside the code
        fence = choose_fence(self.code, self.fence.value)
        return (fence + (self.info or ""), *rows, fence)


_DESIGN_NOTES = """
# CodeBlock — Code of Any Content

## Purpose
The code is written as it is. The only thing that can go wrong is the fence,
so it is chosen to be longer than any run of its character inside the code.

## Trailing Newline
`"print(1)\\n"` and `"print(1)"` are the same block. Without it a file read
from disk would get an empty last line inside the fence.

## Limit
A line break inside `info` is not checked; it would end the fence line.
"""
