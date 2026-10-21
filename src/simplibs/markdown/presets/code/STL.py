# Outers
from ...blocks import CodeBlock


def STL(code: str) -> CodeBlock:
    """Build a block that GitHub draws as a 3D model.

    Init Params:
        code (str): The model as ASCII STL text.

    Markdown:
        A fenced code block with the info string `stl`.

    Example:
        STL("solid cube\\nendsolid cube")
        # Writes:
        # ```stl
        # solid cube
        # endsolid cube
        # ```

    Note:
        GitHub shows a model that can be rotated instead of the source. The text is not
        checked.
    """
    return CodeBlock(code, info="stl")
