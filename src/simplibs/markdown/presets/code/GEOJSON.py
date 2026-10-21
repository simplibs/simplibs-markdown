# Outers
from ...blocks import CodeBlock


def GEOJSON(code: str) -> CodeBlock:
    """Build a block that GitHub draws as a map.

    Init Params:
        code (str): The map as GeoJSON text.

    Markdown:
        A fenced code block with the info string `geojson`.

    Example:
        GEOJSON('{"type": "Point", "coordinates": [14.42, 50.09]}')
        # Writes:
        # ```geojson
        # {"type": "Point", "coordinates": [14.42, 50.09]}
        # ```

    Note:
        GitHub draws an interactive map instead of showing the source. The text is not
        checked.
    """
    return CodeBlock(code, info="geojson")
