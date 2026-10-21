from .BreakChar import BreakChar
from .FenceChar import FenceChar
from .FootnoteRole import FootnoteRole
from .HeadingStyle import HeadingStyle
from .HtmlMode import HtmlMode


_DESIGN_NOTES = """
# blocks enums — Choices of the Block Nodes

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component      | Type | Description                                           |
| :------------- | :--- | :---------------------------------------------------- |
| `BreakChar`    | Enum | The character that draws a thematic break.            |
| `FenceChar`    | Enum | The character that fences a code block.               |
| `FootnoteRole` | Enum | Whether a footnote is a marker in text or a definition. |
| `HeadingStyle` | Enum | How a heading is written (ATX, closed ATX, setext).   |
| `HtmlMode`     | Enum | Whether an HTML node is a block, inline or a comment. |
"""
