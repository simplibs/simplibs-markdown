import re


def choose_fence(code: str, char: str = "`") -> str:
    """Pick a code fence longer than any run of its character inside the code.

    Args:
        code: The code to be fenced.
        char: The fence character (a backtick or a tilde).

    Returns:
        The fence: the character repeated at least three times.
    """

    # 1. Find the longest run of the fence character inside the code
    runs = re.findall(re.escape(char) + "+", code)
    longest = max((len(run) for run in runs), default=0)

    # 2. One more than that, and never fewer than three
    return char * max(3, longest + 1)


_DESIGN_NOTES = """
# choose_fence — Code That Contains a Fence

## Purpose
A code block that shows another code block (this documentation, for one)
cannot be fenced with three backticks. A fence one longer than the longest run
inside can never be closed by the code itself.

## Only the Same Character
A tilde fence is not closed by backticks, so only runs of the chosen
character count.
"""
