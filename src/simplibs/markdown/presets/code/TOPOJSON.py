# Outers
from ...blocks import CodeBlock


def TOPOJSON(code: str) -> CodeBlock:
    """Build a block that GitHub draws as a map.

    Init Params:
        code (str): The map as TopoJSON text.

    Markdown:
        A fenced code block with the info string `topojson`.

    Example:
        TOPOJSON('{"type": "Topology", "objects": {}}')
        # Writes:
        # ```topojson
        # {"type": "Topology", "objects": {}}
        # ```

    Note:
        GitHub draws an interactive map instead of showing the source. The text is not
        checked.
    """
    return CodeBlock(code, info="topojson")
