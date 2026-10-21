def normalize_label(label: str) -> str:
    """Collapse every run of whitespace in a label into one space.

    Args:
        label: A link or definition label.

    Returns:
        The label without leading, trailing or repeated whitespace.
    """

    # 1. `split()` without an argument drops the ends and collapses the runs
    return " ".join(label.split())


_DESIGN_NOTES = """
# normalize_label — One Spelling of a Label

## Purpose
CommonMark matches `[Foo   Bar]` with `[foo bar]`, so a reference link and its
definition can differ in whitespace and still belong together. Both sides
write the label through this function and therefore agree.

## Only Whitespace
It changes what the label *is*, not how it is written. Brackets and
backslashes in a label are `escape_label`'s job; both nodes call the two
functions one after the other.

## Why It Lives in `_common`
Used by `Link` (`inline`) and `LinkDefinition` (`blocks`).

## Removed Since the Draft
The unused `casefold` parameter. Case is left as the author wrote it; the
renderer ignores case when it matches labels.
"""
