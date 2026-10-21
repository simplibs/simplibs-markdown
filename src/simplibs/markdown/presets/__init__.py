from .alerts import CAUTION, IMPORTANT, NOTE, TIP, WARNING
from .code import GEOJSON, MATH_BLOCK, MERMAID, STL, TOPOJSON
from .emphasis import BOLD, BOLD_ITALIC, ITALIC, STRIKETHROUGH
from .headings import H1, H2, H3, H4, H5, H6
from .html import ANCHOR, COMMENT, DETAILS, KBD, MARK, SUB, SUP
from .links import AUTOLINK, BARE_URL, IMAGE
from .lists import BULLET_LIST, DONE_ITEM, NUMBERED_LIST, TASK_ITEM
from .references import COLOR_CHIP, COMMIT_REF, EMOJI, ISSUE_REF, MENTION
from .spacing import EMPTY_LINE, HARD_BREAK, RULE


__all__ = [
    # alerts
    "CAUTION", "IMPORTANT", "NOTE", "TIP", "WARNING",
    # code
    "GEOJSON", "MATH_BLOCK", "MERMAID", "STL", "TOPOJSON",
    # emphasis
    "BOLD", "BOLD_ITALIC", "ITALIC", "STRIKETHROUGH",
    # headings
    "H1", "H2", "H3", "H4", "H5", "H6",
    # html
    "ANCHOR", "COMMENT", "DETAILS", "KBD", "MARK", "SUB", "SUP",
    # links
    "AUTOLINK", "BARE_URL", "IMAGE",
    # lists
    "BULLET_LIST", "DONE_ITEM", "NUMBERED_LIST", "TASK_ITEM",
    # references
    "COLOR_CHIP", "COMMIT_REF", "EMOJI", "ISSUE_REF", "MENTION",
    # spacing
    "EMPTY_LINE", "HARD_BREAK", "RULE",
]


_DESIGN_NOTES = """
# presets — Names for the Things You Write Often

## Purpose
`H1("Title")`, `BOLD("x")`, `NOTE("text")`, `BULLET_LIST(...)`. Each preset is
one node with the arguments filled in, so a document reads like the Markdown
it produces.

## Domain, Not Root
Presets are imported from `simplibs.markdown.presets`, like `rules` and
`actions` in other libraries. The package root exports the nodes and the
enums; this keeps the root short and the presets a vocabulary you opt into.

## Naming
A preset that needs arguments is a function with a capitalized name
(`BOLD(...)`), the same convention as `ANY` and `ONE_OR_MORE` in
`simplibs-regex`. A preset without arguments is a ready instance (`RULE`,
`HARD_BREAK`).

## No Logic
A preset only calls a node. Every check and every error card comes from the
node, so presets add nothing to test beyond that they pass their arguments on.

## Internal Components Registry

| Sub-package  | Kind               | What it holds                                                    |
| :----------- | :----------------- | :--------------------------------------------------------------- |
| `alerts`     | Block presets      | `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`.                |
| `code`       | Block presets      | `MERMAID`, `GEOJSON`, `TOPOJSON`, `STL`, `MATH_BLOCK`.           |
| `emphasis`   | Inline presets     | `BOLD`, `ITALIC`, `BOLD_ITALIC`, `STRIKETHROUGH`.                |
| `headings`   | Block presets      | `H1` to `H6`.                                                    |
| `html`       | Mixed presets      | `DETAILS`, `SUP`, `SUB`, `MARK`, `KBD`, `COMMENT`, `ANCHOR`.     |
| `links`      | Inline presets     | `IMAGE`, `AUTOLINK`, `BARE_URL`.                                 |
| `lists`      | Container presets  | `BULLET_LIST`, `NUMBERED_LIST`, `TASK_ITEM`, `DONE_ITEM`.        |
| `references` | Inline presets     | `MENTION`, `ISSUE_REF`, `COMMIT_REF`, `EMOJI`, `COLOR_CHIP`.     |
| `spacing`    | Mixed presets      | `EMPTY_LINE`, `RULE`, `HARD_BREAK`.                              |
"""
