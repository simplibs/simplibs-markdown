import re
# Inners
from simplibs.markdown.inline._helpers.constants.ALWAYS_ESCAPED import ALWAYS_ESCAPED
from simplibs.markdown.inline._helpers.constants.LINE_START_ESCAPED import LINE_START_ESCAPED


def escape_text(text: str) -> str:
    """Escape everything in a text that Markdown could read as formatting.

    Args:
        text: The text, possibly with several lines.

    Returns:
        A text that renders as the original.
    """

    # 1. Work line by line, because some marks matter only at the start of a line
    escaped_lines = []
    for line in text.split("\n"):

        # 1.1 Escape the characters that mean formatting anywhere
        line = "".join("\\" + char if char in ALWAYS_ESCAPED else char for char in line)

        # 1.2 Split off the indentation; the line start is judged after it
        body = line.lstrip(" ")
        indent = line[: len(line) - len(body)]

        # 1.3 A heading, list or underline mark at the start of the line is escaped
        if body and body[0] in LINE_START_ESCAPED:
            body = "\\" + body

        # 1.4 So is a number that would start an ordered list ("1." or "1)")
        else:
            match = re.match(r"\d{1,9}(?=[.)])", body)
            if match:
                body = body[: match.end()] + "\\" + body[match.end():]

        escaped_lines.append(indent + body)

    # 2. Join the lines back
    return "\n".join(escaped_lines)


_DESIGN_NOTES = """
# escape_text — Text That Stays Text

## Purpose
The strings the author passes are content, not Markdown. `"2024. was a year"`
must not become a list and `"*not bold*"` must not become emphasis.

## Two Kinds of Escape
* Characters with a meaning anywhere (`ALWAYS_ESCAPED`) are escaped wherever
  they are.
* Marks with a meaning only at the start of a line (`LINE_START_ESCAPED`, and
  a number followed by `.` or `)`) are escaped only there, after any
  indentation.

## Checked Against a Parser
The output was compared with `markdown-it-py` on thousands of random strings
built from these characters; the text came back unchanged every time.

## Known Noise
See `ALWAYS_ESCAPED`: the list is cautious and the source gets extra
backslashes. Leaner escaping is a round-2 topic.
"""
