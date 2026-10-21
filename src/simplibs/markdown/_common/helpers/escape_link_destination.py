def escape_link_destination(dest: str) -> str:
    """Write a link destination so that it survives parsing.

    Args:
        dest: The destination (a URL or a path).

    Returns:
        The destination as it is when that is safe, otherwise wrapped in `<...>`
        with the angle brackets escaped. In both forms every backslash is doubled.
    """

    # 1. Count the parentheses; a destination is safe only when they pair up
    depth = 0
    balanced = True
    for char in dest:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                balanced = False
    balanced = balanced and depth == 0

    # 2. A plain destination has no space or control character and does not start with '<'
    plain = bool(dest) and balanced and not dest.startswith("<") and not any(
        char.isspace() or ord(char) < 32 for char in dest
    )

    # 3. A parser reads a backslash before punctuation as an escape, so every backslash is doubled
    escaped = dest.replace("\\", "\\\\")
    if plain:
        return escaped

    # 4. Everything else goes between angle brackets, with the brackets escaped as well
    escaped = escaped.replace("<", "\\<").replace(">", "\\>")
    return "<" + escaped + ">"


_DESIGN_NOTES = """
# escape_link_destination — A Destination That Does Not End Early

## Purpose
`[a](my file.pdf)` and `[a](f(x.html)` are not links. A destination with a
space, a control character, or unbalanced parentheses has to be written in
angle brackets.

## Decisions
* The plain form is kept when it is safe, so ordinary URLs stay readable.
* Balanced parentheses are fine (`https://en.wikipedia.org/wiki/A_(b)`), only
  unbalanced ones force the angle form.

## Backslashes Are Doubled in Both Forms
A parser reads `\\*` in a destination as an escaped `*`, so `a\\*b` written
as it is would lose its backslash and point to `a*b`. A backslash at the end
is worse: `x\\` would escape the closing parenthesis and the link would not
end. Doubling every backslash (`a\\\\*b`, `x\\\\`) gives back the destination
that was given. A path such as `C:\\dir\\f.txt` is written `C:\\\\dir\\\\f.txt`,
which a parser reads as the original.

## Why It Lives in `_common`
Used by `Link` (`inline`) and `LinkDefinition` (`blocks`). It moved here from
the inline helpers when the second user appeared.
"""
