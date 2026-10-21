from collections.abc import Iterable


def prefix_lines(
    lines: Iterable[str],
    first: str,
    rest: str | None = None,
) -> tuple[str, ...]:
    """Put a prefix before every line.

    Args:
        lines: The lines to prefix.
        first: The prefix of the first line (`"> "`, `"- "`, `"[^1]: "`).
        rest: The prefix of the other lines. Defaults to `first`.

    Returns:
        The prefixed lines. An empty line gets the prefix without trailing spaces.
    """

    # 1. Without a separate prefix, every line gets the first one
    rest = first if rest is None else rest

    # 2. Prefix line by line; the first line is the only one with `first`
    prefixed = []
    for index, line in enumerate(lines):
        prefix = first if index == 0 else rest

        # 2.1 An empty line keeps the prefix but loses the spaces behind it
        prefixed.append(prefix + line if line else prefix.rstrip())

    return tuple(prefixed)


_DESIGN_NOTES = """
# prefix_lines — The Only Mechanism Behind Nesting

## Purpose
A quote prefixes its lines with `> `, a list item with its marker and then
with spaces, a footnote with `[^1]: ` and then four spaces. The whole nesting
of Markdown is this function applied from the inside out.

## `first` and `rest`
The first line carries the marker (`- `), the others are only indented
(`"  "`), so a continuation stays inside the item.

## Empty Lines
`"> "` in front of an empty line would leave a trailing space. The prefix is
stripped (`">"`), and a spaces-only prefix becomes an empty line, which is
what Markdown needs inside a list item.
"""
