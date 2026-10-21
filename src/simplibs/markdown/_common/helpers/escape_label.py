def escape_label(label: str) -> str:
    """Write a link label so that its brackets and backslashes do not end it early.

    Args:
        label: The label, normally already normalized (see `normalize_label`).

    Returns:
        The label with every backslash, `[` and `]` escaped by a backslash.
    """

    # 1. The backslash goes first, so the backslashes added below are not doubled
    return label.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


_DESIGN_NOTES = """
# escape_label — A Label That Does Not End Early

## Purpose
`[text][x]y]` is not a reference to the label `x]y`: the first `]` ends the
label and the rest is text. A bracket or a backslash in a label has to be
escaped, in the reference and in its definition alike.

## One Function for Both Sides
`Link` (kind `REFERENCE`) and `LinkDefinition` write their label through
`escape_label(normalize_label(label))`. The two used to differ: the
definition escaped, the link did not, so a label with a bracket never found
its definition. One function makes that impossible to repeat.

## Not Part of `normalize_label`
`normalize_label` changes what the label *is* (whitespace is collapsed); this
function changes only how it is *written*. A label is stored normalized and
escaped when it is output, so `label` stays readable on the node.

## Why It Lives in `_common`
Used by `Link` (`inline`) and `LinkDefinition` (`blocks`).
"""
