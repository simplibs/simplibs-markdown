# Outers
from ...blocks import CodeBlock


def MERMAID(code: str) -> CodeBlock:
    """Build a block that GitHub draws as a diagram.

    Init Params:
        code (str): The diagram in Mermaid syntax.

    Markdown:
        A fenced code block with the info string `mermaid`.

    Example:
        MERMAID("graph TD; A-->B")
        # Writes:
        # ```mermaid
        # graph TD; A-->B
        # ```

    Note:
        GitHub draws the diagram instead of showing the source. If the code contains a fence
        of backticks, the fence is made longer automatically.
    """
    return CodeBlock(code, info="mermaid")
