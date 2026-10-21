from .GEOJSON import GEOJSON
from .MATH_BLOCK import MATH_BLOCK
from .MERMAID import MERMAID
from .STL import STL
from .TOPOJSON import TOPOJSON


_DESIGN_NOTES = """
# code presets

## Purpose
`CodeBlock` with an info string that GitHub renders as more than code.

## Internal Components Registry

| Component    | Type     | Description                                 |
| :----------- | :------- | :------------------------------------------ |
| `GEOJSON`    | Function | A GeoJSON map.                              |
| `MATH_BLOCK` | Function | A display math expression.                  |
| `MERMAID`    | Function | A Mermaid diagram.                          |
| `STL`        | Function | An ASCII STL 3D model.                      |
| `TOPOJSON`   | Function | A TopoJSON map.                             |
"""
