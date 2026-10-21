def escape_link_title(title: str) -> str:
    """Write a link title with the quotes that fit it.

    Args:
        title: The title text.

    Returns:
        The title in double quotes, in single quotes when it contains a double
        quote, or in double quotes with escapes when it contains both.
    """

    # 1. Backslashes are escaped in every form
    title = title.replace("\\", "\\\\")

    # 2. Prefer the quote the title does not contain
    if '"' not in title:
        return f'"{title}"'
    if "'" not in title:
        return f"'{title}'"

    # 3. A title with both quotes escapes the double ones
    return '"' + title.replace('"', '\\"') + '"'


_DESIGN_NOTES = """
# escape_link_title — A Title in the Right Quotes

## Purpose
A title is written `"like this"`, `'like this'` or `(like this)`. A quote
inside it would end the title early.

## Decisions
* Double quotes first, single quotes when the title has a double quote, and
  escapes only when it has both. Most titles need no escape at all.
* The parenthesis form is never written.

## Why It Lives in `_common`
Used by `Link` (`inline`) and `LinkDefinition` (`blocks`).
"""
